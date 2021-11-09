import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

print('system version:', sys.version)

def send_mes():
  my_sender = os.environ.get("SENDER")
  my_pass = os.environ.get("MIYAO")
  my_user = os.environ.get("TARGET_MAIL")
  print('target mail: ', my_user, "; sender: ", my_sender, "; pass: ", my_pass)
  

send_mes()
