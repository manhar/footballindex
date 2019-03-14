#!/usr/bin/env python3
import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path

# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:16:35 2017
This function simulates a portfolio. Each portfolio has a name. Actions that can be performed in a portfolio:
    1. deposit fund
    2. buy player
    3. sell player

@author: ashish
"""
import pandas as pd
import os.path
from datetime import datetime, timedelta
import json
import time
import glob
from mysql_populate_table import insert_f_portfolio_txn, getPortfolioBalance, run_select_sql, run_insert_sql, run_delete_sql

#Game simulation
#method - buy /sell player or deposit fund
#show transacton

#variable holding data file path
file_path="/Users/ashish/Documents/footballindex/data/footballIndex"
#list of file header
col_names=['txn_dt', 'txn_time', 'pid', 'pname','trending','b_price','s_price','team']
#global variable to hold the balance
balance=0.0
commission_rate=0.02
portfolio={}

def set_balance(portfolio,x):
    portfolio["balance"]=x

def get_latest_datafile():
    data_file=""
    txn_date=datetime.today().strftime('%Y%m%d')
    data_file=file_path+txn_date+".txt"
    if os.path.isfile(data_file):
        #print("Today's file: "+data_file)
        return data_file
    else:
        return max(glob.iglob('/Users/ashish/Documents/footballindex/data/footballIndex*txt'), key=os.path.getctime)
        #raise Exception ("Unable to find data file "+data_file)


#log transaction in DB
def log_transaction(portfolio, action, footballer, qty, value, balance):

    curr_time=datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    values=[(curr_time, portfolio, action, footballer, qty, value, balance)]
    print(values)
    query = " INSERT INTO f_portfolio_txn(\
    txn_date , \
    portfolio ,\
    txn_type  ,\
    player  ,\
    qty ,\
    txn_value,\
    balance) "\
    "VALUES(%s,%s,%s,%s,%s,%s,%s)"
    run_insert_sql(query,values)
#update portfolio
def insert_into_portfolio(portfolio, footballer, qty, value):

    curr_time=datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    values=[(curr_time, portfolio,  footballer, qty, value)]
    print(values)
    query = " INSERT INTO f_portfolio(\
    txn_date , \
    portfolio ,\
    player  ,\
    qty ,\
    txn_value) "\
    "VALUES(%s,%s,%s,%s,%s)"
    run_insert_sql(query,values)

#update portfolio
def delete_from_portfolio(portfolio, footballer, qty, value):

    curr_time=datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    values=[(curr_time, portfolio,  footballer, qty, value)]
    print(values)
    query = """  delete from  f_portfolio where player = '"""+footballer+"'"
    run_delete_sql(query)



#function returnning the selling price of a player
def get_player_selling_price(pname):
    #load data file in dataframe
    data_file=""
    data_file=get_latest_datafile()
    df=pd.read_csv(data_file, sep="|",header=None,names=col_names )
    if (pname in df["pname"].values):
        #get the latest row based on max txn_date
        p_row=df.loc[(df['txn_time']==df['txn_time'].max()) & (df['pname']==pname)]
        return  p_row["s_price"].values[0]
    else:
        raise Exception ("Player %s does not exists in %s" %(pname, data_file))


#function returnning the buying price of a player
def get_player_buying_price(pname):
    #load data file in dataframe
    data_file=""
    data_file=get_latest_datafile()
    df=pd.read_csv(data_file, sep="|",header=None,names=col_names )
    if (pname in df["pname"].values):
        #get the latest row based on max txn_date
        p_row=df.loc[(df['txn_time']==df['txn_time'].max()) & (df['pname']==pname)]
        return  p_row["b_price"].values[0]
    else:
        raise Exception ("Player %s does not exists" %(pname))


##function to sell a player
#def sell_player(portfolio,pname, qty, selling_price):
#    cost=qty * selling_price
#    commission= commission_rate*cost
#    index= get_portfolio_player_index(portfolio, pname)
#    if index is None:
#        raise Exception ("Cannot peform sell transaction. Player %s does not exists in %s  " %(pname, portfolio))
#
#    else:
#        portfolio_qty=portfolio["players"][index]["qty"]
#        if qty > portfolio_qty:
#            raise Exception ("%s: Cannot sell %d shares of %s at %.2f .Avaliable qty in portfolio is %d " %(portfolio["portfolio_name"], qty,pname,selling_price, portfolio_qty) )
#            return False
#        else:
#
#            portfolio["players"][index]["qty"]-= qty
#            portfolio["players"][index]["total_cost"]+= cost
#            portfolio["balance"] +=cost
#            log_transaction(portfolio["portfolio_name"], "sold", pname, str(qty), str(cost), str(portfolio["balance"]))
#            #subtract comission from balance
#            portfolio["balance"]-=commission
#            log_transaction(portfolio["portfolio_name"], "commission", pname, str(qty), str(commission), str(portfolio["balance"]))
#            print ("Selling %d shares of %s at %.2f .Avaliable balance is %.2f " %(qty,pname,selling_price, portfolio["balance"]) )
#
#            #delete the player details if we have sold all shares for player
#            if portfolio["players"][index]["qty"] == 0:
#                del portfolio["players"][index]
#                return True


#function to sell a player
def sell_player(portfolio,pname, qty, selling_price):
    cost=qty * selling_price
    commission= commission_rate*cost*-1
    log_transaction(portfolio , "commission", pname, str(qty), str(commission), commission)
    log_transaction(portfolio , "sell", pname, str(qty), str(selling_price), cost)
    delete_from_portfolio(portfolio,pname, qty, selling_price)


#function to buy a player
def buy_player(portfolio, pname, qty, buying_price):
    cost=qty * buying_price *-1
    log_transaction(portfolio, "buy", pname, str(qty), str(buying_price), cost )
    insert_into_portfolio(portfolio, pname, qty, buying_price)


#
##function to buy a player
#def buy_player(portfolio, pname, qty, buying_price):
#    bal= portfolio["balance"]
#    cost=qty * buying_price
#    if cost > bal:
#        raise Exception ("Cannot buy %d shares of %s at %.2f .Avaliable balance is %.2f " %(qty,pname,buying_price, bal) )
#
#    else:
#        index= get_portfolio_player_index(portfolio, pname)
#        if index is  None:
#            player_dic={}
#            player_dic["pname"]= pname
#            player_dic["qty"]= qty
#            player_dic["total_cost"]=cost
#
#            portfolio["players"].append(player_dic)
#            portfolio["balance"] -= cost
#        else:
#
#            portfolio["players"][index]["qty"]+= qty
#            portfolio["players"][index]["total_cost"]+= cost
#            portfolio["balance"] -=cost
#        print ("Buying %d shares of %s at %.2f .Avaliable balance is %.2f " %(qty,pname,buying_price, portfolio["balance"]) )
#        log_transaction(portfolio["portfolio_name"], "buy", pname, str(qty), str(cost), str(portfolio["balance"]))
#    return True



def create_portfolio(portfolio_name):
    data={}
    data["portfolio_name"]=portfolio_name
    data["balance"]=0.0
    data["players"]=[]
    return  data


def deposit_fund(portfolio, fund):
    balance=get_portfolio_balance (portfolio)
    if (balance> 0):
        log_transaction(portfolio, "deposit", '', fund, 0,  str(balance + fund) )


def get_portfolio_balance(portfolio):
    bal=0
    bal_arr= getPortfolioBalance(portfolio)
    if not bal_arr:
        print ( portfolio, " does not exists")
        bal=-999
    else:
        bal = bal_arr[0]

    return bal

def get_portfolio_player_index(portfolio, pname):

    for index in  portfolio["players"]:
        if pname in index.values():
            return ( int(portfolio["players"].index(index)) )
        #else:
        #    return int(-9) #player does not exist in portfolio
def get_player_from_portfolio(portfolio, pname):
    result=run_select_sql(""" select qty as futures , txn_value as bprice from f_portfolio where player= '""" +pname + """' and portfolio= '"""+portfolio+"'")
    return result

def get_portfolio_transaction(portfolio):
    result=run_select_sql(""" select  * from f_portfolio_txn where  portfolio= '"""+portfolio+"'")
    return result


if __name__ == '__main__':
    portfolio_name="robot1"
    #robot_portfolio=create_portfolio(portfolio_name)
#    set_balance(robot_portfolio,100.0)
#    buy_player(robot_portfolio,"Shane Long" ,10)
#    print(robot_portfolio)
#    buy_player(robot_portfolio,"Shane Long" ,1)
#    print(robot_portfolio)
#    sell_player(robot_portfolio,"Shane Long" ,1)
#    print(robot_portfolio)
#
#    print (get_portfolio_balance('robot1'))
#    print(get_portfolio_balance('robot2'))
#
    #deposit_fund(portfolio_name, 1000.0)



# check if predictor suggest to buy
    d=['2017-05-27 13:08:03','2017-05-27 12:13:03']

    query=""" select * from predictor_backfill where what_to_do <>'keep'  order  by 1 asc """
    #his=""" select distinct datetime_id from predictor_backfill where what_to_do <>'keep'  order  by 1 asc """
    #his_df=run_select_sql(his)
    all_data=run_select_sql(query)
    his_df=all_data["datetime_id"].astype(str).unique()
    his_df.astype(str)

    for date_filter in his_df:
        #query=""" select * from predictor_backfill where what_to_do <>'keep' and  datetime_id='"""+date_filter+"'"
        #current_prediction=run_select_sql(query) '2017-05-06 21:54:02'
        current_prediction=all_data.loc[all_data.datetime_id==date_filter]
        #print(current_prediction)
        for i, row in current_prediction.iterrows():
           # print (row)
            player=row["player_id"]
            bprice=row["cur_bprice"]
            sprice=row["cur_sprice"]
            what_to_do=row["what_to_do"]
            player_portflio_df= get_player_from_portfolio(portfolio_name, player)
            if what_to_do=="buy"and player_portflio_df.empty:
                print(date_filter,"buying player ", player )
                buy_player(portfolio_name, player, 10 ,bprice )
                #add player to portfolio

            elif what_to_do=="sell"and not (player_portflio_df.empty):
                print (date_filter,"selling player " , player)
                sell_player(portfolio_name, player, 10,sprice)
                #remove player from portfolio
       # time.sleep(60)
