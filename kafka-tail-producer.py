#!/usr/bin/env python

# Kim Ngo
# June 16, 2015
#
# kafka producer that watches a browser logfile and publishes GET requests as a comma delimmited message: timestamp, user, URL
# -- to be ran with kafka-tail-consumer.py
#
# Uses kafka-python: http://kafka-python.readthedocs.org/en/latest/index.html
# References: https://github.com/harelba/tail2kafka/blob/master/tail2kafka/tail2kafka
#							https://github.com/mumrah/kafka-python/blob/master/load_example.py

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from optparse import OptionParser
import subprocess
import re,os,sys

should_stop = False
pending_messages = []

class Producer():#threading.Thread):
	daemon = True

	# Initializes producer with commandline options
	def __init__(self,options):
		self.host = options.host
		self.port = options.port
		self.topic = options.topic
		self.logfile = options.logfile
		self.metadata = options.metadata
		self.batch_size = options.batch_size
		self.delay = options.delay
		self.pending_messages = []

	# Formats message to be sent to kafka
	def create_message_data(self,data):
		if self.metadata is not None:
			return "%s::%s" % (self.metadata, data)
		elif re.search("GET", data) != None:
			data = re.split('[ ,]', data)
			csv = data[0] + ' ' + data[1] + ',' + data[7] + ',' + data[9]
			return csv

	''' batch not currently working
	def flush_messages(self):
		global pending_messages
		print "flushing %d messages " % len(pending_messages)
		self.producer.send_messages(self.topic,pending_messages)
		pending_messages = []

	def send_to_kafka(self,message_text):
		global pending_messages
		pending_messages.append(message_text)
		if len(pending_messages) == self.batch_size:
			self.flush_messages(self.producer)
	'''

	def log_lines_generator(self, logfile, delay_between_iterations=None):
		global should_stop
		cmd = ['tail', '-n', '0', '-F']
		if delay_between_iterations is not None:
			cmd.append('-s')
			cmd.append(delay_between_iterations)
		cmd.append(logfile)
		process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=None)
		while not should_stop:
			line = process.stdout.readline().strip()
			yield line

	def run(self):
		self.client = KafkaClient(self.host + ':' + str(self.port))
		self.producer = SimpleProducer(self.client)

		try:
			for line in self.log_lines_generator(self.logfile):
				msg = self.create_message_data(line)
				self.producer.send_messages(self.topic, msg)

		except KeyboardInterrupt,e:
			pass

def main():
	parser = OptionParser(usage="""
	%prog -l <log-file> -t <kafka-topic> -s <kafka-server> -p <kafka-port> [other-options]
	Tails a log file continously, sending log lines to a kafka topic as messages and supporting log rotation. Optionally,
	prepend a "metadata" string to each log line (kafka message will contain the string <metadata>:<log-line>).
	set -l to the log file to be tailed. The log tailing supports log rotation.
	set -s and -p to set the kafka server--default localhost:9092
	set -t <topic> to set the kafka topic to send
	""")
#	Simple batching is supported (use -b to choose the batch size, default is 10).
#	Advanced: If needed, use -d <delay> in order to control the tail delay - Unneeded in almost all cases.
#	NOTE: Currently expects kafka/ module to be in a folder parallel to this script.
#""")
	parser.add_option("-s","--host",dest="host",default="localhost",
	                help="kafka host")
	parser.add_option("-p","--port",dest="port",default="9092",
	                help="kafka port")
	parser.add_option("-t","--topic",dest="topic",default=None,
	                help="REQUIRED: Topic to send to")
	parser.add_option("-l","--log-file",dest="logfile",default=None,
	                help="REQUIRED: Log file to tail")
	parser.add_option("-m","--metadata",dest="metadata",default=None,
	                help="REQUIRED: metadata tag to send along with the data")
#	parser.add_option("-b","--batch-size",dest="batch_size",default="10",
#	                help="Size of message batches")
#	parser.add_option("-d","--delay",dest="delay",default=None,
#	                help="tail delay between iterations")
	
	(options,args) = parser.parse_args()
	
	if options.topic is None or options.logfile is None:
		parser.print_help()
		sys.exit(1)

	p = Producer(options)
	p.run()


if __name__ == "__main__":
	
	# DEBUG
	#logging.basicConfig(
	#	format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
	#	level=logging.DEBUG
	#	)
	main()
