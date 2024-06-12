import streamlit as st  
from sqlalchemy import create_engine, text 
import pandas as pd

from MySQL_DB import get_db_connection
from MySQL_DB import get_db_connection_sqlalchemy

from streamlit_lottie import st_lottie
import json


# 在 Streamlit 脚本的开头设置页面配置  
st.set_page_config(  
    page_title="账户查询",  # 设置页面标题   
    page_icon="📑"
)  

st.logo("img/logo_hight_29.png", icon_image="img/logo_hight_29.png")

  
# 检查用户是否已登录  
def is_user_logged_in():  
     return 'user_ID' in st.session_state and st.session_state.user_ID is not None
  
def authenticate_user(user_mail, user_code):
    try:
        connection = get_db_connection()  # 确保这个函数返回的是pymysql的连接
        cursor = connection.cursor()
        query = "SELECT ID, userName FROM fund_user WHERE userMail=%s AND userCode=%s"
        cursor.execute(query, (user_mail, user_code))
        result = cursor.fetchone()
        if result:
            st.session_state.user_ID = result['ID']
            st.session_state.user_name = result['userName']
            return True
        else:
            return False
    except:  # 使用pymysql的特定异常
        st.error(f"Error while connecting to MySQL: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
         

# SQL 查询
query1 = """
SELECT u.id, u.userName as 持有人,
'产品' + t.fundType as 产品类型,
SUM(moneyAmount) as 原始本金,
SUM((t.gainPercent/100) * t.moneyAmount) as 总收益,
(CONCAT((SUM((t.gainPercent/100) * t.moneyAmount) / SUM(moneyAmount) * 100), '%')) as 总收益率,
SUM((t.gainPercent/100) * t.moneyAmount + t.moneyAmount) as 本利合计
FROM fund_user as u
INNER JOIN fund_proBuyTransaction as t ON u.id = t.userID
WHERE t.withdrawstatus = 1
GROUP BY u.id, u.userName, t.fundType
"""

query2="""
SELECT 
'产品'+ t.fundType as 产品,
sum(moneyAmount) as 本金,round(
sum((t.realGain)*t.moneyAmount),2) as 收益,
round(((sum((t.realGain)*t.moneyAmount))/sum(moneyAmount)*100),2)+'%'as 收益率,round(
sum((t.realGain)*t.moneyAmount+t.moneyAmount),2) as 本利合计 
FROM fund_user as u INNER JOIN Query_fund_trans as t ON u.id = t.userID WHERE t.withdrawstatus=1 GROUP BY u.id,u.userName,t.fundType
"""

query3="""
SELECT   
    DATE_FORMAT(t.startDate, '%Y-%m-%d') AS `时间`,  
    CONCAT('产品', t.fundType) AS `产品`,  
    t.moneyAmount AS `本金`,  
    CONCAT(t.realGainPercent, '%') AS `收益率`,  
    ROUND(t.realGain * t.moneyAmount, 2) AS `收益`,  
    ROUND(t.realGain * t.moneyAmount + t.moneyAmount, 2) AS `本利合计`,  
    CASE   
        WHEN t.withDrawStatus = 1 THEN '正常'  
        WHEN t.withDrawStatus = 2 THEN '赎回'  
        ELSE NULL -- 如果需要处理其他情况，可以添加更多的WHEN子句  
    END AS `状态`,  
    fullMemoTip AS `说明`  
FROM   
    Query_fund_trans AS t
"""

# 连接数据库并执行查询
#@st.cache_data
def get_data_frame(query1,query2,query3):
    # 建立数据库连接
    connection = get_db_connection_sqlalchemy()
    
    # 执行查询并读取结果到DataFrame
    df1 = pd.read_sql(text(query1), connection)
    df2 = pd.read_sql(text(query2), connection)
    df3 = pd.read_sql(text(query3), connection)
    
    st.subheader("投资及收益汇总", divider='rainbow')
    st.dataframe(df1)
    st.subheader("客户产品收益统计", divider='rainbow')
    st.dataframe(df2)
    st.subheader("投资记录及收益明细", divider='rainbow')
    st.dataframe(df3)





# 侧边栏登录  
with st.sidebar:  
    if not is_user_logged_in():  
        user_mail = st.text_input("电子邮箱(eMail)")  
        user_code = st.text_input("密码", type="password")
        if st.button("登录"):  
            if authenticate_user(user_mail, user_code):  
                st.success("验证成功")  
            else:  
                st.error("验证不匹配，请确认后再输入。")  
  
# 主页面内容（仅当用户已登录时显示）  
if is_user_logged_in():  
    # 注销按钮  
    if st.button("退出登陆"):  
        del st.session_state.user_ID  
        st.session_state.clear()  # 可选，清除所有 session_state 变量  
        st.success("退出登陆") 
        #显示数据

if is_user_logged_in():  
    st.write(f"欢迎您登陆查询: {st.session_state.user_name} , 请勿刷新，刷新页面需重新登陆。^_^。如发现程序、数据等问题，请联系我解决。谢谢！")  
    # ... 其他登录后可见的内容 ...  
    # 注销按钮  
    query1+=" HAVING u.id="+str(st.session_state.user_ID)
    query2+=" HAVING u.id="+str(st.session_state.user_ID)
    query3+=" WHERE  t.userID="+str(st.session_state.user_ID)
    get_data_frame(query1,query2,query3)

else:  
    # Additional Streamlit code
    st.header("天业理财借款及收益查询" , divider="rainbow")
    st.subheader("请先在左侧侧边栏登录")

    # 读取本地的 Lottie 文件
    with open("Lottie/user_login.json", "r") as f:
        lottie_json_login = json.load(f)
    with open("Lottie/left.json", "r") as f:
        lottie_json_left = json.load(f)
    # 显示 Lottie 动画
    st_lottie(lottie_json_left, speed=3, reverse=False, loop=True, quality="high", height=50, width=50)
    st_lottie(lottie_json_login,speed=3,height=290)
    

  
# 自定义CSS（可选）  
# 你可以在这里添加自定义CSS来美化你的应用  
# st.markdown('''<style> /* CSS样式 */ </style>''', unsafe_allow_html=True)

# 添加CSS隐藏右上角的链接

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



