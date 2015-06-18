#!/usr/bin/env python

# Kim Ngo
# June 18, 2015
#
#

from bokeh.plotting import figure, output_file, show
import sys, os.path

TIME,USER,URL = range(3)

class Data():
	def __init__(self):
		self.x = list()
		self.y = list()

def main():
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " [input file]"
		sys.exit(1)

	input_file = sys.argv[1]
	if not os.path.isfile(input_file):
		print "ERROR: Cannot find " + input_file
		sys.exit(1)

	d = Data()
	with open(input_file) as f:
		for line in f:
			split = line.split(',')
			d.x.append(split[TIME])
			d.y.append(split[URL])

	# Output to static HTML file
	output_file("lines.html", title="testing plot")

	# Create a new plot with a title and axis lablels
	p = figure(title="testing", x_axis_label="Time", y_axis_label="URL")

	# Add a line renderer with legend and line thickness
	p.line(d.x, d.y, line_width=2)

	# Show the results
	show(p)

if __name__ == "__main__":
	main()
