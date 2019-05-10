# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis, FactorRange)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
import colorcet as cc

# Make plot with histogram and return tab
def histogram_tab(data):

	# Function to make a dataset for histogram based on a list of journals,
	def make_dataset(topic_list):

		# Dataframe to hold information
		sum_table=data.groupby('Journal').sum()
		sum_table['Journal']=['AA','ASR','JMAS']

		table = sum_table[topic_list]
		new_table = pd.melt(table,var_name='topics',value_name = 'count')
		journal = ["AA","ASR","JMAS"]*len(topic_list)
		new_table['Journal'] = journal

		grouped = new_table.groupby(['topics','Journal'])
		x = [name for name,group in grouped]
		counts = new_table.groupby(['topics','Journal'])['count'].sum().values

		source = ColumnDataSource(data=dict(x=x, counts=counts))
		p = figure(x_range=FactorRange(*x), plot_height=250, title="Topics Break Down by Year")
		return source,p


	def style(p):
		# Title 
		p.title.align = 'center'
		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

		# Axis titles
		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		# Tick labels
		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		return p
	
	def make_plot(src,p):
		journal = ["AA","ASR","JMAS"]
		
		palette = [cc.rainbow[i*15] for i in range(17)]
		p.vbar(x='x', top='counts', width=0.9, source=src,fill_color=factor_cmap('x', palette=palette, factors=journal, start=1, end=2))

		p.y_range.start = 0
		p.x_range.range_padding = 0.1
		p.xaxis.major_label_orientation = 1
		p.xgrid.grid_line_color = None
		hover = HoverTool()
		hover.tooltips = [("count","@counts")]

		hover.mode = 'vline'

		p.add_tools(hover)

		# Styling
		p = style(p)

		return p
	
	
	
	def update(attr, old, new):
		topics_to_plot = [topic_selection.labels[i] for i in topic_selection.active]
		
		new_src,p = make_dataset(topics_to_plot)
		src.data.update(new_src.data)
		
	# Carriers and colors
	available_topics = ["topics_domestic_politics","topics_international_relations", "topics_society","topics_econ"]
		
	topic_selection = CheckboxGroup(labels=available_topics, 
									  active = [0, 1,2,3])
	topic_selection.on_change('active', update)
	
	# Initial carriers and data source
	initial_topics = [topic_selection.labels[i] for i in topic_selection.active]
	
	src,p = make_dataset(initial_topics)
	p = make_plot(src,p)
	
	# Put controls in a single element
	controls = WidgetBox(topic_selection)
	
	# Create a row layout
	layout = row(controls, p)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'Histogram')

	return tab