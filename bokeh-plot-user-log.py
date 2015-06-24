#!/usr/bin/env python

# Kim Ngo
# June 18, 2015
#
# Reads username.log file with the format: Timestamp, URL
# Plots time vs. page visited

import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.models.tools import (WheelZoomTool, PanTool,BoxZoomTool,ResetTool,ResizeTool)
import sys, os.path
import re

Y_AXIS_LABEL = "xdata.proxy\nWiki Page"
HTML_EXTENSION = '.html'


### Bokeh tools ###

hover = HoverTool(
	tooltips = [
		("Timestamp", "@TS"),
		("Wiki page", "$y"),
	]
)
box = BoxZoomTool(dimensions = ["width","y"])
pan = PanTool(dimensions = ["width","y"])
zoom = WheelZoomTool(dimensions = ["width","y"])
TOOLS = [hover, box, zoom, pan, ResizeTool(), ResetTool()]

### End tools ###



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
	data['TS'] = data.Date.map(lambda x: x.strftime('%m/%d/%Y %H:%M:%S')) # Used for HoverTool.tooltips

	source = ColumnDataSource(data)

	# Output to static HTML file
	no_ext = re.sub('\..*', '', input_file) # Removes log file extension
	path = re.sub('\/.*', '/', no_ext) # Extracts file path
	user = re.sub('.*\/', '', no_ext) # Extracts user
	output_file(path+user+HTML_EXTENSION)
	
	# Create a new plot with a title and axis lablels
	p = figure(title=user,
							x_axis_type="datetime",
							y_range=list(set(data.URL)),
							x_axis_label='Timestamp',
							y_axis_label=Y_AXIS_LABEL,
							plot_width=800,
							plot_height=200+(len(set(data.Date)))*10, # y-axis dynamic to URLS visited
							tools=TOOLS,
							toolbar_location="right"
						)
	p.scatter("Date","URL",source=source, size=10)

	# Show the results
	#show(p)

if __name__ == "__main__":
	main()
