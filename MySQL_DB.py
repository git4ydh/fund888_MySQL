import pymysql.cursors
import streamlit as st
from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus  
 

#@st.cache_resource
def get_db_connection():
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor,
        db="fund888_schema",
        host="mysql4fund888-dahai-b872.g.aivencloud.com",
        password="AVNS_ENBkUZ8m80t2z-QTjc0",
        read_timeout=10,
        port=14503,
        user="avnadmin",
        write_timeout=10,
    )
    return connection



 

'''
def get_db_connection_sqlalchemy():
    connSQLalachemy = create_engine('mysql+pymysql://avnadmin:AVNS_ENBkUZ8m80t2z-QTjc0@mysql4fund888-dahai-b872.g.aivencloud.com/fund888_schema')  
    return connSQLalachemy
'''

def get_db_connection_sqlalchemy():
    # PyMySQL 连接参数  
    db_user = 'avnadmin'  
    db_password = 'AVNS_ENBkUZ8m80t2z-QTjc0'  
    db_host = 'mysql4fund888-dahai-b872.g.aivencloud.com'  
    db_port = 14503  
    db_name = 'fund888_schema'  
    timeout = 10  
    
    # 构造 SQLAlchemy 连接字符串（不包括连接超时等参数）  
    db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'  
    
    # 设置连接参数，包括连接超时等  
    connect_args = {  
        'connect_timeout': timeout,  
        'read_timeout': timeout,  
        'write_timeout': timeout,  
    }  
    
    # 使用 create_engine 创建 SQLAlchemy 引擎  
    connSQLalachemy = create_engine(db_url, connect_args=connect_args)
    return connSQLalachemy