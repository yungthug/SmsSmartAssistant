import handle_client as handle

#global console logging can be tweaked here.
def log(data):
	print "[LOG]: "+str(data)+" ..."

# ----- MAILER IMPORTS -----
import mailer as m
get_msg=m.main #() returns: {'msg','sender','subject'}
send_to=m.send_to #('client','subject','body')
# ----- END MAILER -----

while True:
	client_dict = get_msg()
	print client_dict
	send_to(client_dict['sender'],'',client_dict['msg'])