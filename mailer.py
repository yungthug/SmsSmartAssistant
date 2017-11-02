import imaplib,email,smtplib
import variablemanager as varmang
from main import log
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

server = imaplib.IMAP4_SSL('imap.gmail.com')
s = smtplib.SMTP('smtp.gmail.com', 587)

logged_in=False
def user_registration():
	global USER
	try:
		contents=varmang.read_from('glUser')
		if 'user:' in contents[0]:
			USER=contents[0].split('user:')[1]
		if 'pass:' in contents[1]:
			PSWD=contents[1].split('pass:')[1]
		server.login(USER,PSWD)
	except:
		while True:
			log('welcome! you will only be required to register your google account one')
			log('time unless you change your login credintials.')
			log('')
			log('IMPORTANT NOTE! this program will not relay communications until you')
			log('go into google account settings and "Allow less secure apps".')
			log('')
			USER=raw_input('Gmail: ')
			PSWD=raw_input('Password: ')
			try:
				server.login(USER,PSWD)
				varmang.write_to('glUser','user:'+USER+'\npass:'+PSWD)
				log('your username and password have been stored.')
				break
			except Exception as e:
				log(e)
	return USER,PSWD

def login():
	global server,s,logged_in
	if logged_in == False:
		USER,PSWD=user_registration()
		s.starttls()
		s.login(USER,PSWD)
		log('Authentication successful. Server online')
		logged_in=True


# ----- SEND TO CLIENT -----
def send_to(client,subject,body):
	log('Sending message to '+client)
	msg = MIMEMultipart()
	msg['From'] = USER
	msg['To'] = client
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	s.sendmail(USER,client,text)
	log('Message sent')
# ----- END SEND -----

# ----- RECIEVE FROM -----
def get_latest():
	server.select("Inbox")
	result, data = server.search(None, "ALL")
	ids = data[0]
	id_list = ids.split()
	latest_email_id = id_list[-1]
	result, data = server.fetch(latest_email_id, "(RFC822)")
	return data[0][1]

def strip_email(raw_message):
	useful_info=[]
	for x in email.message_from_string(raw_message).walk():
		if x.get_content_type() == 'text/plain':
			useful_info.append(x.get_payload())
	return useful_info[0]

def get_sender(raw_message):
	sender_info=[]
	lines=raw_message.split('\r\n')
	for x in lines:
		if 'From:' in x:
			sender_info.append(x.split(':')[1])
	return sender_info[0]

def get_subject(raw_message):
	subject=[]
	lines=raw_message.split('\r\n')
	for x in lines:
		if 'Subject:' in x:
			subject.append(x.split(':')[1])
	return subject[0]
# ----- END RECIEVE FROM -----

def main():
	login()
	last=get_latest()
	log('Waiting for new msg')
	while True:
		new = get_latest()
		if new != last:
			sender=get_sender(new)
			subject=get_subject(new)
			plain_text=strip_email(new)
			log('Message from '+sender+'\n     Content:\n               '+plain_text+'\n     ')
			return {'sender':sender,'subject':subject,'msg':plain_text}			

