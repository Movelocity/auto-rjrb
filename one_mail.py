import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime

def send_mes():
  sender = os.environ.get("SENDER")
  key = os.environ.get("MIYAO")
  reciever = os.environ.get("TARGET")
  #print('target mail len: ', len(reciever), "; sender: ", sender, "; pass: ", key) #you can see these args show like *** cause they are hidden
  try:
    content = 'Have a nice day.\\n\tClock: '+str(datetime.datetime.now().hour+8)
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["GithubAction", sender])
    msg['To'] = formataddr(["Locity", reciever])
    msg['Subject'] = 'The title was eaten'
    # message body formed
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, key)
    server.sendmail(sender, [reciever, ], msg.as_string())
    server.quit()
  except Exception:
    print(Exception)
    return False
  return True
