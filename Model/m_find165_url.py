import streamlit as st
import sqlite3

 # 定義數據庫名稱、表名稱和列名稱
#database_name = '165.db3'
#table_name = 'url_table'
#column_name = 'WEBURL'

def search_database(input_string, database_name, table_name, column_name):
    # 建立到 SQLite 數據庫的連接
    conn = sqlite3.connect(database_name)

    # 準備 SQL 查詢
    query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"

    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query, ('%' + input_string + '%',))

    # 檢查結果
    results = cursor.fetchall()

    # 關閉連接
    conn.close()

    return results



if __name__ == "__main__":
    result_message = perform_165_url_search()
    print("最後修改日期:", result_message )