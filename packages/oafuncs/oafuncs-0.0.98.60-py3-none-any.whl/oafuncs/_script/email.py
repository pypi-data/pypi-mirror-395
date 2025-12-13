from rich import print



def _send_message(msg_from, password, msg_to, title, content):
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    # 1. 连接邮箱服务器
    con = smtplib.SMTP_SSL("smtp.qq.com", 465)

    # 2. 登录邮箱
    # msg_from, password = _email_info()
    # con.login(msg_from, _decode_password(password))
    con.login(msg_from, password)

    # 3. 准备数据
    # 创建邮件对象
    msg = MIMEMultipart()

    # 设置邮件主题
    subject = Header(title, "utf-8").encode()
    msg["Subject"] = subject

    # 设置邮件发送者
    msg["From"] = msg_from

    # 设置邮件接受者
    msg["To"] = msg_to

    # or
    # content = '发送内容'
    msg.attach(MIMEText(content, "plain", "utf-8"))

    # 4.发送邮件
    con.sendmail(msg_from, msg_to, msg.as_string())
    con.quit()

    print(f"已通过{msg_from}成功向{msg_to}发送邮件！")
    print("发送内容为：\n{}\n\n".format(content))





if __name__ == "__main__":
    pass
