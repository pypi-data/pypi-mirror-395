import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from rich import print
from rich.progress import track
from oafuncs.oa_down.user_agent import get_ua
from oafuncs.oa_file import remove
from oafuncs.oa_data import ensure_list

__all__ = ["download5doi"]


def _get_file_size(file_path, unit="KB"):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return "文件不存在"

    # 获取文件大小（字节）
    file_size = os.path.getsize(file_path)

    # 单位转换字典
    unit_dict = {
        "PB": 1024**5,
        "TB": 1024**4,
        "GB": 1024**3,
        "MB": 1024**2,
        "KB": 1024,
    }

    # 检查传入的单位是否合法
    if unit not in unit_dict:
        return "单位不合法，请选择PB、TB、GB、MB、KB中的一个"

    # 转换文件大小到指定单位
    converted_size = file_size / unit_dict[unit]

    return converted_size


class _Downloader:
    """
    根据doi下载文献pdf
    """

    # 进程级缓存：首次探测后的可用镜像列表，后续复用
    _alive_mirrors_cache: list[str] | None = None

    def __init__(self, doi, store_path, *, min_size_kb=50, timeout_html=15, timeout_pdf=30, sleep_secs=5, tries_each_url=3, debug=False):
        self.url_list = [
            r"https://sci-hub.se",
            r"https://sci-hub.ren",
            r"https://sci-hub.st",
            r"https://sci-hub.ru",  # 最好用的一个网站
            # ------------------------------------- 以下网站没验证
            r"https://sci-hub.in",
            r"https://sci-hub.hlgczx.com/",
        ]
        self.base_url = None
        self.url = None
        self.doi = doi
        self.pdf_url = None
        self.pdf_path = None
        # requests 期望 header 值为 str，这里确保 UA 是字符串而不是 bytes
        self.headers = {"User-Agent": str(get_ua())}
        # 10.1175/1520-0493(1997)125<0742:IODAOO>2.0.CO;2.pdf
        # self.fname = doi.replace(r'/', '_') + '.pdf'
        self.fname = re.sub(r'[/<>:"?*|]', "_", doi) + ".pdf"
        self.store_path = Path(store_path)
        self.fpath = self.store_path / self.fname
        self.wrong_record_file = self.store_path / "wrong_record.txt"
        self.sleep = sleep_secs
        self.cookies = None
        self.check_size = max(1, int(min_size_kb))
        self.url_index = 0
        self.try_times_each_url_max = max(1, int(tries_each_url))
        self.try_times = 0
        self.timeout_html = max(5, int(timeout_html))
        self.timeout_pdf = max(5, int(timeout_pdf))
        self.debug = bool(debug)

    # ---------------- 镜像可用性探测 ----------------
    def _is_mirror_alive(self, base_url: str) -> bool:
        """
        仅检测镜像根路径是否可连通（HTTP 200 即认为可用）。
        不访问具体 DOI，避免被动触发风控；只做连通性筛查。
        """
        try:
            r = requests.get(base_url + "/", headers=self.headers, timeout=8, allow_redirects=True)
            return 200 <= r.status_code < 400
        except Exception:
            return False

    def _ensure_alive_mirrors(self):
        # 若已经有进程级缓存，直接复用
        if _Downloader._alive_mirrors_cache is not None:
            self.url_list = list(_Downloader._alive_mirrors_cache)
            return

        print(f"[bold cyan]Probing mirrors connectivity (first run)...")
        alive = []
        for base in self.url_list:
            ok = self._is_mirror_alive(base)
            status = "OK" if ok else "DOWN"
            print(f"  [{status}] {base}")
            if ok:
                alive.append(base)
        if alive:
            _Downloader._alive_mirrors_cache = alive
            self.url_list = alive
            print(f"[bold cyan]Alive mirrors: {len(alive)}; pruned {len(set(self.url_list)) - len(alive) if self.url_list else 0}.")
        else:
            print("[bold yellow]No mirror passed probe; keep original list for fallback attempts.")

    def _extract_pdf_url_from_html(self, html: str) -> str | None:
        """
        从 Sci-Hub 页面 HTML 中尽可能稳健地提取 PDF 链接。

        兼容多种模式：
        - onclick="location.href='...pdf?download=true'"
        - <iframe id="pdf" src="...pdf?...">
        - <a ... href="...pdf?...">
        - 其他出现 .pdf 的 src/href 场景

        返回绝对 URL；若找不到返回 None。
        """
        text = html

        # 先尝试常见 onclick 跳转
        patterns = [
            # onclick="location.href='...pdf?...'" 或 document.location
            r"onclick\s*=\s*[\"']\s*(?:document\.)?location\.href\s*=\s*[\"']([^\"']+?\.pdf(?:[?#][^\"']*)?)[\"']",
            # iframe id="pdf" src="...pdf?..."
            r"<iframe[^>]+id\s*=\s*[\"']pdf[\"'][^>]+src\s*=\s*[\"']([^\"']+?\.pdf(?:[?#][^\"']*)?)[\"']",
            # 通用 a 标签 href
            r"<a[^>]+href\s*=\s*[\"']([^\"']+?\.pdf(?:[?#][^\"']*)?)[\"']",
            # 通用任意 src/href
            r"(?:src|href)\s*=\s*[\"']([^\"']+?\.pdf(?:[?#][^\"']*)?)[\"']",
        ]

        for pat in patterns:
            m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
            if m:
                got_url = m.group(1)
                # 规范化为绝对 URL
                if got_url.startswith("//"):
                    return "https:" + got_url
                if got_url.startswith("http://") or got_url.startswith("https://"):
                    return got_url
                # 其余按相对路径处理
                return urljoin(self.base_url + "/", got_url.lstrip("/"))

        return None

    def get_pdf_url(self):
        print("[bold #E6E6FA]-" * 120)
        print(f"DOI: {self.doi}")
        print(f"Requesting: {self.url}...")
        try:
            # 使用较小的超时时间避免长时间阻塞
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout_html)
            if response.status_code == 200:
                self.cookies = response.cookies
                text = response.text
                # 去除转义反斜杠，提升正则匹配成功率
                text = text.replace("\\", "")

                self.pdf_url = self._extract_pdf_url_from_html(text)
                if self.pdf_url:
                    if self.debug:
                        print(f"Found PDF link: {self.pdf_url}")
                    else:
                        print(f"Found PDF link (masked): .../{Path(self.pdf_url).name}")
                else:
                    print(
                        f"[bold #AFEEEE]The website {self.url_list[self.url_index]} does not expose a detectable PDF link (pattern mismatch)."
                    )
                    self.try_times = self.try_times_each_url_max + 1
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                print(f"[bold #AFEEEE]The website {self.url_list[self.url_index]} do not include the PDF file (HTTP error).")
                self.try_times = self.try_times_each_url_max + 1
        except Exception as e:
            print(f"Failed to retrieve the webpage. Error: {e}")
            self.try_times = self.try_times_each_url_max + 1

    def url_iterate(self):
        if self.url_index >= len(self.url_list):
            return
        url = self.url_list[self.url_index]
        self.base_url = url
        self.url = url + "/" + self.doi
        self.get_pdf_url()
        # for url in self.url_list:
        #     self.url = url + self.doi
        #     self.get_pdf_url()
        #     if self.pdf_url:
        #         break

    def write_wrong_record(self):
        # 先读取txt中的内容，如果已经存在则不再写入
        if self.wrong_record_file.exists():
            with open(self.wrong_record_file, "r") as f:
                lines = f.readlines()
            if self.doi in lines:
                return
        with open(self.wrong_record_file, "a") as f:
            f.write(self.doi + "\n")

    def download_pdf(self):
        if self.fpath.exists():
            fsize = _get_file_size(self.fpath, unit="KB")
            if fsize < self.check_size:
                # delete the wrong file
                os.remove(self.fpath)
                print(f"[bold yellow]The PDF file {self.fpath} is only {fsize:.2f} KB. It will be deleted and retry.")
            else:
                print("[bold #E6E6FA]-" * 120)
                print(f"[bold purple]The PDF file {self.fpath} already exists.")
                return
        self.url_index = 0
        already_downloaded = False
        self.try_times = 0
        while not already_downloaded:
            self.url_iterate()
            if not self.pdf_url:
                self.url_index += 1
                if self.url_index >= len(self.url_list):
                    print("Failed to download the PDF file.")
                    self.write_wrong_record()
                    return
                else:
                    self.try_times = 0
                    continue
            else:
                self.try_times += 1
            if self.try_times > self.try_times_each_url_max:
                self.url_index += 1
                if self.url_index >= len(self.url_list):
                    # print("Failed to download the PDF file.")
                    self.write_wrong_record()
                    return
            print(f"Downloading: {self.fname}...")
            try:
                response = requests.get(self.pdf_url, headers=self.headers, cookies=self.cookies, timeout=self.timeout_pdf)
                if response.status_code == 200:
                    with open(self.fpath, "wb") as f:
                        f.write(response.content)
                    fsize = _get_file_size(self.fpath, unit="KB")
                    if fsize < self.check_size:
                        # delete the wrong file
                        os.remove(self.fpath)
                        print(f"[bold yellow]The PDF file {self.fpath} is only {fsize:.2f} KB. It will be deleted and retry.")
                    else:
                        print(f"[bold green]Sucessful to download {self.fpath}")
                        already_downloaded = True
                else:
                    self.try_times = self.try_times_each_url_max + 1
                    print(f"Failed to download the PDF file. Status code: {response.status_code}")
                    print(f"[bold #AFEEEE]The website {self.url_list[self.url_index]} do not inlcude the PDF file.")
            except Exception as e:
                print(f"Failed to download the PDF file. Error: {e}")
            time.sleep(self.sleep)
            if self.try_times >= self.try_times_each_url_max:
                self.url_index += 1
                if self.url_index >= len(self.url_list):
                    print("\n[bold #CD5C5C]Failed to download the PDF file.")
                    self.write_wrong_record()
                    return
                if self.try_times == self.try_times_each_url_max:
                    print(f"Tried {self.try_times} times for {self.url_list[self.url_index-1]}.")
                    print("Try another URL...")


def _read_excel(file, col_name=r"DOI"):
    df = pd.read_excel(file)
    df_list = df[col_name].tolist()
    # 去掉nan
    df_list = [doi for doi in df_list if str(doi) != "nan"]
    return df_list


def _read_txt(file):
    with open(file, "r") as f:
        lines = f.readlines()
    # 去掉换行符以及空行
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def download5doi(
    store_path=None,
    doi_list=None,
    txt_file=None,
    excel_file=None,
    col_name=r"DOI",
    *,
    probe_mirrors: bool = True,
    min_size_kb: int = 50,
    timeout_html: int = 15,
    timeout_pdf: int = 30,
    tries_each_url: int = 3,
    sleep_secs: int = 5,
    force: bool = False,
    debug: bool = False,
):
    """
    Description:
        Download PDF files by DOI.

    Parameters:
        store_path: str, The path to store the PDF files.
        doi_list: list or str, The list of DOIs.
        txt_file: str, The path of the txt file that contains the DOIs.
        excel_file: str, The path of the excel file that contains the DOIs.
        col_name: str, The column name of the DOIs in the excel file. Default is 'DOI'.

    Returns:
        None

    Example:
        download5doi(doi_list='10.3389/feart.2021.698876')
        download5doi(store_path='I:\\Delete\\ref_pdf', doi_list='10.3389/feart.2021.698876')
        download5doi(store_path='I:\\Delete\\ref_pdf', doi_list=['10.3389/feart.2021.698876', '10.3389/feart.2021.698876'])
        download5doi(store_path='I:\\Delete\\ref_pdf', txt_file='I:\\Delete\\ref_pdf\\wrong_record.txt')
        download5doi(store_path='I:\\Delete\\ref_pdf', excel_file='I:\\Delete\\ref_pdf\\wrong_record.xlsx')
        download5doi(store_path='I:\\Delete\\ref_pdf', excel_file='I:\\Delete\\ref_pdf\\wrong_record.xlsx', col_name='DOI')
    """
    if not store_path:
        store_path = Path.cwd()
    else:
        store_path = Path(str(store_path))
    store_path.mkdir(parents=True, exist_ok=True)
    store_path = str(store_path)

    if doi_list:
        doi_list = ensure_list(doi_list)
    if txt_file:
        doi_list = _read_txt(txt_file)
    if excel_file:
        doi_list = _read_excel(excel_file, col_name)
    # 去重并清洗
    doi_list = [str(x).strip() for x in doi_list if str(x).strip()]
    doi_list = list(dict.fromkeys(doi_list))  # 保序去重

    # 只有在不是追加下载的场景下再清除 wrong_record
    if not force:
        remove(Path(store_path) / "wrong_record.txt")
    print(f"Downloading {len(doi_list)} PDF files...")
    for doi in track(doi_list, description="Downloading..."):
        dl = _Downloader(
            doi,
            store_path,
            min_size_kb=min_size_kb,
            timeout_html=timeout_html,
            timeout_pdf=timeout_pdf,
            sleep_secs=sleep_secs,
            tries_each_url=tries_each_url,
            debug=debug,
        )
        # 是否进行镜像探测
        if probe_mirrors:
            dl._ensure_alive_mirrors()
        dl.download_pdf()


if __name__ == "__main__":
    store_path = r"F:\AAA-Delete\DOI_Reference\5\pdf"
    excel_file = r"F:\AAA-Delete\DOI_Reference\5\savedrecs.xls"
    download5doi(store_path, excel_file=excel_file)
