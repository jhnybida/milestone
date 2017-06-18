from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components 
import requests
import pandas as pd
import json
import datetime as dt

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    ticker = request.form['ticker']
    features = request.form.getlist('features')
    startdate = request.form['startdate']

    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % str(ticker) + '?api_key=' + 'wmEXswRBxQjWWQGo81H7'
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    datajs = raw_data.json()
    df = pd.DataFrame(datajs['data'])
    df.columns = datajs['column_names']

    df['dates'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    dates = df.loc[df.dates > (dt.datetime.now()-dt.timedelta(days=int(startdate)))].dates
    colors = {'Close':'red', 'Open':'blue', 'Adj. Close':'green', 'Adj. Open':'purple'}
    datestrs = {'1':'the last day', '7':'the last week','30':'the last month','365':'the last year','10000':'all time'}
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"

    plot = figure(tools = TOOLS,x_axis_type='datetime',x_axis_label='date',y_axis_label='price',plot_width=600, plot_height=600)
    for feature in features:
      plot.line(x = dates, y = df[feature], color = colors[feature], legend = feature)

    script,div = components(plot)
    return render_template('graph.html',ticker = ticker,startdate = datestrs[startdate],script=script, div=div)   

if __name__ == '__main__':
  app.run(port=33507)


