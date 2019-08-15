

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import json
import datetime
import pandas as pd

# Connecting to the database
def rankings():


    connection = mysql.connector.connect(host='localhost',
                                             database='clearcentrix',
                                             user='user',
                                             password='password')
    cursor = connection.cursor()
# cursor.execute('SELECT claim_id FROM Claim_Summary LIMIT 5;')
# my_result = cursor.fetchall()
# for x in my_result:
  #  print(x)

    df = pd.read_sql('''SELECT clm_line.claim_line_item_control_number,clm_line.plan_remit_carc_1,
        clm_line.parent_provider_id,clm.plan_remit_date,
        clm_line.plan_billed_amount
          FROM Claim_Lines clm_line LEFT JOIN Claim_Summary clm ON
          clm_line.claim_id=clm.claim_id
          ;''', con=connection)
#print(df['claim_line_item_control_number'])

        #
        # # The ranks on providers and denials based on past
        # with open('denial_rank.json', 'r') as read_file:
        #     denial_rank = json.load(read_file)
    denial_rank = {'PR21':'11','PR22':'5','PR23':'7','PR24':'3','PR25':'6','PR26':'9'}
    with open('parnt_prov_rank.json', 'r') as read_file:
        prnt_prov_rank = json.load(read_file)
        #
        # # Ranking claims which have Process Flag - False
        #
    current_date = datetime.datetime.now()
        #
    df['exp'] = 180 - (current_date - df['plan_remit_date']).dt.days
        #
    df['rank_denial_code'] = df['plan_remit_carc_1'].map(denial_rank).fillna('4')
    df['rank_denial_code'] = df['rank_denial_code'].astype('float')
    df['rank_prov'] = df['parent_provider_id'].map(prnt_prov_rank).fillna('10')
    df['rank_prov'] = df['rank_prov'].astype('float')
        #
        # # Ranking formula
    df['rank'] = df['plan_billed_amount'] * df['rank_denial_code'] * df['rank_prov'] * 0.01 * df['exp']
#print(df['rank'])
#df['rank'] = df['rank'] / (df['plan_billed_submission_version'] + 1)
        # # Update query  rows
        #
    sql_update_query = """Update Claim_Lines set priority_score = %s where claim_line_item_control_number= %s;"""
        # # multiple records to be updated in tuple format
    records_to_update = list(zip(df['rank'], df['claim_line_item_control_number']))
    cursor.executemany(sql_update_query, records_to_update)
    connection.commit()

    df1 = pd.read_sql('''SELECT priority_score FROM Claim_Lines ;''', con=connection)
    print(df1)
        #
        # print(cursor.rowcount, "Records Updated successfully into computers table. ")
        # print("The Updated count is: ", cursor.rowcount)
# except mysql.connector.Error as error:
#     print("Failed to update records to database: {}".format(error))
# finally:
#         # closing database connection.
#         if connection.is_connected():
#             connection.close()
#         print("connection is closed")
