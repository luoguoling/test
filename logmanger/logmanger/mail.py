#!/usr/bin/env python


# -*- coding: utf-8 -*-


import smtplib


from email.mime.text import MIMEText


import MySQLdb


def send_mail(to_list,sub,content):




    mail_host="smtp.qq.com"


    mail_user="992975991"


    mail_pass="Luoguoling123?"


    mail_postfix="qq.com"


    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"


    msg = MIMEText(content)


    msg['Subject'] = sub


    msg['From'] = me


    msg['To'] = to_list


    try:


        s = smtplib.SMTP()


        s.connect(mail_host)


        s.login(mail_user,mail_pass)


        s.sendmail(me, to_list, msg.as_string())


        s.close()


        return True




    except Exception, e:


        print str(e)


        return False


if __name__ == '__main__':


    strcontent="mail content"


    mailto_list = ['lgl15984@163.com', '992975991@qq.com']


    for mailto in mailto_list:


        send_mail(mailto, "xxx monitor and report", strcontent.encode('utf-8'))
