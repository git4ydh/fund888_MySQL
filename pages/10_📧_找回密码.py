import streamlit as st  
import re  
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
import os
import sys 

from streamlit_lottie import st_lottie
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  MySQL_DB import get_db_connection

# 在 Streamlit 脚本的开头设置页面配置  
st.set_page_config(  
    page_title="找回密码",  # 设置页面标题   
    page_icon="📧"
)  

st.logo("img/logo_hight_29.png", icon_image="img/logo_hight_29.png")

# 数据库连接配置  
 
  
# 邮件发送配置  
email_config = {  
    'sender': 'ok_ydh@163.com',  
    'password': 'Sea86757@',  
    'smtp_server': 'smtp.163.com',  
    'smtp_port': 465  
}  
  
def send_email(recipient, message):  
    msg = MIMEMultipart()  
    msg['From'] = email_config['sender']  
    msg['To'] = recipient  
    msg['Subject'] = "天业理财账户密码"  
    msg.attach(MIMEText(message, 'plain'))  
      
    server = smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port'])  
    server.login(email_config['sender'], email_config['password'])  
    server.sendmail(email_config['sender'], recipient, msg.as_string())  
    server.quit()  
  
def validate_email(email):  
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  
    return re.match(pattern, email) is not None  
  
def query_database(email):  
    conn = get_db_connection()
    cursor = conn.cursor()  
    query = "SELECT userCode FROM fund_user WHERE userMail = %s"  
    cursor.execute(query, (email.lstrip().rstrip()),)  
    result = cursor.fetchone()  
    cursor.close()  
    conn.close()
    # 如果result不是None，那么我们可以安全地返回它的第一个元素  
    if result is not None:  
        return result  # 这里我们假设查询只返回了一个字段（userCode）  
    else:  
        return None  # 或者你可以返回一个特定的值或抛出一个异常来表示没有找到用户  
  
# Streamlit 应用主体   
st.header("找回账户查询密码" , divider="rainbow")
email = st.text_input('请输入您的电子邮箱地址')  
  
if st.button('发送密码到邮箱'):  
    if not validate_email(email):  
        st.error('请输入有效的电子邮件地址！')  
    else:  
        result = query_database(email)  
        if result:  
            user_code = result['userCode']
            print(user_code)
            message = f"天业理财账户查询，您的密码是: {user_code}"  
            send_email(email, message) 
            st.success('密码已发送到您的邮箱！')  
        else:  
            st.error('未找到与该邮箱地址相关联的用户！')


# 读取本地的 Lottie 文件
with open("Lottie/eMail.json", "r") as f:
    lottie_json_eMail = json.load(f)
st_lottie(lottie_json_eMail,speed=3,height=240)
    
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

