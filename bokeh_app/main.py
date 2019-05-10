# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.histogram import histogram_tab

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# read and clean data
df = pd.read_csv('bokeh_app/data/African_Studies_Journal_Review_Project_Database.csv', header=0,encoding = 'unicode_escape') 
cleaned_df = df.iloc[:,[0]+list(range(19,140))]
cleaned_df = cleaned_df.dropna()
cleaned_df.iloc[:,range(21,115)] = cleaned_df.iloc[:,range(21,115)].astype(int)
data = cleaned_df.iloc[:,[0,7]+list(range(21,115))]


# Create each of the tabs
tab1 = histogram_tab(data)
# tab2 = density_tab(flights)
# tab3 = table_tab(data)
# tab4 = map_tab(map_data, states)
# tab5 = route_tab(flights)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1])

# Put the tabs in the current document for display
curdoc().add_root(tabs)


