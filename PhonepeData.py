import pandas as pd
import json
import mysql.connector
import os
import requests

# To clone the data directly from github to current working directory
response = requests.get('https://api.github.com/repos/PhonePe/pulse')
repo = response.json()
clone_url = repo['clone_url']
repo_name = "pulse"
clone_dir = os.path.join(os.getcwd(), repo_name)

def get_aggregated_transaction_data(path):
    Agg_trans=os.listdir(path)
    Agg_trans_list = {'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'count':[], 'amount':[]}
    for i in Agg_trans:
        path_i = path + i+ "/"
        Agg_yr = os.listdir(path_i)
        for j in Agg_yr:
            path_j = path_i + j + "/"
            Agg_yr_list= os.listdir(path_j)
            for k in Agg_yr_list:
                path_k = path_j + k
                Data = open(path_k,'r')
                Data = json.load(Data)
                for z in Data['data']['transactionData']:
                    Name = z['name']
                    count = z['paymentInstruments'][0]['count']
                    amount = z['paymentInstruments'][0]['amount']
                    Agg_trans_list['Transaction_type'].append(Name)
                    Agg_trans_list['count'].append(count)
                    Agg_trans_list['amount'].append(amount)
                    Agg_trans_list['State'].append(i)
                    Agg_trans_list['Year'].append(j)
                    Agg_trans_list['Quarter'].append(int(k.strip('.json')))
    return pd.DataFrame(Agg_trans_list)

def get_aggregated_user_data(path):
    Agg_user = os.listdir(path)
    Agg_user_list = {'State': [], 'Year': [], 'Quarter': [], 'brand': [], 'count': [],
            'Percentage': []}
    for i in Agg_user:
        p_i = path + i + "/"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "/"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                Data = open(p_k, 'r')
                Data = json.load(Data)
                try:
                    for l in Data["data"]["usersByDevice"]:
                        brand_name = l["brand"]
                        count_ = l["count"]
                        ALL_percentage = l["percentage"]
                        Agg_user_list["brand"].append(brand_name)
                        Agg_user_list["count"].append(count_)
                        Agg_user_list["Percentage"].append(ALL_percentage)
                        Agg_user_list["State"].append(i)
                        Agg_user_list["Year"].append(j)
                        Agg_user_list["Quarter"].append(int(k.strip('.json')))
                except:
                    pass
    return pd.DataFrame(Agg_user_list)

def get_map_transaction_data(path):
    map_trans = os.listdir(path)
    map_trans_list = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'count': [],
            'amount': []}
    for i in map_trans:
        p_i = path + i + "/"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "/"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k       
                Data = open(p_k, 'r')
                Data = json.load(Data)
                for l in Data["data"]["hoverDataList"]:
                    District = l["name"]
                    count = l["metric"][0]["count"]
                    amount = l["metric"][0]["amount"]
                    map_trans_list["District"].append(District)
                    map_trans_list["count"].append(count)
                    map_trans_list["amount"].append(amount)
                    map_trans_list['State'].append(i)
                    map_trans_list['Year'].append(j)
                    map_trans_list['Quarter'].append(int(k.strip('.json')))
    return pd.DataFrame(map_trans_list)

def get_map_user_data(path):
    map_user = os.listdir(path)
    map_user_list = {"State": [], "Year": [], "Quarter": [], "District": [],
            "RegisteredUser": []}
    for i in map_user:
        p_i = path + i + "/"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "/"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                Data = open(p_k, 'r')
                Data = json.load(Data)
                for l in Data["data"]["hoverData"].items():
                    district = l[0]
                    registereduser = l[1]["registeredUsers"]
                    map_user_list["District"].append(district)
                    map_user_list["RegisteredUser"].append(registereduser)
                    map_user_list['State'].append(i)
                    map_user_list['Year'].append(j)
                    map_user_list['Quarter'].append(int(k.strip('.json')))
    return pd.DataFrame(map_user_list)
    
def get_top_transaction_data(path):
    top_trans = os.listdir(path)
    top_trans_list = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'count': [],
            'amount': []}
    for i in top_trans:
        p_i = path + i + "/"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "/"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                # print(p_k)
                Data = open(p_k, 'r')
                Data = json.load(Data)
                for l in Data['data']['pincodes']:
                    Name = l['entityName']
                    count = l['metric']['count']
                    amount = l['metric']['amount']
                    top_trans_list['District'].append(Name)
                    top_trans_list['count'].append(count)
                    top_trans_list['amount'].append(amount)
                    top_trans_list['State'].append(i)
                    top_trans_list['Year'].append(j)
                    top_trans_list['Quarter'].append(int(k.strip('.json')))
    return pd.DataFrame(top_trans_list)
    
def get_top_user_data(path):
    top_user = os.listdir(path)
    top_user_list = {'State': [], 'Year': [], 'Quarter': [], 'District': [],
            'RegisteredUser': []}
    for i in top_user:
        p_i = path + i + "/"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "/"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                # print(p_k)
                Data = open(p_k, 'r')
                Data = json.load(Data)
                for l in Data['data']['pincodes']:
                    Name = l['name']
                    registeredUser = l['registeredUsers']
                    top_user_list['District'].append(Name)
                    top_user_list['RegisteredUser'].append(registeredUser)
                    top_user_list['State'].append(i)
                    top_user_list['Year'].append(j)
                    top_user_list['Quarter'].append(int(k.strip('.json')))
    return pd.DataFrame(top_user_list)

def clean_state_names(df):
    """
    Given a DataFrame with a 'State' column, replace the state names with their full names.
    """
    states={'andaman-&-nicobar-islands':'Andaman & Nicobar',
             'andhra-pradesh': 'Andhra Pradesh',
             'arunachal-p':'Arunanchal Pradesh',
             'assam': 'Assam',
             'bihar': 'Bihar',
             'chandigarh': 'Chandigarh',
             'chhattisgarh': 'Chhattisgarh',
             'dadra-&-nagar-haveli-&-dama':'Dadara & Nagar Havelli',
             'delhi': 'NCT of Delhi',
             'goa': 'Goa',
             'gujarat': 'Gujarat',
             'haryana': 'Haryana',
             'himachal-pradesh': 'Himachal Pradesh',
             'jammu-&-kashmir': 'Jammu & Kashmir',
             'jharkhand': 'Jharkhand',
             'karnataka': 'Karnataka',
             'kerala': 'Kerala',
             'ladakh': 'Ladakh',
             'lakshadweep':'Lakshadweep',
             'madhya-pradesh': 'Madhya Pradesh',
             'maharashtra': 'Maharashtra',
             'manipur': 'Manipur',
             'meghalaya': 'Meghalaya',
             'mizoram':'Mizoram',
             'nagaland': 'Nagaland',
             'puducherry': 'Puducherry',
             'punjab': 'Punjab',
             'rajasthan': 'Rajasthan',
             'sikkim': 'Sikkim',
             'tamil-nadu': 'Tamil Nadu',
             'telangana': 'Telangana',
             'tripura': 'Tripura',
             'uttar-pradesh': 'Uttar Pradesh',
             'uttarakhand': 'Uttarakhand',
             'west-bengal': 'WestBengal',
             'odisha':'Odisha'}

    df['State'] = df['State'].replace(states)
    return df

def create_and_update_table(cursor, table_name,data,columns):
    """
    Create a table with the given table_name and columns using the given cursor.
    """
    create_and_update_table_query = (
        f"CREATE TABLE IF NOT EXISTS {table_name} ("
        f"{', '.join(columns)})"
    )
    cursor.execute(create_and_update_table_query)
    """
    Insert data into the given table using the given cursor.
    """
    for row in data:
        insert_row_query = (
            f"INSERT INTO {table_name} "
            f"({', '.join(row.keys())}) "
            f"VALUES ({', '.join([f'%({k})s' for k in row.keys()])})"
        )
        cursor.execute(insert_row_query, row)
        
cnx = mysql.connector.connect(user='root', password='Your_Password',
                              host='localhost',
                              database='Phonepe_Pulse')

cursor = cnx.cursor()
def main():
    #Get the data from json file
    df_aggregated_transaction = get_aggregated_transaction_data("pulse/data/aggregated/transaction/country/india/state/")
    df_aggregated_user = get_aggregated_user_data("pulse/data/aggregated/user/country/india/state/")
    df_map_transaction=get_map_transaction_data("pulse/data/map/transaction/hover/country/india/state/")
    df_map_user=get_map_user_data("pulse/data/map/user/hover/country/india/state/")
    df_top_transaction=get_top_transaction_data("pulse/data/top/transaction/country/india/state/")
    df_top_user=get_top_user_data("pulse/data/top/user/country/india/state/")
    
    #to clean the state names
    df_aggregated_transaction = clean_state_names(df_aggregated_transaction)
    df_aggregated_user = clean_state_names(df_aggregated_user)
    df_map_transaction=clean_state_names(df_map_transaction)
    df_map_user=clean_state_names(df_map_user)
    df_top_transaction=clean_state_names(df_top_transaction)
    df_top_user=clean_state_names(df_top_user)
    
    #To create and update the data to Mysql DB
    create_and_update_table(cursor, 'aggregated_transactions', df_aggregated_transaction.to_dict(orient='records'),["id INT NOT NULL AUTO_INCREMENT",
                                     "State VARCHAR(255)",
                                     "Year VARCHAR(255)",
                                     "Quarter VARCHAR(255)",
                                     "Transaction_type VARCHAR(255)",
                                     "count INT",
                                     "amount FLOAT",
                                     "PRIMARY KEY (id)"
                                     ])
    
    create_and_update_table(cursor, 'aggregated_user',df_aggregated_user.to_dict(orient='records'),["id INT NOT NULL AUTO_INCREMENT,"
                                     "  State VARCHAR(255),"
                                     "  Year VARCHAR(255),"
                                     "  Quarter VARCHAR(255),"
                                     "  brand VARCHAR(255),"
                                     "  count INT,"
                                     "  Percentage FLOAT,"
                                     "  PRIMARY KEY (id)"
                                     ])

    create_and_update_table(cursor, 'map_transaction',df_map_transaction.to_dict(orient='records'),["  id INT NOT NULL AUTO_INCREMENT,"
                                     "  State VARCHAR(255),"
                                     "  Year VARCHAR(255),"
                                     "  Quarter VARCHAR(255),"
                                     "  District VARCHAR(255),"
                                     "  count INT,"
                                     "  amount FLOAT,"
                                     "  PRIMARY KEY (id)"])

    create_and_update_table(cursor, 'map_user',df_map_user.to_dict(orient='records'),["  id INT NOT NULL AUTO_INCREMENT,"
                                     "  State VARCHAR(255),"
                                     "  Year VARCHAR(255),"
                                     "  Quarter VARCHAR(255),"
                                     "  District VARCHAR(255),"
                                     "  RegisteredUser INT,"
                                     "  PRIMARY KEY (id)"])

    create_and_update_table(cursor, 'top_transaction',df_top_transaction.to_dict(orient='records'),["  id INT NOT NULL AUTO_INCREMENT,"
                                     "  State VARCHAR(255),"
                                     "  Year VARCHAR(255),"
                                     "  Quarter VARCHAR(255),"
                                     "  District VARCHAR(255),"
                                     "  count INT,"
                                     "  amount FLOAT,"
                                     "  PRIMARY KEY (id)"])

    create_and_update_table(cursor, 'top_user',df_top_user.to_dict(orient='records'),["  id INT NOT NULL AUTO_INCREMENT,"
                                     "  State VARCHAR(255),"
                                     "  Year VARCHAR(255),"
                                     "  Quarter VARCHAR(255),"
                                     "  District VARCHAR(255),"
                                     "  RegisteredUser INT,"
                                     "  PRIMARY KEY (id)"])  
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
