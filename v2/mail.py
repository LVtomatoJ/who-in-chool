import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import traceback
import threading
from default import Mail
 
sender = Mail.sender
password = Mail.password
 
 
 
def send_mail(mail_to, subject, content, sub_type='plain'):
 
    ret = True
    try:
        msg = MIMEText(content, sub_type, 'utf-8')
        msg['From'] = formataddr([sender, sender])
        msg['To'] = formataddr([mail_to, mail_to])
        msg['Subject'] = subject
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [mail_to, ], msg.as_string())
        server.quit()
    except Exception :
        traceback.format_exc()
        ret = False
    return ret
 
 
def send_async_mail(mail_to, subject, content, sub_type='plain'):
    thr = threading.Thread(target=send_mail, args=[mail_to, subject, content, sub_type])
    thr.start()
 
 
def send_async_mail_prepare(title, content, user_email):
    send_async_mail(user_email,title,content)
 

