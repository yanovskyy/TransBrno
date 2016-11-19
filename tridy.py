# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:48:47 2016

@author: volsicka
"""

class Account:
    def __init__(self, accountNumber, name, bankCode, currency):
        self.accountNumber = ''
        self.name = ''
        self.bankCode = -1
        self.currency = ''
    
class Transaction:
    def __init__(self, sender, receiver, dueDate, amount):
        if amount<0:
            self.sender = receiver
            self.receiver = sender
            self.amount = abs(amount)
        else:
            self.sender = sender
            self.receiver = receiver            
            self.dueDate = dueDate
            self.amount = amount