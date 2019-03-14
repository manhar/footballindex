import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path



from mysql.connector import MySQLConnection, Error
import pandas as pd
from sqlalchemy import create_engine
import datetime
import dateutil.relativedelta
import my_config


current_datetime=datetime.datetime.today()


sql_alchemy =my_config.ConfigSectionMap("sql_alchemy")['db_parameters']
engine = create_engine(sql_alchemy)
sql_connector = my_config.ConfigSectionMap("mysql_connector")

f=open("/home/wolverine/projects/secret/pwd.txt")
pwd=f.read().replace("\n","")
f.close()

sql_connector["password"]=pwd

sql_alchemy=sql_alchemy.replace("<user>",sql_connector["user"]).replace("<database>",sql_connector["database"]).replace("<host>",sql_connector["host"]).replace("<pwd>",sql_connector["password"])




def insert_f_daily_score(scores):
    query = "INSERT INTO f_daily_score( \
             date_id ,\
             time_id , \
             player_id  ,\
             player_name , \
             rank  , \
             bprice  , \
             sprice   ,\
             trend ,\
             team  ,\
             datetime_id ) "\
             "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        conn = MySQLConnection(** sql_connector)

        cursor = conn.cursor()
        cursor.executemany(query, scores)

        conn.commit()
    except Error as e:
        print('Error insert_f_daily_score:', e)

    finally:
        cursor.close()
        conn.close()


def insert_f_daily_score_staging(scores):
    query = "INSERT INTO f_daily_score_staging( \
             date_id ,\
             time_id , \
             player_id  ,\
             player_name , \
             rank  , \
             bprice  , \
             sprice   ,\
             trend ,\
             team ,\
             datetime_id ) "\
             "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        conn = MySQLConnection(** sql_connector)

        cursor = conn.cursor()
        cursor.executemany(query, scores)

        conn.commit()
    except Error as e:
        print('Error insert_f_daily_score_staging:' ,scores, e)

    finally:
        cursor.close()
        conn.close()



def insert_f_daily_news(values):
    query = "INSERT INTO f_daily_news(hash_key ,feed_name ,title,link,comments,description,pubdate,pos_score,neg_score) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()
        cursor.executemany(query, values)

        conn.commit()
    except Error as e:
        print('Error insert_f_daily_news: ',values, e)

    finally:
        cursor.close()
        conn.close()


def insert_d_player_list(values):
    query1 = "truncate table d_player_list; "
    query2="INSERT INTO d_player_list(player_id ,player_name, team) VALUES(%s,%s,%s)"

    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()
        cursor.execute(query1)
        cursor.executemany(query2, values)

        conn.commit()
    except Error as e:
        print('Error insert_d_player_list: ',values, e)

    finally:
        cursor.close()
        conn.close()


def run_insert_sql(query, values):
    #query = "INSERT INTO f_daily_news(hash_key ,feed_name ,title,link,comments,description,pubdate,pos_score,neg_score) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()
        cursor.executemany(query, values)

        conn.commit()
    except Error as e:
        print('Error running insert sql : ',query ,values, e)

    finally:
        cursor.close()
        conn.close()

def run_select_sql(query):
    df=pd.DataFrame()
    df =getDataInDF(query, query)
    #print (df.count())
    return df

def run_delete_sql(query):
    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()
    except Error as e:
        print('Error running insert sql : ',query, e)

    finally:
        cursor.close()
        conn.close()


def check_new_hash_key_exists(hash_key):
    query="select hash_key from f_daily_news where hash_key= '"+ hash_key+"'"
    res=""
    try:
        conn = MySQLConnection(** sql_connector)

        cursor = conn.cursor()
        cursor.execute (query)
        res=cursor.fetchall()

    except Error as e:
        print('Error check_new_hash_key_exists:', e)

    finally:
        cursor.close()
        conn.close()
    return res


def getplayerpredictionscore(pid):
    #query=""" select  datetime_id as txn_datetime  , date_id, time_id, player_id, bprice, sprice, rank, trend  , 1 as last_5min_pct_change, 1 as last_24hr_pct_change from f_daily_score where player_id= '"""+ pid+"'"

    #query= """ select  datetime_id as txn_datetime  ,  player_id, cur_bprice as bprice, last_5min_pct_change, last_24hr_pct_change from f_player_stats where player_id= '"""+ pid+"'"
    query= """ select  datetime_id as txn_datetime  ,  player_id, cur_bprice as bprice,
    last_1min_pct_change,
    last_2min_pct_change,
    last_3min_pct_change,
    last_4min_pct_change,
    last_5min_pct_change,
    last_6min_pct_change,
    last_7min_pct_change,
    last_8min_pct_change,
    last_9min_pct_change,
    last_10min_pct_change,
    what_to_do,
    last_24hr_pct_change from predictor where player_id= '"""+ pid+"'"

    res=""
    df=pd.DataFrame()
    try:
        df = pd.read_sql(query, engine)

    except Error as e:
        print('Error getplayerpredictionscore:', e)
    return df


def getplayerscore(pid,hours_filter ):

    dt=(current_datetime - dateutil.relativedelta.relativedelta(hours=hours_filter)).strftime("%Y-%m-%d %H:%m:%S")

    if pid=="":
        query= """ select   * from f_daily_score where  datetime_id >='"""+dt+"'"
    else:
        query= """ select   * from f_daily_score where player_id= '"""+ pid+"' and datetime_id >='"+dt+"'"

    df=pd.DataFrame()
    try:
        df = pd.read_sql(query, engine)

    except Error as e:
        print('Error getplayerscore:', e)
    return df



def getNewsPubDateByPlayer(pid, team, hours_filter):
    dt =(current_datetime - dateutil.relativedelta.relativedelta(hours=hours_filter)).strftime("%Y-%m-%d %H:%m:%S")
    #query=""" select  datetime_id as txn_datetime  , date_id, time_id, player_id, bprice, sprice, rank, trend  , 1 as last_5min_pct_change, 1 as last_24hr_pct_change from f_daily_score where player_id= '"""+ pid+"'"

    #query= """ select  datetime_id as txn_datetime  ,  player_id, cur_bprice as bprice, last_5min_pct_change, last_24hr_pct_change from f_player_stats where player_id= '"""+ pid+"'"
    if (team=="" and  pid==""):
        query= """select hash_key, pubdate, title , feed_name
        from f_daily_news n
        where
        pubdate >= '"""+dt+"""'"""

    elif team=="":
        query= """select hash_key, pubdate, title , feed_name
        from f_daily_news n
        where
        pubdate >= '"""+dt+"""'
        and match(title) against ('"""+pid+"""')"""
    elif pid=="":
        query= """select hash_key, pubdate, title , feed_name
        from f_daily_news n
        where
        pubdate >= '"""+dt+"""'
        and match(title) against ('"""+team+"""')"""
    else:
        query= """ select hash_key, pubdate, title , feed_name
        from f_daily_news n
        where
        pubdate >= '"""+dt+"""'
        and match(title ) against( '"""+team+"""')
        and match(title) against ('"""+pid+"""')"""

    df=pd.DataFrame()
    try:
        df = pd.read_sql(query, engine)

    except Error as e:
        print('Error getNewsPubDateByPlayer:', e)
    return df



def getLatestNewsKey(HH):
    #This function returns the latest news hash keys after HH hours
    query=""" select hash_key from f_daily_news where STR_TO_DATE( pubdate, '%Y%m%d %H:%i:%s') >=  DATE_ADD(now(), INTERVAL -"""+str(HH)+""" HOUR) ;"""
    df=pd.DataFrame()
    df_arr=[]
    try:
        df = pd.read_sql(query, engine)
        df_arr=df.hash_key.values

    except Error as e:
        print('Error getLatestNewsKey:', e)
    return df_arr


def getPortfolioBalance(portfolio):
    #This function returns the latest news hash keys after HH hours
    query=""" select balance from f_portfolio_txn where portfolio='"""+portfolio+"""' order by txn_date desc limit 1 ;"""
    df=pd.DataFrame()
    df_arr=[]
    try:
        df = pd.read_sql(query, engine)
        df_arr=df.balance.values

    except Error as e:
        print('Error getPortfolioBalance:', e)
    return df_arr


def getDataInDF(caller, query):

    #print(query)
    df=pd.DataFrame()
    try:
        df = pd.read_sql(query, engine)
    except Error as e:
        print(str(caller),":", e)
    return df

def getAllplayerscore(hours_filter):
    dt=(current_datetime - dateutil.relativedelta.relativedelta(hours=hours_filter)).strftime("%Y-%m-%d %H:%m:%S")

    query=""" select datetime_id as txn_datetime , date_id, time_id, player_id, bprice, sprice, rank, trend from f_daily_score where datetime_id  >= '"""+dt+"'"

    df=pd.DataFrame()
    df =getDataInDF("getAllplayerscore", query)
    #print (df.count())
    return df

def getDistinctPlayers(hours_filter):
    dt=(current_datetime - dateutil.relativedelta.relativedelta(hours=hours_filter)).strftime("%Y-%m-%d %H:%m:%S")

    query=""" select distinct player_id from f_daily_score where datetime_id  >= '"""+dt+"'"

    df=pd.DataFrame()
    df =getDataInDF("getDistinctPlayers", query)
    #print (df.count())
    return df


def getAllprediction(player_id, dt):
    #dt=(current_datetime - dateutil.relativedelta.relativedelta(hours=hours_filter)).strftime("%Y-%m-%d %H:%m:%S")

    query=""" select * from predictor where player_id ='"""+player_id+"""' and datetime_id  >= '"""+dt+"'  "

    df=pd.DataFrame()
    df =getDataInDF("getAllprediction", query)
    #print (df.count())
    return df

def get_pos_news_date(player):
    query="""select  hash_key, pubdate  \
    from f_daily_news \
    where lower(title) like '%"""+ player+"""%'\
    and pos_score >neg_score \
    and lower(title) like '% man utd%'\
    order by pubdate desc ;"""
    df=pd.DataFrame()
    df =getDataInDF("get_pos_news_date", query)
    return df

def get_neg_news_date(player):
    query="""select  hash_key, pubdate  \
    from f_daily_news \
    where lower(title) like '%"""+ player+"""%'\
    and pos_score < neg_score \
    and lower(title) like '% man utd%'\
    order by pubdate desc ;"""
    df=pd.DataFrame()
    df =getDataInDF("get_neg_news_date", query)
    return df



def insert_f_portfolio_txn(values):
    query = "INSERT INTO f_portfolio_txn(\
    txn_date , \
    portfolio ,\
    txn_type  ,\
    player  ,\
    qty ,\
    txn_value,\
    balance) "\
    "VALUES(%s,%s,%s,%s,%s,%s,%s)"

    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()
        cursor.executemany(query, values)

        conn.commit()
    except Error as e:
        print('Error insert_f_portfolio_txn:', e)

    finally:
        cursor.close()
        conn.close()


def run_mysql_proc(proc_name, param):
    result=""

    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()
        cursor.callproc(proc_name, param)

        conn.commit()
    except Error as e:
        print('Error run_mysql_proc: ' , e)

    finally:
        cursor.close()
        conn.close()


def run_mysql_proc_output(proc_name):
    #result=()

    try:

        conn = MySQLConnection(** sql_connector)
        cursor = conn.cursor()

        #args = [0, 0,0,0]

        #result=cursor.callproc(proc_name, args)
        cursor.callproc(proc_name)
        print(cursor.stored_results())
        data=cursor.stored_results()
        return pd.DataFrame(data, columns=['player_id', 'bprice', 'sprice', 'what_to_do'])
        #for result in cursor.stored_results():
        #    print(result.fetchall())
       # cursor.execute("call predictor()",multi=True)
       # result=cursor.fetchall()
        #print(type(result))


        conn.commit()
    except Error as e:
        print('Error run_mysql_proc: ' , e)

    finally:
        cursor.close()
        conn.close()

    #return result
