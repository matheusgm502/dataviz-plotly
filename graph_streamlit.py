import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask, render_template

#Stocks
stocks = ['MGLU3.SA','PETR3.SA','VALE3.SA','ITSA3.SA']

#Dataframe
df = pd.DataFrame()
for stock in stocks:
    tick = yf.Ticker(stock)
    df[stock]=tick.history(start='2019-01-01', end='2022-12-01')['Open']
    df[stock+" Volume"]= tick.history(start='2019-01-01', end='2022-12-01')['Volume']

#Figure 1
fig = make_subplots(specs=[[{"secondary_y": True}]])

for stock in stocks:
    fig.add_trace(go.Scatter(x=df.index,y=df[stock].values, name=stock, mode='lines'))

for stock in stocks:
    fig.add_trace(go.Bar(x=df.index,y=df[stock+" Volume"].values, name=f'{stock} Volume'), secondary_y=True)

fig.update_yaxes(range=[0, 1000000000], secondary_y=True)

selector = [
    {'count':1,'label':'1m','step':'month','stepmode':'backward'},
    {'count':6,'label':'6m','step':'month','stepmode':'backward'},
    {'count':1,'label':'1y','step':'year','stepmode':'backward'},
    {'count':1,'label':'YTD','step':'year','stepmode':'todate'}
]

dropdown = [
    {'label':'All','method':'update','args':[
        {'visible':[True, True, True, True, False, False, False, False]}]},
    {'label':"MGLU3.SA",'method':"update", 'args':[{'visible': [True, False, False, False]}]},
    {'label':"PETR3.SA",'method':"update", 'args':[{'visible': [False, True, False, False]}]},
    {'label':"VALE3.SE",'method':"update", 'args':[{'visible': [False, False, True, False]}]},
    {'label':"ITSA3.SA",'method':"update", 'args':[{'visible': [False, False, False, True]}]}    
]

fig.update_layout(
    xaxis={'rangeselector':{'buttons':selector}},
    updatemenus = [{'buttons':dropdown,'xanchor':'left','x':-0.5}])

fig.update_layout(title='Preço de Abertura e Volume')

fig.data[4].visible=False
fig.data[5].visible=False
fig.data[6].visible=False
fig.data[7].visible=False

#Figure 2

stocks2 = ['MGLU3.SA','PETR3.SA','VALE3.SA','ITSA3.SA','BOVA11.SA']

df2 = pd.DataFrame()
for stock in stocks2:
    tick = yf.Ticker(stock)
    df2[stock]=tick.history(start='2019-01-01', end='2022-12-01')['Open']

chdf = df2.pct_change(periods=1)[1:]
chdf.head(2)

fig2 = go.Figure()

for stock in stocks:
    fig2.add_trace(go.Scatter(x=chdf[stock],y=chdf['BOVA11.SA'], mode='markers', name=stock))

dropdown = [
    {'label':'All','method':'update','args':[
        {'visible':[True, True, True, True]}]},
    {'label':"MGLU3.SA",'method':"update", 'args':[{'visible': [True, False, False, False]}]},
    {'label':"PETR3.SA",'method':"update", 'args':[{'visible': [False, True, False, False]}]},
    {'label':"VALE3.SE",'method':"update", 'args':[{'visible': [False, False, True, False]}]},
    {'label':"ITSA3.SA",'method':"update", 'args':[{'visible': [False, False, False, True]}]}  
]

fig2.update_layout(updatemenus = [{'buttons':dropdown,'xanchor':'left','x':-0.5}])

fig2.update_layout(title='Correlação de Retornos Diários com o BOVA11', xaxis_title='Retorno da Ação',yaxis_title='Retorno do BOVA11')

# Total Revenue

stocks3 = ['MGLU3.SA','PETR3.SA','VALE3.SA','ITSA3.SA']

df3 = pd.DataFrame()
for stock in stocks3:
    tick = yf.Ticker(stock)
    df3[stock]=tick.income_stmt.T['Total Revenue']

fig3 = go.Figure()

for stock in stocks3:
    fig3.add_trace(go.Bar(x = [2018,2019,2020,2021],y=df3[stock], name=stock))

selector2 = [
    {'label':stocks3[0],'method':'update','args':[{'visible':[True,False, False,False]}]},
    {'label':stocks3[1],'method':'update','args':[{'visible':[False,True, False,False]}]},
    {'label':stocks3[2],'method':'update','args':[{'visible':[False, False, True,False]}]},
    {'label':stocks3[3],'method':'update','args':[{'visible':[False, False,False, True]}]}
]

fig3.update_layout(
    updatemenus = [{'buttons':dropdown,'type':'buttons','direction':'left', 'yanchor':"top", 'y':1.2,'xanchor':'right','x':1.2}],title='Faturamento Total', 
)

fig3.add_annotation(x=2020, y=85000000000,
            text="Pandemia - COVID-19",
            showarrow=False)

fig3.update_yaxes(range=[0, 100000000000], title='R$')



#Streamlit

st.title("Relatório de Ações")

st.plotly_chart(fig)

st.plotly_chart(fig2)

st.plotly_chart(fig3)