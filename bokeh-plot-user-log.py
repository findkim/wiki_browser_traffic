#!/usr/bin/env python

# Kim Ngo
# June 18, 2015
#
# Reads username.log file with the format: Timestamp, URL
# Plots time vs. page visited

import pandas as pd
from bokeh.plotting import figure, output_file, show
import sys, os.path
#import datetime
import re

HTML_EXTENSION = '.html'

# Truncates URL--Replaces + with ' ' and extracts page title 
def truncate_URL(url):
	return re.sub('\+', ' ', re.sub('.*\/', '', url))

def main():
	if len(sys.argv) < 2:
		print("Usage: " + sys.argv[0] + " [input file]")
		sys.exit(1)

	input_file = sys.argv[1]
	if not os.path.isfile(input_file):
		print("ERROR: Cannot find " + input_file)
		sys.exit(1)

	# Read input file
	data = pd.read_csv(input_file, header=None, names=['Date', 'URL'], parse_dates=['Date'])

	# Clean up data
	data['URL'] = data['URL'].apply(truncate_URL)

	# Output to static HTML file
	user = input_file.split('.') # Removes log file extension
	output_file(user[0]+HTML_EXTENSION)
	
	# Create a new plot with a title and axis lablels
	p = figure(title=user[0],
							x_axis_type="datetime",
							y_range=list(set(data.URL)),
							x_axis_label='Timestamp',
							y_axis_label='Page Title',
							plot_width=800
						)
	p.circle(list(data.Date), list(data.URL))

	# Show the results
	show(p)

if __name__ == "__main__":
	main()
