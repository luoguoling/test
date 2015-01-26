#coding:utf-8
import threading
import MySQLdb
from datetime import datetime
import time,os
import smtplib
from email.mime.text import MIMEText
#from log import logger
import logging
def get_log():
    logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='myapp.log',
    filemode='w')
    logger = logging.getLogger('root')
    return logger
def get_con():
    host = "211.237.12.103"
    port = 5849
    logsdb = "serverlist"
    user = "rolin"
    password = "abc123?"
    con = MySQLdb.connect(host=host, user=user, passwd=password, db=logsdb, port=port, charset="utf8")
    return con

def calculate_time():
    now = time.mktime(datetime.now().timetuple())-60*2
    result = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    return result
def backup_time():
    now = time.mktime(datetime.now().timetuple())-60*2
    result = time.strftime('%Y%m%d', time.localtime(now))
    backupresult = result + str(result)
    return backupresult


def get_data():
    select_time = calculate_time()
    get_log().info("select time:"+select_time)
    sql = "SELECT COUNT(DISTINCT gamedatadbname) FROM gameserverinfo WHERE agent='ynvng' and isdelete!=1  ORDER BY zone"
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    num1 = results[0]
    num = num1[0]
    cursor.close()
    conn.close()
    return num
def get_backupdata():
    backupnum = os.popen('ls *`date +%Y%m%d04`* |wc -l').read()
    return backupnum
def check():
    numdata = int(get_data())
    backupnum = int(get_backupdata())
    if numdata == backupnum:
        result = '韩国备份成功'
    else:
        result = "韩国备份失败"
    return result
def send_email(content):
 
    sender = "lgl15984@163.com"
    receiver = ["992975991@qq.com"]
    host = 'smtp.163.com'
    port = 465
    msg = MIMEText(content)
    msg['From'] = "lgl15984@163.com"
    msg['To'] = "992975991@qq.com"
    msg['Subject'] = "backup check"
 
    try:
        smtp = smtplib.SMTP_SSL(host, port)
        smtp.login(sender, 'xxxx')
        smtp.sendmail(sender, receiver, msg.as_string())
        getlog().info("send email success")
    except Exception, e:
        get_log().error(e)
def task():
    shijian = calculate_time()
    while True:
        get_log().info("monitor running")
        results = check()
        if results == "备份成功":
            content = "备份成功"
        else:
            content = "备份失败"
            send_email(content + shijian)
        time.sleep(2*60)

def run_monitor():
    monitor = threading.Thread(target=task)
    monitor.start()
 
 
if __name__ == "__main__":
    run_monitor()




