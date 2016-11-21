# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:52:17 2016

@author: volsicka
"""
import pandas as pd
import networkx as nx
import API
from sklearn import preprocessing
import database_manager as db

"""
Jestli chcete mít rúzně velká kolečka dle velikosti účtu, ve force.js nahraďte v proměnné   

var node = vis.selectAll("circle.node")
      .attr("r", 5)
      
      tímto
      
      .attr("r", function(d) { return d.balance; })
"""

#import numpy as np
#import matplotlib.pyplot as plt
#d = API.dataTransakci()
#acc = API.dataUctu()
transManager = db.TransactionsManager()
accManager = db.AccountsManager()

accounts = accManager.getAccounts()
transactions = transManager.getAllTransactions()

acc = accounts
d = transactions

dfAcc = pd.DataFrame(columns=('accountNumber', 'name', 'bankCode', 'balance', 'currency', 'isTransparent'))

for i in range(len(acc)):
    dfAcc.loc[i] = [acc[i].accountNumber, acc[i].name, acc[i].bankCode,acc[i].balance, 
           acc[i].currency, acc[i].isTransparent]

df = pd.DataFrame(columns=('sender','receiver','dueDate','amount'))
for i in range(len(d)):
    df.loc[i] = [d[i].sender, d[i].receiver,d[i].dueDate,d[i].amount]


min_max_scaler = preprocessing.MinMaxScaler()
dfAcc['balance'] = min_max_scaler.fit_transform(dfAcc['balance'].fillna(value=0).reshape(-1, 1))
#dfAcc[dfAcc['balance']<1] = 1
dfAcc['balance'] = dfAcc['balance'] * 20
dfAcc.loc[dfAcc['balance']<5,'balance'] = 5
  
    
G=nx.Graph()

df2 = df[df['sender']!='000000-0000000000']
dfTrans = df2[df2['receiver'] != '000000-0000000000']
dfTrans = dfTrans.reset_index()

for i in range(dfAcc.shape[0]):
    G.add_node(dfAcc.loc[i].accountNumber)
    
for i in range(dfTrans.shape[0]):
    G.add_edge(dfTrans.loc[i].sender,dfTrans.loc[i].receiver)
    
#000000-0305469993
#dfAcc[dfAcc.accountNumber == '000000-0305469993']['balance'].head(1).tolist()[0]
#nx.draw_networkx_edges(G)
#plt.show()
#H=nx.DiGraph(G)
#nx.draw(H)
#nx.draw_spectral(G)
#http://localhost:8000/force/force.html

import json
from networkx.readwrite import json_graph
import http_server

# this d3 example uses the name attribute for the mouse-hover value,
# so add a name to each node
for n in G:
    G.node[n]['name'] = dfAcc[dfAcc.accountNumber == n]['name'].head(1).to_string()
    G.node[n]['balance'] = dfAcc[dfAcc.accountNumber == n]['balance'].head(1).tolist()[0]
# write json formatted data
g = json_graph.node_link_data(G) # node-link format to serialize
# write json
json.dump(g, open('force/force.json','w'))
print('Wrote node-link JSON data to force/force.json')
# open URL in running web browser
http_server.load_url('force/force.html')
print('Or copy all files in force/ to webserver and load force/force.html')
#

