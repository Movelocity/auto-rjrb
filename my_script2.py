import sys
from email.mime.text import MIMEText
from email.utils import formataddr

print('system version:', sys.version)

def send_mes():
  my_sender = '209848539@qq.com'
  my_pass = 'vyeytokvzjmrbjba'
  try:
    msg = MIMEText('hello', 'plain', 'utf-8')  # 填写邮件内容
    msg['From'] = formataddr(["in the campus", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["209848539@qq.com", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = 'OK'  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
  except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
    print(Exception)

send_mes()
