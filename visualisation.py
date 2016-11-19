# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:52:17 2016

@author: volsicka
"""
import pandas as pd
import networkx as nx
import API
#import numpy as np
#import matplotlib.pyplot as plt
d = API.dataTransakci()
acc = API.dataUctu()
dfAcc = pd.DataFrame(columns=('accountNumber', 'name', 'bankCode', 'balance', 'currency', 'isTransparent'))

for i in range(len(acc)):
    dfAcc.loc[i] = [acc[i].accountNumber, acc[i].name, acc[i].bankCode,acc[i].balance, 
           acc[i].currency, acc[i].isTransparent]

df = pd.DataFrame(columns=('sender','receiver','dueDate','amount'))
for i in range(len(d)):
    df.loc[i] = [d[i].sender, d[i].receiver,d[i].dueDate,d[i].amount]
    
    
G=nx.Graph()

df2 = df[df['sender']!='000000-0000000000']
dfTrans = df2[df2['receiver'] != '000000-0000000000']
dfTrans = dfTrans.reset_index()
for i in range(dfAcc.shape[0]):
    G.add_node(dfAcc.loc[i].accountNumber)
    
for i in range(dfTrans.shape[0]):
    G.add_edge(dfTrans.loc[i].sender,dfTrans.loc[i].receiver)
    

#nx.draw_networkx_edges(G)
#plt.show()
#H=nx.DiGraph(G)
#nx.draw(H)
#nx.draw_spectral(G)

import json
from networkx.readwrite import json_graph
import http_server

# this d3 example uses the name attribute for the mouse-hover value,
# so add a name to each node
for n in G:
    G.node[n]['name'] = dfAcc[dfAcc.accountNumber == n]['name'].head(1).to_string()
# write json formatted data
d = json_graph.node_link_data(G) # node-link format to serialize
# write json
json.dump(d, open('force/force.json','w'))
print('Wrote node-link JSON data to force/force.json')
# open URL in running web browser
http_server.load_url('force/force.html')
print('Or copy all files in force/ to webserver and load force/force.html')
#
#nx.draw_graphviz(G)
#hist = np.histogram(df['amount'], bins=20)
#plt.plot(df['amount'])
#plt.show()
#plt.hist(hist)    
#
#print df['amount'].min(),df['amount'].max()
for n in G:
    print G.node[n]['name']