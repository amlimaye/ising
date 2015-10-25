class MetropolisLogger:
	def __init__(self,filename,keys,fmtstring=None):
		#open file handle to filename
		self.file = open(filename,'r')

		#store keylist
		self.keys = keys
		self.keys.insert(0,'num')

		#store format, if none default to all keys floats
		if fmt == None:
			self.fmtstring = '%8d,'.join(['%0.8f,' for _ in self.keys])
			self.fmtstring[-1] = '\n'
		else:
			self.fmtstring = fmt
		if len(self.fmtstring.split()) != len(self.keys):
			raise ValueError('Must have identical number of keys and '
							 'substitutions in format string')

		#construct header
		self.header = ''.join([str(key) for key in self.keys])
		self.header[-1] = '\n'

		#write header to logfile
		self.file.write('%s' % (self.header))

	def __del__(self):
		self.file.close()

	def write_log(self,logdict,num=0):
		#construct string for logfile entry
		logargs = self.num + tuple([logdict[key] for key in self.keys])
		self.file.write(self.fmtstring % logargs)