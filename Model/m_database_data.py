import streamlit as st
import os
from datetime import datetime

def database_data(): 
    # 資料庫文件路徑
    db_file_path = 'Model/165.db3'  # 替換為實際的 SQLite 資料庫文件路徑

    # 獲取最後修改時間戳
    last_modified_timestamp = os.path.getmtime(db_file_path)

    # 轉換為日期時間對象
    last_modified_date = datetime.fromtimestamp(last_modified_timestamp)

    # 將日期轉換為字串格式
    last_modified_str = last_modified_date.strftime('%Y-%m-%d %H:%M:%S')

    return last_modified_str