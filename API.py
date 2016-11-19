# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 10:42:15 2016

@author: volsicka

API přístup k datům transparentních účtu v ČSAS
"""

#import simplejson as json
import simplejson as json
import requests
from classes import Account, Transaction
from database_manager import *

headers = {
  'WEB-API-key': '678fb7e7-52d3-4c9f-a937-18fda0c84b48',
  'content-encoding':'UTF-8'
}

#info = {'accountNumber':''}
#r = requests.get('https://api.csas.cz/sandbox/webapi/api/v2/transparentAccounts/', headers=headers)
#
#data = json.loads(r.text)
#print(json.dumps(data, indent=4, sort_keys=True))
#for i in range(len(data['accounts'])):
#    print(data['accounts'][i]['accountNumber'] + ", " + data['accounts'][i]['name'] )

"""
data o uctech
"""
def dataUctu():    
    r = requests.get('https://api.csas.cz/sandbox/webapi/api/v2/transparentAccounts/', headers=headers)
    
    data = json.loads(r.text,"utf8")
    A = []
    for i in range(len(data.get('accounts',[]))):
        ucet = Account(
            data['accounts'][i]['accountNumber'],
            data['accounts'][i]['name'],
            str(data['accounts'][i]['bankCode']),
            float(data['accounts'][i]['balance']),
            data['accounts'][i].get('currency',None),
            True
        )
        A.append(ucet)
        
    for i in range(len(data['accounts'])):
        cisloUctu = data['accounts'][i]['accountNumber']
    
        r = requests.get('https://api.csas.cz/sandbox/webapi/api/v2/transparentAccounts/'+cisloUctu+'/transactions/', headers=headers)
        #print(json.dumps(dataUcet, indent=4, sort_keys=True))
        dataUcet = json.loads(r.text)
        #print(json.dumps(data, indent=4, sort_keys=True))
        for i in range(len(dataUcet.get('transactions',[]))):
            tranS = Account(
                str(dataUcet['transactions'][i]['sender'].get('accountNumber',None)),
                None,
                dataUcet['transactions'][i]['sender'].get('bankCode',None),
                None,
                None,
                False
            )
            
            if tranS not in A:
                A.append(tranS)           
            
            tranR = Account(
                str(dataUcet['transactions'][i]['receiver'].get('accountNumber',None)),
                None,
                dataUcet['transactions'][i]['receiver'].get('bankCode',None),
                None,
                None,
                0
            )
         
            if tranR not in A:
                A.append(tranR)
    return A


"""
data o transakcích
"""
def dataTransakci():    
    r = requests.get('https://api.csas.cz/sandbox/webapi/api/v2/transparentAccounts/', headers=headers)
    
    data = json.loads(r.text)
    #print(json.dumps(data, indent=4, sort_keys=True))
    T=[]
    for i in range(len(data['accounts'])):
        cisloUctu = data['accounts'][i]['accountNumber']
    
        r = requests.get('https://api.csas.cz/sandbox/webapi/api/v2/transparentAccounts/'+cisloUctu+'/transactions/', headers=headers)
        dataUcet = json.loads(r.text)

        for i in range(len(dataUcet.get('transactions',[]))):
            tran = Transaction(str(dataUcet['transactions'][i]['sender']['accountNumber']), \
            str(dataUcet['transactions'][i]['receiver']['accountNumber']), \
            str(dataUcet['transactions'][i]['dueDate'])[:10], \
            float(dataUcet['transactions'][i]['amount']['value']),
            dataUcet['transactions'][i]['amount']['currency']
            )
            T.append(tran)
    return T


#print d
account_list = dataUctu()
accManager = AccountsManager()
transManager = TransactionsManager()
accManager.createAccounts(account_list)
transactions_list = dataTransakci()
transManager.createTransactions(transactions_list)


#df = pd.DataFrame(columns=('sender','receiver','dueDate','amount'))
#for i in range(len(d)):
#    df.loc[i] = [d[i].sender, d[i].receiver,d[i].dueDate,d[i].amount]
