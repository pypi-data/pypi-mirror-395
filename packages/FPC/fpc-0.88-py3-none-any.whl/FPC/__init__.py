import builtins,platform,time,math,os,urllib,sys,hashlib,json
from collections.abc import Iterable
from datetime import datetime
from urllib import request
dicts={}
IS_WIN=False if platform.system().find('Linux')>-1 else True
NOW=datetime.now()
NOW_TS=math.floor(NOW.timestamp())
NOW=NOW.strftime('%Y-%m-%d %H:%M:%S')
start_time=0
try:import requests as requests_
except ImportError:pass
else:
	class requests():
		def __init__(self, retry=3,headers={}, **kwargs):
			self.retry=retry if retry else 1
			self.session = requests_.Session()
			self.session.mount('http://', requests_.adapters.HTTPAdapter(max_retries=self.retry))
			self.session.mount('https://', requests_.adapters.HTTPAdapter(max_retries=self.retry))
			if headers.get('headers') is None:headers['User-Agent']= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
			self.session.headers.update(headers)
		def _meta(self,*args,**kwargs):
			for x in range(self.retry):
				try:
					return getattr(self.session,self._method)(*args,**kwargs)
				except Exception as e:
					if x==self.retry-1:raise e
					time.sleep(x+1)
		def __getattr__(self,name):
			if name in ['get','post','put','delete','patch','options','head']:
				self._method=name
				return self._meta
			else:
				return self.session
def is_numeric(x):
	try:float(x);return True
	except:return False
def now(x=None):#x='micro' return microsecond;x='str' return now time to string;x is number means convert timestamp to string;x is sting means convert string to timestamp
	if not x:return int(datetime.now().timestamp())
	elif x=='micro':return datetime.now().timestamp()
	elif x=='str':return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(x,(int,float)):return datetime.fromtimestamp(x if x <1e11 else x/1000).strftime('%Y-%m-%d %H:%M:%S')
	else:
		try:return int(datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timestamp())
		except:
			try: import dateutil.parser;return int(dateutil.parser.parse(x).timestamp())
			except Exception:
				import time_parser; return int(datetime.strptime(time_parser.parse_times(x),'%Y-%m-%d %H:%M:%S').timestamp())
_time=now
class interval_exec(object):#interval=FPC.interval_exec(10),interval()#运行10次执行一次,与时间无关
	def __init__(self,interval,now=True):
		self.interval=interval
		self.count=-1 if now else 0
	def __call__(self):
		self.count+=1
		return self.count%self.interval==0
def parse_time(_time):
	try:
		_time = _time.strip()
		later_time = {'d': 86400, 'h': 3600, 'm': 60}
		unit = _time[-1]
		if unit in later_time:
			_time = int(time.time()) + int(_time[:-1]) * later_time[unit]
		else:
			if _time.count(':')==1:_time+=':00'
			if ' ' in _time:
				if _time.count('-') == 0:
					_time = datetime.now().strftime('%Y-%m-') + _time
				elif _time.count('-') == 1:
					_time = datetime.now().strftime('%Y-') + _time
				_time = datetime.strptime(_time, '%Y-%m-%d %H:%M:%S').timestamp()
			else:
				_time = datetime.now().strftime('%Y-%m-%d ') + _time
				_time = datetime.strptime(_time, '%Y-%m-%d %H:%M:%S').timestamp()
				if _time < int(time.time()):
					_time += 86400
		return int(_time)
	except Exception as e:
		raise Exception(f'FPC.parse_time error,can not parse "{_time}"')
def print(*a,func=None,time='%m/%d %H:%M:%S',pretty=False,path=None,flush=False,debug=False,**s):
	if debug and 'debug' not in sys.argv:return
	a=list(a)
	if func:
		for i,x in enumerate(a):
			a[i]=func(x)
	if path:
		f=open(path,'w' if flush else 'a',encoding='utf-8')
		s['file']=f
	if time:
		builtins.print(datetime.now().strftime(time)+' : ',end='',**s)
	if pretty:
		import pprint
		if s.get('file'):s['stream']=s.pop('file')
		for x in a:
			pprint.pprint(x,sort_dicts=False,**s)
	else:
		builtins.print(*a,**s)
p=print
def pd(*a, **k):print(*a,pretty=True,time=None,**k);exit()
def log(*x,path=None,**s):#已经带有时间
	if path is None:
		path='d:/tmp/FPC.log' if IS_WIN else ('/tmp/FPC.log' if os.path.exists('/tmp') else './FPC.log')
	with open(path,'a',encoding='utf-8') as f:
		print(*x,file=f,**s)
def split_str(strs,num=1):
	_=[]
	for x in range(math.ceil(len(strs)/num)):
		_.append(strs[x*num:x*num+num])
	return _
def diff(a,b):
	diff={}
	for x in a:
		if b.get(x)!=a[x]: diff[x]=[a[x],b.get(x)]
	return diff
def notice(x,c='default',silent=None,channel=None,is_async=False,time=''):
	if is_async:
		process(notice,args=(x,c,silent,channel,False,time))
		return True
	if silent:
		red=redis()
		if red.exists(x if not channel else channel):return
		else:
			red.set(x if not channel else channel,'1',silent)
	try:
		with request.urlopen(f'http://call.ff2.pw/?{c}={urllib.parse.quote_plus(x)}&passwd=frank{("&time="+urllib.parse.quote_plus(str(time))) if time else "" }') :
			return True
	except Exception as e:
		print('FPC_notice_err:',e)
		return False
def interact(**argv):
	for k, v in argv.items():
		locals()[k] = v
	del k,v,argv
	while True:
		try:
			lines = []
			while True:
				line = input("... " if lines else ">>> ")
				if line.lower() == 'exit':
					return
				if not line and not lines:
					continue
				if not line:
					break
				if not lines and not line.endswith(':'):
					lines.append(line)
					break
				lines.append(line)
			if lines:
				code = '\n'.join(lines)
				if len(lines)==1:
					result = eval(code)
					result is None or builtins.print(result)
				else:
					exec(code)
		except Exception as e:
			builtins.print(f"err: {str(e)}")
def rand_sleep(i=0.4,a=0.8):import random;time.sleep(random.randint(int(i*1000),int(a*1000))/1000);
def rand(i=9,a=None):import random;return random.randint(int(i),int(a)) if a else random.randint(0,int(i-1));
def md5(x):hl = hashlib.md5();hl.update(x.encode('utf-8') if isinstance(x,str) else x);return hl.hexdigest();
def bin2hex(x):import binascii;return binascii.hexlify(x.encode('utf-8') if isinstance(x,str) else x);
def base64_encode(x):import base64;return base64.b64encode(x) if isinstance(x,bytes) else base64.b64encode(x.encode('utf-8'))
def base64_decode(x):import base64;return base64.b64decode(x+(b'===' if isinstance(x,bytes) else '==='))
def parse(o,attr_value=False):#print class/obj's attr beatiful
	method_list=[];attr_list=[]
	for x in dir(o):
		if x[:2] == '__':
			continue
		if callable(getattr(o, x)):
			method_list.append(x)
		else:
			attr_list.append(x)
	if attr_value:
		attr_dict = {x: getattr(o, x) for x in attr_list}
	return [method_list,attr_dict if attr_value else attr_list]
#save or open a python varible,callable obj and name and expire just for local
def obj(obj=None,remote=False,name:str|None =None,expire:str|int|None =None,is_json=False,path:str|None =None):#path优于name,remote模式无名字只保存一个对象
	if is_json:import json as pickle
	else:import pickle
	if remote:
		if obj is None:
			with request.urlopen(r'http://a.ff2.pw/obj.php') as f:
				return pickle.loads(f.read())
		else:
			with request.urlopen(r'http://a.ff2.pw/obj.php',pickle.dumps(obj)) as f:
				return True
	else:
		if path is None:
			os.path.exists('/tmp') or os.makedirs('/tmp')
			if name is None:
				path='/tmp/'+(sys.argv[0][sys.argv[0].replace('\\','/').rindex('/')+1:] if '/' in sys.argv[0] or '\\' in sys.argv[0] else sys.argv[0])+'.obj'
			else: path=f'/tmp/_named_{name}.obj'
		obj_callable=callable(obj)
		if obj is not None and not obj_callable:return pickle.dump(obj,open(path,'wb'))
		if os.path.exists(path):
			expire=int(expire[:-1])*{'s':1,'m':60,'h':3600,'d':86400}[expire[-1]] if isinstance(expire,str) else expire
			if expire and NOW_TS-os.path.getmtime(path)>expire:
				if obj is None:
					os.remove(path)
			else:return pickle.load(open(path,'rb'))
		if obj_callable:
			data=obj()
			pickle.dump(data,open(path,'wb'))
			return data
		return None
def encrypt(string,password=None):
	if isinstance(string,bytes): string=string.decode('latin')
	first_letter=string[0]
	hl = hashlib.sha512()
	hl.update(first_letter.encode('utf-8')if password is None else password.encode('utf-8'))
	sha512=hl.digest()
	_= sha512[0]%64
	sha512=(sha512[_:]+sha512[:_])*math.ceil(len(string)/64)
	encrypted=''
	for i,x in enumerate(string):
		encrypted+=chr((ord(x)+sha512[i])%94+33)
	if password is None:
		encrypted=chr((ord(first_letter)+ord(encrypted[-1]))%94+33)+encrypted[1:]
	return encrypted
def decrypt(string,password=None):
	hl = hashlib.sha512()
	if password is None:
		for i in range(6):
			_=94*i+ord(string[0])-(ord(string[-1])+33)
			if _ >=33 and _<127:break
		first_letter=chr(_)
	hl.update(first_letter.encode('utf-8')if password is None else password.encode('utf-8'))
	sha512=hl.digest()
	_= sha512[0]%64
	sha512=(sha512[_:]+sha512[:_])*math.ceil(len(string)/64)
	decrypted=''
	for i,x in enumerate(string):
		for ii in range(6):
			_=94*ii+ord(x)-(sha512[i]+33)
			if _ >=33 and _<127:break
		decrypted+=chr(_)
	if password is None:
		decrypted=first_letter+decrypted[1:]
	return decrypted
def start():
	global start_time
	start_time=now('micro')
def end(_type=True):#True:print False:return number:sleep(number)
	if _type is True : print(now('micro')-start_time)
	elif _type is False:return now('micro')-start_time
	elif isinstance(_type,(int,float)):
		_=_type-(now('micro')-start_time)
		_>0 and time.sleep(_)
def coin_price(coins:Iterable[str]):
	coins_str=coins if isinstance(coins,str) else ','.join(coins)
	with request.urlopen(f'http://a.ff2.pw/coin_price.php?coin={coins_str}') as f:
		res=json.loads(f.read())
		return res[coins_str] if isinstance(coins,str) else res
def sort(a=Iterable,key=None,reverse=False):#dict[key:value]:when key==True short by key,when key is None short by value,otherotherwise short by value[key],
	if isinstance(a,dict):
		return dict(sorted(a.items(), key=((lambda x: x[0]) if key is True else (lambda x: x[1][key])) if key else lambda x: x[1], reverse=reverse))
	elif isinstance(a,str):
		return sorted(a,reverse=reverse)
	else:
		return sorted(a, key=None if key is None else lambda x: x[key], reverse=reverse)
def pretty(data):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                processed_first = pretty(value[0])
                result[key] = [processed_first]
            elif isinstance(value, list) and len(value) == 0:
                result[key] = []
            else:
                result[key] = pretty(value)
        return result
    elif isinstance(data, list):
        if len(data) > 0:
            processed_first = pretty(data[0])
            return [processed_first]
        else:
            return []
    else:
        return data
class mysql(object):
	conn=None
	def __init__(self, host=None,port=3306,threadsafe=False,sync=False,**args):
		import pymysql
		self.pymysql=pymysql
		if threadsafe:
			from threading import Lock
			self.lock=Lock()
		else:self.lock=None
		if host is not None and host.startswith('sqlite'):
			import sqlite3
			self.conn=sqlite3.connect('/tmp/sqlite.db' if ':' not in host else host[host.index(':')+1:] ,isolation_level=None)
			self.conn.row_factory = sqlite3.Row
			if 'table' in args : self.table=args['table']
			return
		if args.get('ssh_host'):
			import sshtunnel
			sshtunnel.DAEMON=True
			sshtunnel.SSHTunnelForwarder.daemon_forward_servers=True
			sshtunnel.SSHTunnelForwarder.daemon_transport=True
			self.server = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=args.pop('ssh_host'),ssh_username=args.pop('ssh_username'),ssh_password=args.pop('ssh_password'),remote_bind_address=('127.0.0.1' if host is None else host,port))
			self.server.start()
			port=self.server.local_bind_port
		connect_config={'host':'127.0.0.1' if host is None else host,'port':port,'user':'root','password':'','db':'localhost','cursorclass':pymysql.cursors.DictCursor,'autocommit':None}
		if 'table' in args:
			self.table=args['table']
			del args['table']
		if not args:
			args=obj(name='mysql' if host is None else f'mysql_{host}')
		for x in args:# type: ignore
			connect_config[x]=args[x] # type: ignore
		self.connect_config = connect_config
		sync and self.__init_connect__()
	def __init_connect__(self):
		for x in range(3 if IS_WIN else 1):
			try:
				self.conn = self.pymysql.connect(**self.connect_config)
				break
			except self.pymysql.err.OperationalError as e:
				continue
		else:
			raise e
	def __getattr__(self,attr):
		return getattr(self.conn,attr)
	def _decide_type(self,value):
		if isinstance(value,(int,float)):
			pass
		elif isinstance(value,bytes):
			value=value.decode('utf-8')
		elif value is None:
			value='NULL'
		else:
			value='"'+self.pymysql.converters.escape_string(str(value))+'"'
		return value
	def _split_dict(self,dicts,splitor=','):
		string=''
		for field in dicts:
			if isinstance(dicts[field],(list,tuple)):
				operator= dicts[field][0].upper()
				if 'IN' in operator:
					value=''
					for in_value in dicts[field][1]:
						value+=f'{self._decide_type(in_value)},'
					value=value[:-1]
					string+=f' `{field}` {operator} ({value}) {splitor}'
				elif 'BETWEEN' in operator:
					value=[self._decide_type(dicts[field][1][0]),self._decide_type(dicts[field][1][1])]
					string+=f' `{field}` {operator} {value[0]} and {value[1]} {splitor}'
				else:
					value=self._decide_type(dicts[field][1])
					string+=f' `{field}` {operator} {value} {splitor}'
			else:
				value=self._decide_type(dicts[field])
				string+=f' `{field}`={value} {splitor}'
		return string[:-len(splitor)]
	def _split_add_dict(self,dicts):
		key=value=''
		for x in dicts:
			key+=r'`%s`,'%x
			if dicts[x] is None:value+='null,'
			else:value+=r'%s,'%(dicts[x]) if is_numeric(dicts[x]) else r'"%s",'%(self.pymysql.converters.escape_string(str(dicts[x])))
		return key[:-1],value[:-1]
	def execute(self,strs,is_query=None):
		if not self.conn:self.__init_connect__()
		strs=strs.strip()
		op_type=strs[:4].lower()
		is_query = True if op_type in ['sele','show','desc','with'] or is_query else False
		for x in range(3):
			try:
				cur=None
				if self.lock:self.lock.acquire(timeout=10)
				cur=self.conn.cursor()
				cur.execute(strs)
				if is_query:
					data=cur.fetchall()
				elif op_type in ['upda','dele']:
					data=cur.rowcount
				else:
					data=cur.lastrowid
				return data
			except Exception as e:
				if '2006' in str(e) or '2013' in str(e) or isinstance(e,self.pymysql.err.InterfaceError):
					if self.conn:
						self.conn.close();self.conn=None;
						self.__init_connect__()
				else:
					e.args=e.args+(f' FPC_SQL:{strs}',)
					raise e
			finally:
				if cur:cur.close()
				if self.lock:self.lock.release()
		# is_query or self.conn.commit()
		raise Exception('FPC.mysql:try 3 times connect,but error')
	def add(self,dicts,table=None,ignore=False,duplicate=[]):
		'''table is optional,dicts can be list or dict,duplicate should be list as field names you want to update'''
		if not isinstance(table,str):
			if table is None:
				table=self.table
			else:#table is not none and reverse two args
				table_=dicts
				dicts=table
				table=table_
		if not dicts:return
		if isinstance(dicts,dict): dicts=[dicts]
		values=''#values like (1,2),(2,3) 
		for x in dicts:
			key,value=self._split_add_dict(x)
			values+=r'(%s),'%(value)
		ignore='' if not ignore else 'ignore'
		duplicate_str=''
		if duplicate:
			duplicate_str='as a on duplicate key update '
			for x in duplicate:
				duplicate_str+=f' `{x}`=a.`{x}`,'
			duplicate_str=duplicate_str[:-1]
		return self.execute(f''' insert {ignore} into `{table}`({key}) values {values[:-1]} {duplicate_str}''')
	def update(self,data,where,table=None):
		'''where can be str or dict'''
		table=self.table if table is None else table
		where=self._split_dict(where,'and') if isinstance(where,dict) else where
		data=self._split_dict(data)
		return self.execute(r' update `%s` set %s where %s'%(table,data,where))
	def delete(self,where,table=None,where_splitor='and'):
		where=self._split_dict(where,where_splitor) if isinstance(where,dict) else where
		return self.execute(r' delete from `%s` where %s'%(table,where))
	def select(self,where=None,table=None,where_splitor='and',field='*',order=None,limit=None):
		table=self.table if table is None else table
		query_str=f'select {field} from {table} '
		if where:
			where=self._split_dict(where,where_splitor) if isinstance(where,dict) else where
			query_str+=f'where {where} '
		if order:
			query_str+=f'order by {order} '
		if limit:
			query_str+=f'limit {limit} '
		return self.execute(query_str)
	def find(self,*args,**argv):
		# if 'order' not in argv : argv['order']='id desc'
		res=self.select(*args,**argv,limit=1)
		return res and (res[0][list(res[0].keys())[0]] if len(res[0])==1 else res[0])
class redis(object):
	server=False
	def __init__(self,host='127.0.0.1',db=0,port=6379,ssh_host=None,ssh_username='root',ssh_password=None):
		import redis
		if ssh_host:
			import sshtunnel
			sshtunnel.DAEMON=True
			sshtunnel.SSHTunnelForwarder.daemon_forward_servers=True
			sshtunnel.SSHTunnelForwarder.daemon_transport=True
			self.server = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=ssh_host,ssh_username=ssh_username,ssh_password=ssh_password,remote_bind_address=(host,port))
			self.server.start()
			port=self.server.local_bind_port
		self.redis=redis.StrictRedis(host=host, port=port, db=db,decode_responses=True)
	def __getattr__(self,attr):
		return getattr(self.redis,attr)
def process_arg_construct(urls:list,args):#args must be iterable
	proc_args=[]
	every_proc_count=math.ceil(len(args)/len(urls))
	for i,url in enumerate(urls):
		proc_args.append((url,args[i*every_proc_count:i*every_proc_count+every_proc_count]))
	return proc_args
def process(target,is_thread=True,join=False,num:int=1,sleep=None,daemon=False,**args):
	'''args:{
				'sync':True,
				'args':[('',),('',)]for mult proc,('','')for single proc the same parameter to multiple processes specified by num,
				'kwargs':[{'':''}]for mult proc,{'':''}like args,
			} or others that transfer to Thread or Process'''
	if isinstance(target,(str,list)):#args:target,[sync=True]
		import subprocess
		proc=subprocess.Popen(target,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True if isinstance(target,str) else False);
		return proc.communicate() if args.get('sync',True) else proc
	pros=[]
	if 'args' in args and 'kwargs' in args and 'kwargs' in args:
		_num=max(len(args['args'])if isinstance(args['args'],list)else 0,len(args['kwargs'])if isinstance(args['kwargs'],list)else 0)
		if num!=1 and num!=_num:
			raise ValueError(f'max args length is {_num} not equal to num:{num}')
		num=_num
	if 'args' in args:
		if isinstance(args['args'],tuple):
			args_list=[args['args']]*num 
		elif isinstance(args['args'],list):
			if num!=1 and num!=len(args['args']):
				raise ValueError('args length must be equal to num')
			args_list=args['args']
			num=len(args_list)
		else:
			raise ValueError('args must be tuple or list')
	if 'kwargs' in args:
		if isinstance(args['kwargs'],dict):
			kwargs_list=[args['kwargs']]*num 
		elif isinstance(args['kwargs'],list):
			if num!=1 and num!=len(args['kwargs']):
				raise ValueError('kwargs length must be equal to num')
			kwargs_list=args['kwargs']
			num=len(kwargs_list)
		else:
			raise ValueError('kwargs must be tuple or list')
	
	if is_thread: from threading import Thread as proc
	else: from multiprocessing import Process as proc
	for x in range(num):
		if 'args' in args:
			args['args']=args_list[x]
		if 'kwargs' in args:
			args['kwargs']=kwargs_list[x]
		pros.append(proc(target=target,**args))
		if daemon : pros[-1].daemon=True
		pros[-1].start()
		if sleep:time.sleep(sleep)
	if join:
		for x in range(num):
			_start = time.monotonic() if x == 0 else _start
			_remaining = None if join is True else max(0, join - (time.monotonic() - _start))
			pros[x].join(_remaining)
	return pros[0] if len(pros)==1 else pros
class ErrorCounter:
	def __init__(self,time_interval=60):
		from collections import deque
		self.error_timestamps = deque()
		self.time_interval=time_interval
	def add(self):
		current_time = time.time()
		self.error_timestamps.append(current_time)
	def count(self):
		current_time = time.time()
		while self.error_timestamps and self.error_timestamps[0] < current_time - self.time_interval:
			self.error_timestamps.popleft()
		return len(self.error_timestamps)
	def clear(self):
		self.error_timestamps.clear()