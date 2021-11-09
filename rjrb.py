import sys
import os
import json
import logging
import requests, time, random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime

print('system version:', sys.version)


class CheckBot:
      def __init__(self):
        self.data = "{}"
        self.my_Name = "Volunteer"
        self.my_sender = os.environ.get("SENDER")
        self.my_pass = os.environ.get("MIYAO")
        self.my_user = '(mail of reciever)you need to pass that arg to submit()'
        self.api = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.headers = {
            "Host": "student.wozaixiaoyuan.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",  #修改6
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/147/page-frame.html",
            "Content-Length": "360",
            "JWSESSION": ""
        }
        self.data = {
            "answers": '["0"]',
            "seq": self.get_seq(),
            "temperature": self.get_random_temprature(),
            "longitude": os.environ.get("JINGDU"),  # 经度
            "latitude": os.environ.get("WEIDU"),  # 纬度
            "country": "中国",
            "province": "广东省",
            "city": os.environ.get("CITY"),
            "district": os.environ.get("DISTRICT")
        }
      
      # 获取随机体温
      def get_random_temprature(self):
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.2, 36.7))

      # seq的1,2,3代表早，中，晚
      def get_seq(self):
        current_hour = datetime.datetime.now().hour+8
        if 0 <= current_hour <= 9:
            return "1"
        elif 11 <= current_hour < 15:
            return "2"
        elif 17 <= current_hour < 23:
            return "3"
        else:
            return 1

      def run(self):
        print(datetime.datetime.now()+8)
        print("second header = ", self.headers)
        res = requests.post(self.api, headers=self.headers, data=self.data, ).json()  # 打卡提交
        print("result = ", res)
        try:
            msg = MIMEText(self.my_Name+"  "+get_status(res), 'plain', 'utf-8')  # 填写邮件内容
            msg['From'] = formataddr(["GithubAction", self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["Dear_reciever", self.my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = get_status(res)  # 邮件的主题，也可以说是标题
      
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
            server.login(self.my_sender, self.my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
            server.sendmail(self.my_sender, [self.my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            res = False
            print(res)
        return True
      
      def submit(self, username, password, mailbox, host, user_agent, name):
        header = {
            "Host": host,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us,en",
            "Connection": "keep-alive",
            "User-Agent": user_agent,
            "Content-Length": "360",
        }
        print("first header = ", header)
        self.headers["User-Agent"] = user_agent
        self.my_Name = name
        self.my_user = mailbox
        self.data["temperature"] = self.get_random_temprature() # 更新一次体温
        print("data = ", self.data)
        loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        url = loginUrl + "?username=" + username + "&password=" + password

        session = requests.session()
        respt = session.post(url, data=self.data, headers=header)
        res = json.loads(respt.text)
        if res["code"] == 0:
            print("Login success.")
            jwsession = respt.headers['JWSESSION']
            self.headers["JWSESSION"] = str(jwsession)
        else:
            print(res)
            print('Login failed.')
            return
        self.run()
        
        
        
def dailyCheck():
    checkbot = CheckBot()
    checkbot.submit(username="GHSaccount",
                    password="GHScode",  # 每次微信重登后好像都要改密码
                    host="gw.wozaixiaoyuan.com",
                    user_agent="Dalvik/2.1.0 (Linux; U; Android 11; M2102J2SC Build/RKQ1.200826.002)",
                    mailbox=os.environ.get("TARGET"),
                    name="Captain ")

    
dailyCheck()
