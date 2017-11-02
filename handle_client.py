from main import log
from mailer import send_to

known_clients={}

def words_only(msg):
	sifted=''
	acceptable='abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	for x in list(msg):
		if x in list(acceptable):
			sifted=sifted+x
	return sifted.split(' ')

def detect_name(msg):
	name=''
	ignore=['my','name','is','yes','hi','oh','it','its']
	words = words_only(msg)
	for x in words:
		x=x.lower()
		if x not in ignore:
			name=name+' '+x
	return name

def detect_yes(msg):
	yes=['yes','yea','yup','mhm']
	for x in msg.split(' '):
		x=x.lower()
		if x in yes:
			return True

step1=[]
def whos_this(sender):
		send_to(sender,'','whos this')
		step1.append(sender)

def main(sender_dict):
	client=sender_dict['sender']
	msg=sender_dict['msg']
	if client not in known_clients:
		if sender not in step1:
			whos_this()
		else:
			name=detect_name()






