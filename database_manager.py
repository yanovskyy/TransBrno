import sqlite3
from classes import *

class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg, values):
        self.cur.execute(arg, values)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()

class AccountsManager(object):
    def createAccounts(self, accounts):
        dbmgr = DatabaseManager("TRANSBRNO.db")
        for account in accounts:
            query = """
                INSERT OR IGNORE into ACCOUNTS
                ('ACCOUNT_NUMBER', 'NAME', 'BANK_CODE', 'CURRENCY', 'TRANSPARENT', 'BALLANCE')
                values (?, ?, ?, ?, ?, ?)
            """
            values = (account.accountNumber, account.name, account.bankCode, account.balance, account.currency, account.isTransparent)
            for row in dbmgr.query(query, values):
                print (row)

class TransactionsManager(object):
    def createTransactions(self, transactions):
        dbmgr = DatabaseManager("TRANSBRNO.db")
        for transaction in transactions:
            query = """
                  insert into TRANSACTIONS
                  ('SENDER', 'RECEIVER', 'AMOUNT', 'DUE_DATE', 'CURRENCY')
                  values (?, ?, ?, ?, ?)
            """
            values = (transaction.sender, transaction.receiver, transaction.amount, transaction.dueDate, transaction.currency)
            for row in dbmgr.query(query, values):
                    print (row)


#account = Account("000000-2824570013", "Spolecenstvi Praha 4", 8000, 35345.5, "CZK", True)
# account_list = [account]
# accManager = AccountsManager()
# accManager.createAccounts(account_list)