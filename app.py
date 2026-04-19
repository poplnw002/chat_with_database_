import streamlit as st
import pandas as pd
import sqlite3
from google import genai
from google.genai import types
import json
# ดึง API Key
gemini_api_key = st.secrets["gemini_api_key"]
gmn_client = genai.Client(api_key=gemini_api_key)
# รายละเอียดฐานข้อมูล
db_name = 'test_database.db'
data_table = 'transactions'
data_dict_text = """
- trx_date: วันที7ทําธุรกรรม
- trx_no: หมายเลขธุรกรรม
- member_code: รหัสสมาชิกของลูกค้า
- branch_code: รหัสสาขา
- branch_region: ภูมิภาคที7สาขาตั้งอยู่
- branch_province: จังหวัดที7สาขาตั้งอยู่
- product_code: รหัสสินค้า
- product_category: หมวดหมู่หลักของสินค้า
- product_group: กลุ่มของสินค้า
- product_type: ประเภทของสินค้า
- order_qty: จํานวนชิ Dน/หน่วย ที7ลูกค้าสั7งซื Dอ
- unit_price: ราคาขายของสินค้าต่อ K หน่วย
- cost: ต้นทุนของสินค้าต่อ K หน่วย
- item_discount: ส่วนลดเฉพาะรายการสินค้านั Dนๆ
- customer_discount: ส่วนลดจากสิทธิของลูกค้า
- net_amount: ยอดขายสุทธิของรายการนั Dน
- cost_amount: ต้นทุนรวมของรายการนั Dน
"""
# HELPER FUNCTIONS
def query_to_dataframe(sql_query, database_name):
"""รัน SQL และคืนค่าเป็น DataFrame"""
try:
connection = sqlite3.connect(database_name)
result_df = pd.read_sql_query(sql_query, connection)
connection.close()
return result_df
except Exception as e:
return f"Database Error: {e}"
# ตรวจสอบและสร้าง Chat History ใน Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title('Gemini Chat with Database')

# แสดงประวัติการสนทนา
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# รับ Input
if prompt := st.chat_input("พิมพ์คำถามที่นี่..."):
    # เก็บและแสดงข้อความ User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # ประมวลผลและแสดงข้อความ Assistant
    with st.chat_message("assistant"):
        with st.spinner('กำลังหาคำตอบ...'):
            response = generate_summary_answer(prompt)
            st.markdown(response)

    # เก็บคำตอบลง Session
    st.session_state.messages.append({"role": "assistant", "content": response})
