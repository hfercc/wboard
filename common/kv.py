from sae import kvdb,channel
from django.contrib.auth.models import User
import json
from wboard import settings
from datetime import datetime

kv = kvdb.KVClient()

#format [USER_ID]_[ID]_[Chat flag]

class ChannelKV(object):
	
	def __init__(self, user_id):
		self.__list = None
		if isinstance(user_id, User):
			self.__id = str(user_id.id)
			self.__user = user_id
		else:
			self.__id = str(user_id)
			self.__user = User.objects.get(id=int(self.__id))
		
	def get_list(self):
		if self.__list is None:
			strs = kv.get(self.__id)
			self.__list = {}
			if strs is None:
				strs = ''
			for i in strs.split():
				j, k = i.split('_')
				self.__list[int(j)] = k == 'c'
		print 'get_list:', self.__list
		return self.__list
		
	def get_name(self, l, index):
		if l[index]:
			c = 'c'
		else:
			c = ''
		return "%s_%d_%s" % (self.__id, index, c)
		
	def get_chat_list(self):
		l = self.get_list()
		return {i:l[i] for i in l if l[i]}
		
	def get_min(self):
		i = 0
		while i in self.get_list():
			i+=1
		return i
		
	def add(self, chat=False):
		i = self.get_min()
		c = 'c' if chat else ''
		self.__list[i] = chat
		self.save()        
		return channel.create_channel('%s_%d_%s' % (self.__id, i, c), 1440)
		
	def delete(self, name):
		l = self.get_list()
		print 'delete:',name, l
		index = int(name.split('_')[1])
		if index in l:
			del self.__list[index]
			self.save()            
			
	def save(self):
		str = []
		for i,j in self.get_list().iteritems():
			c = 'c' if j else ''
			str += ['%d_%s' %(i, c)]
		kv.set(self.__id, ' '.join(str))
		
	def __del__(self):
		self.save()

        
	def send(self, name, data):
		start = datetime.now()
		channel.send_message(name, data)
		end = datetime.now()
		return (end-start).seconds<3

	def send_unread(self, name = ''):
		n = reduce(lambda x,y:x+y, (getattr(self.__user, i).unread_notifications(self.__user).count() for i in ('commentnotification_set', 'statusnotification_set')))
		p = self.__user.private_message_received.filter(has_read=False).count()
		msg = json.dumps({'n':n, 'p':p})
		print 'send_unread', self.get_list()
		if not name:
			keys = self.get_list().keys()
			for i in keys:
				n = self.get_name(self.__list, i)            
				if n[-1] != 'c':
					if not self.send(n, msg):
						del self.__list[i]                    
						print i
		else:
			channel.send_message(name, msg)
			
	def send_message(self, msg):
		print 'send_message:' , self.get_chat_list()
		l = self.get_chat_list()        
		keys = l.keys()
		for i in keys:        
			if not self.send(self.get_name(l, i), json.dumps(msg)):
				del self.__list[i]            