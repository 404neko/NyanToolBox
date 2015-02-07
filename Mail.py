import smtplib
from email.mime.text import MIMEText
from email.header import Header

def SendMail(Login,Head,Subject,Content):
	Server=Login[0]
	UserName=Login[1]
	PassWord=Login[2]
	Sender=Head[0]
	Receiver=Head[1]
	Msg=MIMEText(Content,'html','UTF-8')
	Msg['Subject']=Header(Subject,'UTF-8')
	SMTP=smtplib.SMTP()
	SMTP.connect(Server)
	SMTP.ehlo()
	SMTP.starttls()
	SMTP.login(UserName,PassWord)
	SMTP.sendmail(Sender,Receiver,Msg.as_string())
	SMTP.quit()