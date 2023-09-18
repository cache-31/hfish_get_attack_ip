#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
import json
import time
import datetime

#获取攻击IP
def get_attack_ip():
    end_time = int(time.time())
    five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)  #如需要获取几天前的数据可以将minutes=5改为days=x
    five_minutes_ago = int(time.mktime(five_minutes_ago.timetuple()))
    url = "https://ip:port/api/v1/attack/ip?api_key=xxxx"
    data = {
      "start_time": five_minutes_ago,
      "end_time": end_time,
      "intranet": -1,
      "source": 0,
      "threat_label": [ ]
    }
    req = requests.post(url, json=data, verify=False)
    return req.content

#推送告警消息至Webhook，根据实际情况修改代码
def post_alarm(attack_ip):
    alarmbot_url = "https://ip:port/webhook/send?api_key=xxxx"
    data = {
        "content":f"【发现内网攻击行为】\n近五分钟内【{attack_ip}】对内网服务器发起攻击，请尽快排查！"
    }
    requests.post(alarmbot_url, json=data)

response_text = json.loads(get_attack_ip())
attack_ip = response_text.get('data', {}).get('attack_ip')
if attack_ip != []:
  attack_ip = str(attack_ip).replace("[\'", "").replace("\']", "").replace("\'","").replace("\'","")
  # print(attack_ip)
  post_alarm(attack_ip)
else:
   print('there is no attack ip !')

    
