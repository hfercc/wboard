from django.test.client import Client
import os
os.sys.path += ['../']
	
def cls():
	i = os.system('cls')

def set_path(path):
	global url_path
	url_path = str(path)
	
def set_arg(key, value):
	args[str(key)] = eval(value)
	
def del_arg(key):
	del args[key]
	
def get():
	global response
	response = client.get(url_path, args)
	print_response()
	
def post():
	global response
	response = client.post(url_path, args)
	print_response()
	
def login(username, password):
	client.login(username = username, password = password)
	
def logout():
	client.logout()
	
def show():
	print 'Path: ', url_path
	print 'Args: '
	for k, v in args.iteritems():
		print '%.10s %s' % (k,v)
		
def print_response():
	print 'STATUS_CODE: ', response.status_code
	print 'CONTENT:'
	print response.content
	
def file(key, fname):
	args[key] = open(eval(fname), 'r')

menus = {'get': get,
				 'post': post,
				 'cls': cls,
				 'path': set_path,
				 'set': set_arg,
				 'del': del_arg,
				 'login': login,
				 'logout': logout,
				 'show': show,
				 'file': file,
				}

def main():		
	global url_path, args, client, response
	url_path = ''
	args = {}
	client = Client()
	response = None
	while True:
		login('superuser', 'superuser')
		cmd_list = raw_input('test> ').split()
		try:
			sub_cmd = cmd_list[0]
			#print cmd_list
			if sub_cmd == 'exit':
				break
			del cmd_list[0]
			menus[sub_cmd](*cmd_list)
		except Exception, e:
			print 'ERROR: %s' % e
	