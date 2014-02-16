from sae import kvdb
from sae import channel

kv = kvdb.KVClient()

class ChannelKV(object):
	
	def __init__(self, user_id):
		self.__list = None
		self.__id   = str(user_id)
		kv.set(self.__id, '')
		
	def get_list(self):
		if self.__list is None:
			self.__list = [int(i) for i in kv.get(self.__id).split()]
		return self.__list
		
	def get_name_list(self):
		return ['%s___%d' % (self.__id, i) for i in self.get_list()]
		
	def get_min(self):
		i = 0
		while i in self.get_list():
			i+=1
		return i
		
	def add(self):
		i = self.get_min()
		self.__list += [i]
		return i
		
	def add_and_get_url(self):
		i = self.add()
		return channel.create_channel('%s___%d' % (self.__id, i), 60*60*24*2)
		
	def delete(self, index):
		l = self.get_list()
		if index in l:
			self.__list.remove(index)
			
	def save(self):
		kv.set(self.__id, ' '.join(map(str, self.get_list()))
		
	def __del__(self):
		self.save()
		
def del_url(url):
	id, i = url.split("___")
	ChannelKV(id).delete(i)
	
def send_all(id, msg):
	kv = ChannelKV(id)
	for name in kv.get_name_list():
		channel.send_message(name, msg)