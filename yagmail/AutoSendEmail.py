import yagmail
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

            # 使用 yagmail 发送邮件
            yag = yagmail.SMTP(user=sender_email, password=sender_password, host=smtp_server, port=smtp_port)

            # 设置邮件内容
            contents = [body]

            # 发送邮件时同时传递附件（如果有）
            yag.send(to=recipients, subject=subject, contents=contents, attachments=attachments)

            print(f"邮件 '{subject}' 发送成功！")
    except Exception as e:
        print(f'邮件发送失败: {e}')

# 调用示例
if __name__ == "__main__":
    config_file = 'config.json'
    config = load_config(config_file)
    send_email(config)
