from main import log
def write_to(F,Data):
	try:
		File = open(F+'.txt','a')
		if Data not in read_from(F):
			File.write(Data+'\n')
		File.close()
		return True
	except Exception as E:
		log(E)

def read_from(F):
	D=open(F+'.txt','r').read().split('\n')
	return D