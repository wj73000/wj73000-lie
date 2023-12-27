import streamlit as st
import pandas as pd
import sqlite3
import requests
from io import StringIO

def check_and_update_database(url, database_name, table_name):
    response = requests.get(url, timeout=10)
    data = StringIO(response.text)
    df_new = pd.read_csv(data)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    table_exists = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'").fetchone()

    if table_exists:
        df_existing = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        if not df_existing.equals(df_new):
            df_new.to_sql(table_name, conn, index=False, if_exists='replace')
            result = "【165假投資及博弈網站】已更新最新資料了！"
        else:
            result = "【165假投資及博弈網站】已經是最新資料！"
    else:
        df_new.to_sql(table_name, conn, index=False)
        result = "【165假投資及博弈網站】建立新資料庫，已更新完成！"

    conn.close()
    return result



if __name__ == "__main__":
   # 檢查並更新數據庫
   result_message = check_and_update_database(csv_url, database_name, table_name)
   print("最後修改日期:", result_message )