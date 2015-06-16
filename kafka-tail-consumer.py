#!/usr/bin/env python

# Kim Ngo
# June 16, 2015
#
# kafka consumer that reads comma delimmited messages: timestamp, user, URL
# creates a directory and appropriate user log files to append message to
# metadata is appended to kafka-tail.log file
# -- to be ran with kafka-tail-producer.py

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from optparse import OptionParser
import subprocess
import atexit
import re,os,sys,os.path

METADATA_LOG = 'kafka-tail.log'
USER = 1

class Consumer():#threading.Thread):
	daemon = True

	def __init__(self,options):
		self.host = options.host
		self.port = int(options.port)
		self.topic = options.topic
		self.group = options.group
		self.directory = options.directory

		self.create_log_directory()
		self.create_log_file()

	def create_log_file(self):
		if not os.path.isfile(METADATA_LOG):
			cmd = 'touch ' + METADATA_LOG
			os.system(cmd)

	def create_log_directory(self):
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

	def run(self):
		client = KafkaClient(self.host + ':' + str(self.port))
		consumer = SimpleConsumer(client, self.group, self.topic,
			max_buffer_size = None,
		)

		try:
			for message in consumer:
				# Handles metadata messages and appends to kafka-tail log file
				if re.search("::", message.message.value) != None:
					cmd = 'echo \"' + message.message.value + '\" >> ' + METADATA_LOG
					os.system(cmd)

				# Handles csv messages and appends to appropriate log file
				else:
					print message.message.value
					data =  message.message.value.split(',')
					user_log_file = self.directory + '/' + data[USER] + '.csv'
					if not os.path.isfile(user_log_file):
						cmd = 'touch ' + user_log_file
						os.system(cmd)
					cmd = 'echo \"' + message.message.value + '\" >> ' + user_log_file
					os.system(cmd)
		except KeyboardInterrupt,e:
			pass


def main():
	parser = OptionParser(usage="""
	%prog -d <output dir> -s <kafka-server> -p <kafka-port> [other-options]
	Tails a log file continously, sending log lines to a kafka topic as messages and supporting log rotation. Optionally,
	prepend a "metadata" string to each log line (kafka message will contain the string <metadata>:<log-line>).
	set -d for the directory name of output log files--default 'logs'.
	set -s and -p to set the kafka server--default localhost:9092
	set -t <topic> to set the kafka topic to listen to
	Simple batching is supported (use -b to choose the batch size, default is 10).
	Advanced: If needed, use -d <delay> in order to control the tail delay - Unneeded in almost all cases.
	NOTE: Currently expects kafka/ module to be in a folder parallel to this script.
""")
	parser.add_option("-s","--host",dest="host",default="localhost",
	                help="kafka host")
	parser.add_option("-p","--port",dest="port",default="9092",
	                help="kafka port")
	parser.add_option("-t","--topic",dest="topic",default=None,
	                help="REQUIRED: Topic to listen to")
	parser.add_option("-g", "--group",dest="group",default=None,
									help="REQUIRED: consumer group")
	parser.add_option("-d","--output-directory",dest="directory",default='logs',
	                help="output directory")
	
	(options,args) = parser.parse_args()
	
	if options.topic is None or options.group is None:
		parser.print_help()
		sys.exit(1)

	c = Consumer(options)
	c.run()
	#c.start()

if __name__ == "__main__":
	main()
