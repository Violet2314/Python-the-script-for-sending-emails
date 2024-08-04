import smtplib
import random
import subprocess
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import formataddr
from datetime import datetime

# 获取当前日期
now = datetime.now()
current_month = now.month
current_day = now.day

def run_cpp_exe(exe_path, work_dir):
    try:
        # 使用subprocess.run来执行exe文件，并捕获输出
        # cwd参数被设置为./random，这将使得可执行文件在./random目录中运行
        result = subprocess.run([exe_path], capture_output=True, text=True, cwd=work_dir, encoding='utf-8')
        # 打印输出结果
        output_lines = result.stdout.splitlines()
        heeder = output_lines[0]
        ans = output_lines[1]
        #print(heeder)
        #print(ans)
        return heeder, ans
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def email_send():
    # 邮件配置信息
    heeder, ans = run_cpp_exe('./random/std.exe', './random')
    if current_month == 8 and current_day == 10:
        ans = '七夕晚会你去吗？草芥和华恋有邀我去参加诶…………我是可以拒绝啦，可是那样好像显得我想太多了吧？你看，万一旁边都是情侣该怎么办？既然是七夕当天，草介和华恋是不是从前一天晚上就睡一起了？万一一大早撞见他们两个该如何面对？你也知道这些问题我其实一点也不在乎嘛，但刻意拒绝反而显得我想太多了。如果你参加的话，该怎么说呢，就有个护身符，或者说好列有人陪伴，我是这样想啦，所以………。你应该会来吧?\n'
        ans += '七夕晚会特别有意思哦。\n'
        ans += '你就当自己被骗了吧。\n'
        ans += '来吧。\n'
        ans += '快点上当受骗吧。\n'
        heeder = '快来参加七夕晚会！'

    print(heeder)
    print(ans)

    smtp_server = 'smtp.qq.com'  # 邮箱服务器
    smtp_port = 465  # 邮箱端口
    smtp_ssl = True  # 启用ssl
    smtp_user = 'anna_yanami@qq.com'
    smtp_password = 'divapeynaaafdbjj'  # 邮箱授权码，到邮箱网站中查看

    # 发送邮件信息
    sender = 'anna_yanami@qq.com'  # 发送者邮箱
    receivers = '3279499388@qq.com'  # 接收者邮箱

    # 创建邮件对象
    message = MIMEMultipart('related')
    message['From'] = formataddr(["八奈见杏菜", sender])
    message['To'] = formataddr(["顿感怪", receivers])
    message['Subject'] = Header(heeder, 'utf-8')  # 邮件标题

    # 邮件正文
    mail_content = f"""
    <html>
    <body>
        <img src="cid:image1">
        <p>{ans}</p>
    </body>
    </html>
    """
    message.attach(MIMEText(mail_content, 'html', 'utf-8'))
    num = random.randint(1,18)
    # 添加图片到正文中
    image_path = './image/'  # 图片路径
    image_path += str(num)
    image_path += '.png'
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data)
            image.add_header('Content-ID', '<image1>')
            message.attach(image)
    except Exception as e:
        print(f"Error: 无法读取图片: {e}")

    # 发送邮件
    try:
        smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 连接服务器
        smtp_obj.login(smtp_user, smtp_password)  # 登入发送者邮箱
        smtp_obj.sendmail(sender, receivers, message.as_string())  # 发送邮件指令
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 邮件发送失败: ", e)

def check_date_and_update():
    # 读取day.txt中的内容
    try:
        with open('day.txt', 'r') as file:
            lines = file.readlines()
            file_month = int(lines[0].strip())
            file_day = int(lines[1].strip())
    except Exception as e:
        print(f"Error reading day.txt: {e}")
        file_month, file_day = None, None

    # 判断当前日期和文件中的日期是否相同
    if file_month == current_month and file_day == current_day:
        print("今天已经发过了.")
        return  # 跳出函数

    # 如果日期不同，则继续执行email_send并更新day.txt
    email_send()  # 调用你的email_send函数

    # 更新day.txt中的内容
    try:
        with open('day.txt', 'w') as file:
            file.write(f"{current_month}\n{current_day}\n")
        print("日期更新.txt")
    except Exception as e:
        print(f"Error writing to day.txt: {e}")

if __name__ == "__main__":
    check_date_and_update()