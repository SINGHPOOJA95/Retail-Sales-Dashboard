from flask import Flask,render_template
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

app= Flask(__name__)
@app.route('/')
def index():
    data=pd.read_excel("Retail-Supply-Chain-Sales-Dataset.xlsx")
  
    products=data.groupby('Product Name')[['Sales','Profit']].sum().reset_index()
    fig=px.scatter(products, x=products['Sales'],y=products['Profit'],hover_data=['Product Name'])

    fig.update_layout(
    
    paper_bgcolor="#b3cbd3",
    
    
    title_font_size=24)

    fig.update_traces(
       marker_color="#B179C7"
    )
    fig.show()


    
    discount_profit_impact=data.groupby('Discount')['Profit'].median().reset_index()
    fig_1=px.line(discount_profit_impact,x='Discount',y='Profit')
    fig_1.update_layout(
       paper_bgcolor="#b3cbd3",
    )

    fig_1.update_traces(
       
       marker_color="#172384"
       
       
    )
    fig_1.show()
   
    
    region_performance=data.groupby(['Region','City'])[['Sales','Profit']].sum().reset_index()
    fig_2=px.bar(region_performance, x='Region' ,y=['Sales','Profit'],barmode='group')
   
    fig_2.update_layout(
      paper_bgcolor="#b3cbd3",
   )
    fig_2.data[0].marker.color="#6ea7bc"
    fig_2.data[1].marker.color="#e1d557"
    fig_2.update_traces(
       marker_line_width=0
    )
    fig_2.show()

    data['delivery_time']= data['Ship Date']-data['Order Date']
    data=data.sort_values('delivery_time')
    data['delivery_time']=data['delivery_time'].dt.days
    Delay_delivery=data[data['delivery_time']>10]

    Region_wise_delay=Delay_delivery.groupby(['Ship Mode','Region']).size().reset_index(name='delivery_time')
    fig_3=px.bar(Region_wise_delay, x='Region', y='delivery_time',color='Ship Mode',color_discrete_map={
       'Standard Class':"#f56f97",
       'Second Class':"#f989aa",
       'First Class':"#f6a9c0",
       'Same Day':"#f9cbd9",
    })
    fig_3.update_layout(
        paper_bgcolor="#b3cbd3",
    )
    fig_3.show()
    
    segment=data.groupby('Segment')['Sales'].sum().reset_index()
    fig_4=px.pie(segment,names='Segment', values='Sales',color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_4.update_layout(
       paper_bgcolor="#b3cbd3"
    )
    
    fig_4.show()

    graph_html=fig.to_html(full_html=False)
    graph_html_1=fig_1.to_html(full_html=False)
    graph_html_2=fig_2.to_html(full_html=False)
    graph_html_3=fig_3.to_html(full_html=False)
    graph_html_4=fig_4.to_html(full_html=False)
    return render_template('index.html',graph_html=graph_html,graph_html_1=graph_html_1,graph_html_2=graph_html_2,graph_html_3=graph_html_3,graph_html_4=graph_html_4)
   


if __name__=="__main__":
  app.run(debug=True)
