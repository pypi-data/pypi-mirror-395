import smtplib,sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def 发送邮件(邮件主题, 邮件信息, 发送邮箱地址 = None, 接受邮箱地址 = None, 发送邮箱密码 = None, 停止程序 = True):
    """
    :param 邮件主题: 邮件主题(标题)
    :param 邮件信息: 邮件文本信息
    :param 发送邮箱地址: 6666@qq.com
    :param 接受邮箱地址: 8888@qq.com
    :param 发送邮箱密码: 发送邮箱密码不是登录邮箱密码，自行百度Python发送邮件密码
    :param 停止程序: 停止程序运行，默认为True
    """
    # 发件人和收件人信息
    sender_email = 发送邮箱地址 or "3215176932@qq.com"
    receiver_email = 接受邮箱地址 or "xdsndy@qq.com"
    password = 发送邮箱密码 or "rbfgdpvrpxxcddif"
    # 创建邮件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = 邮件主题

    # 添加邮件正文
    message.attach(MIMEText(str(邮件信息), "plain"))

    server = smtplib.SMTP("smtp.qq.com", 587, timeout=10)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

    if 停止程序:
        sys.exit()