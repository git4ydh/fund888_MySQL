import pymysql
import pandas as pd
import streamlit as st
import os
import sys

import json
from streamlit_lottie import st_lottie


# 获取当前脚本的绝对路径  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  MySQL_DB import get_db_connection


st.set_page_config(  
    page_title="产品收益",  # 设置页面标题   
    page_icon="📈"
)  



st.logo("img/logo_hight_29.png", icon_image="img/logo_hight_29.png")

#@st.cache_data
def displayPro1Intrest(conn):
    # Connect to the database

    cursor = conn.cursor()
    # Execute the query
    query = "SELECT yearNum as 年份, monthNum, nowValue FROM fund_monthlyGain WHERE monthNum=12 ORDER BY yearNum ASC"
    cursor.execute(query)
    # Fetch the data
    data = cursor.fetchall()
    # Create the DataFrame
    df = pd.DataFrame(data, columns=['年份', 'monthNum', 'nowValue'])
    # Calculate the annual return rate manually
    df['年收益率'] = df['nowValue'].diff() / df['nowValue'].shift(1) * 100
    # Handle the first year separately
    df.loc[0, '年收益率'] = (df.loc[0, 'nowValue'] - 1) * 100
    # Display the results using Streamlit
    df['年份'] = df['年份'].astype(str) #去掉数字中的逗号
    df = df.sort_values(by="年份", ascending=False)
    st.write(df[['年份', '年收益率']].fillna('N/A'))
    # 将DataFrame转换为st.bar_chart所需的格式  
    chart_data = df[['年份', '年收益率']].set_index('年份')['年收益率'].to_dict()  
    st.bar_chart(chart_data)
    cursor.close()

#@st.cache_data
def displayProIntrest2(conn):
    try:
        with conn.cursor() as cursor:
            # SQL查询
            sql = """
                    SELECT 
                        DATE(startDate) AS '开始时间',
                        DATE(endDate) AS '结束时间',
                        FORMAT(twoTimesBankInterest / 2,2) AS '银行利率', 
                        FORMAT(twoTimesBankInterest,2) AS '两倍银行利率', 
                        FORMAT(fund2RealInterest,2) AS '产品2利率'
                    FROM
                        fund_pro2_intrest 
                    ORDER BY startDate DESC
            """
            cursor.execute(sql)
            
            # 获取查询结果
            results = cursor.fetchall()
            
            # 将结果转换为DataFrame
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            # 使用pandas的style功能为特定列添加颜色
            def highlight_column(s):
                return ['background-color: yellow' if s.name == '产品2利率' else '' for _ in s]

            # 应用样式到整个DataFrame的列
            styled_df = df.style.apply(highlight_column, axis=0)
            st.dataframe(styled_df)
            
    finally:
        w=1
        cursor.close()

conn  = get_db_connection()

st.subheader("产品一收益率,浮动收益(N%/年)" , divider="rainbow")
displayPro1Intrest(conn)

st.subheader("产品二收益率，固定收益，为银行一倍多一点" , divider="rainbow")
displayProIntrest2(conn)



with st.sidebar:  
    # 读取本地的 Lottie 文件
    with open("Lottie/chart.json", "r") as f:
        lottie_json_chart = json.load(f)
    st_lottie(lottie_json_chart,speed=3,height=240)

# Close the connection
conn.close()