import os
import sys

class MetropolisLogger:
	def __init__(self,filename,keys,fmtstring=None):
		#open file handle to filename
		self.file = open(filename,'w')

		#store keylist
		self.keys = keys

		#store format, if none default to all keys floats
		if fmtstring == None:
			self.fmtstring = '%08d,'.join(['%0.8f,' for _ in self.keys])
			self.fmtstring = self.fmstring[0:-1]+'\n'
		else:
			self.fmtstring = fmtstring+'\n'

		print self.fmtstring.split()
		#len(self.keys)+1 is to account for iteration number prepended at start
		if len(self.fmtstring.split(',')) != len(self.keys)+1:
			raise ValueError('Must have identical number of keys and '
							 'substitutions in format string')

		#construct header
		self.header = ''.join([str(key) + ',' for key in self.keys])
		self.header = self.header[0:-1]+'\n'

		#write header to logfile
		self.file.write('%s' % (self.header))

	def __del__(self):
		self.file.close()

	def write_log(self,logdict,num=0):
		#construct string for logfile entry
		logargs = (num,) + tuple([logdict[key] for key in self.keys])
		self.file.write(self.fmtstring % logargs)