from rich import print
import time
import os

__all__ = ["os_command", "get_queue_node", "query_queue", "running_jobs", "submit_job", "get_job_status", "sbatch_job"]


# 负责执行命令并返回输出
def os_command(cmd):
    import subprocess
    print(f'🔍 执行命令: {cmd}')
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # 打印错误信息（若有，方便排查问题）
    if result.stderr:
        print(f'❌ 错误输出: {result.stderr.strip()}')
    # 检查命令是否执行成功（非0为失败）
    if result.returncode != 0:
        print(f'❌ 命令执行失败，退出码: {result.returncode}')
        return None
    return result.stdout


# 返回“队列名:节点数”的字典
def get_queue_node():
    import re
    # 执行 sinfo | grep "idle" 获取空闲队列数据
    cmd = 'sinfo | grep "idle"'
    output = os_command(cmd)
    if not output:  # 命令执行失败或无输出，返回空字典
        return {}
    
    # 初始化结果字典：键=队列名，值=节点数
    queue_node_dict = {}
    # 按行解析命令输出
    for line in output.strip().split('\n'):
        line = line.strip()
        if not line:  # 跳过空行
            continue
        
        # 正则匹配：仅捕获“队列名”（第1组）和“节点数”（第2组）
        # 末尾用 .* 忽略节点列表，不影响匹配
        pattern = r"^(\S+)\s+\S+\s+\S+\s+(\d+)\s+idle\s+.*$"
        match = re.match(pattern, line)
        
        if match:
            queue_name = match.group(1)    # 提取队列名作为字典的键
            node_count = int(match.group(2))# 提取节点数作为字典的值（转为整数）
            queue_node_dict[queue_name] = node_count  # 存入字典
    
    return queue_node_dict


def query_queue(need_node=1, queue_list =['dcu','bigmem','cpu_parallel','cpu_single']):
    queue_dict = get_queue_node()
    hs = None
    for my_queue in queue_list:
        if my_queue == 'cpu_parallel':
            for mq in ['cpu_parallel','cpu_parallel*']:
                if mq in queue_dict and queue_dict[mq] >= need_node:
                    hs = 'cpu_parallel'
                    break
        else:
            if my_queue in queue_dict and queue_dict[my_queue] >= need_node:
                hs = my_queue
                break
    return hs


def running_jobs():
    # 通过qstat判断任务状态，是否还在进行中
    # status = os.popen('qstat').read()
    status = os.popen('squeue').read()
    Jobs = status.split('\n')[1:]
    ids = [job.split()[0] for job in Jobs if job != '']
    return ids


def sbatch_job(script='run.slurm'):
    '''提交任务到集群，并返回任务ID'''
    content_sub = os_command(f"sbatch {script}")
    if not content_sub:
        print('提交任务命令没有返回输出或返回了错误！')
        return None
    else:
        content_sub_lower = content_sub.lower()
        if 'error' in content_sub_lower or 'failed' in content_sub_lower:
            print('提交任务时出现错误（从输出检测到 error/failed）！')
            print(f'命令输出: {content_sub.strip()}')
            return None
        else:
            print(f'提交任务成功，{content_sub.strip()}')
            job_id = content_sub.strip().split()[-1]
            return job_id


def get_job_status(jobid):
    """
    获取指定任务ID的ST状态（如R/PD/S等）
    :param jobid: 任务ID（整数或字符串格式均可）
    :return: 任务的ST状态字符串，未找到任务返回None
    """
    import re  # 复用正则模块，内部导入避免依赖冲突
    jobid_str = str(jobid).strip()
    if not jobid_str.isdigit():
        print(f'⚠️  输入的任务ID {jobid} 格式无效，需为纯数字')
        return None
    
    # 执行squeue命令精准匹配目标任务（避免多ID混淆）
    cmd = f'squeue | grep -w {jobid_str}'
    output = os_command(cmd)
    
    if not output:
        print(f'❌ 未找到任务ID {jobid_str} 的相关信息（可能已完成或输入错误）')
        return None
    
    # 解析输出中的ST状态（匹配JOBID后的第五个字段，处理多空格分隔）
    # 正则匹配逻辑：忽略前置空格 → 匹配JOBID → 匹配后续任意字符 → 捕获ST状态（单个大写字母/字母组合）
    pattern = r'\s*\d+\s+\S+\s+\S+\s+\S+\s+(\S+)'
    match = re.search(pattern, output)
    if match:
        st_status = match.group(1)
        print(f'✅ 任务ID {jobid_str} 的ST状态：{st_status}')
        return st_status
    else:
        print(f'❌ 无法解析任务ID {jobid_str} 的ST状态，命令输出：{output.strip()}')
        return None



def submit_job(working_dir=None, script_tmp='run.slurm', script_run='run.slurm', need_node=1, queue_tmp='<queue_name>', queue_list=['dcu', 'bigmem', 'cpu_parallel', 'cpu_single'], max_job=38, wait=False): 
    '''提交任务到集群，并返回任务ID'''
    from .oa_file import replace_content
    import datetime
    if working_dir is None:
        working_dir = os.getcwd()
    os.chdir(working_dir)
    print(f'切换工作目录到: {working_dir}')
    
    if need_node > 1 and 'cpu_single' in queue_list:
        queue_list.remove('cpu_single')
    
    while True:
        running_job = running_jobs()
        if not running_job or len(running_job) < max_job:
            queue = query_queue(need_node=need_node, queue_list=queue_list)
            if queue:
                replace_content(script_tmp, {f'{queue_tmp}': f"{queue}"}, False, f'{working_dir}', script_run)
                print(f'找到计算资源，提交任务，队列：{queue}')
                print(f'Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                job_id = sbatch_job(script_run)
                # 避免在 None 上使用 'in' 导致 TypeError：os_command 在失败时会返回 None
                if job_id:
                    print(f'任务ID: {job_id}，等待30秒后检查任务状态！')
                    time.sleep(30)
                    job_st = get_job_status(job_id)
                    if job_st == 'PD':
                        os_command(f'scancel {job_id}')
                        print(f'因作业{job_id}处于PD状态，取消！')
                        time.sleep(30)
                    else:
                        break
                else:
                    print('等待30秒后重试！')
                    time.sleep(30)
            else:
                print('没有足够的计算资源，等待30秒后重试！')
                time.sleep(30)
        else:
            print(f'当前系统任务数：{len(running_job)}，等待60秒后重试！')
            time.sleep(60)
    
    print(f'等待10秒后，继续查询任务或进行下一个操作！')
    time.sleep(10)
    
    if wait:
        while True:
            if job_id in running_jobs():
                print(f'Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                # print(f'任务{job_id}正在队列中...')
                get_job_status(job_id)
                time.sleep(60)
            else:
                print(f'任务{job_id}已完成！')
                break
    else:
        print(f'任务{job_id}已提交，不等待其完成，继续执行后续操作！')
    
    return job_id

if __name__ == "__main__":
    pass
