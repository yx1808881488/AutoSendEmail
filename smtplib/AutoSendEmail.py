import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json

# 读取配置文件
def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

# 配置邮件信息
def send_email(config):
    try:
        smtp_server = config['smtp_server']
        smtp_port = config['smtp_port']
        sender_email = config['sender']
        sender_password = config['password']

        # 循环发送多封邮件，每封邮件有不同的主题、内容和接收者
        for email_config in config['emails']:
            subject = email_config['subject']
            body = email_config['body']
            recipients = email_config['recipients']
            attachments = email_config.get('attachments', [])  # 获取多个附件路径

            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipients)  # 多个收件人时以逗号分隔
            msg['Subject'] = subject

            # 添加邮件正文
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加附件
            if attachments:
                for attachment in attachments:
                    if attachment and attachment != 'None':
                        with open(attachment, 'rb') as file:
                            part = MIMEApplication(file.read(), Name=attachment)
                            part['Content-Disposition'] = f'attachment; filename="{attachment.split("/")[-1]}"'
                            msg.attach(part)

            # 连接SMTP服务器并发送邮件
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipients, msg.as_string())  # 发送邮件
                print(f"邮件 '{subject}' 发送成功！")
    except Exception as e:
        print(f'邮件发送失败: {e}')

# 调用示例
if __name__ == "__main__":
    config_file = 'config.json'
    config = load_config(config_file)
    send_email(config)
