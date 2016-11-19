# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:48:47 2016

@author: volsicka
"""


class Account:
    def __init__(self, accountNumber, name, bankCode, balance, currency, isTransparent):
        self.accountNumber = accountNumber
        self.name = name
        self.bankCode = bankCode
        self.balance = balance
        self.currency = currency
        self.isTransparent = isTransparent

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Transaction:
    def __init__(self, sender, receiver, dueDate, amount, currency):
        if amount < 0:
            self.sender = receiver
            self.receiver = sender
            self.amount = abs(amount)
        else:
            self.sender = sender
            self.receiver = receiver
            self.amount = amount

        self.dueDate = dueDate
        self.currency = currency