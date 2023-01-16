#the function to transform the aspx file to a csv file
def create_dataframe(File_name):
    import os
    import sys
    import pandas as pd
    from bs4 import BeautifulSoup

    path = '/work/Dataset/'+File_name

    # empty list
    data = []

    # for getting the header from
    # the HTML file
    list_header = []
    soup = BeautifulSoup(open(path),'html.parser')
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    # Storing the data into Pandas
    # DataFrame
    dataFrame = pd.DataFrame(data = data, columns = list_header)
    dataFrame.drop(dataFrame.columns[[0,7]], axis=1, inplace=True)
    dataFrame.columns=['date','closing','adjusted','evolution','quantity','volume']
    dataFrame=dataFrame.apply(lambda x: x.str.replace(',','.'))
    dataFrame=dataFrame.apply(lambda x: x.str.replace('\n',''))
    dataFrame['closing']=dataFrame['closing'].astype('float')
    dataFrame['adjusted']=dataFrame['adjusted'].astype('float')
    dataFrame['evolution']=dataFrame['evolution'].astype('float')
    dataFrame['quantity']=dataFrame['quantity'].astype('float')
    dataFrame['volume']=dataFrame['volume'].astype('float')
    dataFrame['date']= pd.to_datetime(dataFrame['date'])
    dataFrame=dataFrame.sort_values('date')
    dataFrame=dataFrame.reset_index()
    dataFrame=dataFrame.drop('index',axis=1)
    
    return dataFrame

#the function that creates the graph :
import plotly.graph_objects as go
from plotly.subplots import make_subplots
def plot_graph():
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces(the price graph)
    fig.add_trace(go.Scatter(x=data['date'], y=data['closing'], name="closing price"),secondary_y=False,)
    
    #add the volume graph
    fig.add_trace(
        go.Bar(x=data['date'], y=data['volume'],name='volume'),
        secondary_y=True,
    )
    #change the size of the figure
    fig.update_layout(
        autosize=False,
        width=900,
        height=500,paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Price</b>", secondary_y=False,autorange=False)
    fig.update_yaxes(title_text="<b>Volume</b>", secondary_y=True)
    fig.update_yaxes(range=[50,1600], secondary_y=False)
    fig.show()

#The functions that return the max and min for some columns

def return_max(data):
    return max(data['closing'])
def return_min(data):
    return min(data['closing'])
def volume_max(data):
    return max(data['volume'])
def quantity_max(data):
    return max(data['quantity'])