import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/suraksha_setu.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()

st.dataframe(df)   # shows table with scroll + filters

# import streamlit as st
# import sqlite3

# DB_PATH = "database/suraksha_setu.db"

# conn = sqlite3.connect(DB_PATH)
# cursor = conn.execute("PRAGMA table_info(feedback);")
# for col in cursor.fetchall():
#     st.write(col)
# conn.close()






# import streamlit as st
# import sqlite3

# def delete_report(report_id):
#     conn = sqlite3.connect("database/incidents.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
#     conn.commit()
#     conn.close()

# st.title("Delete Report")

# report_id = st.number_input("Enter Report ID to delete", min_value=1, step=1)

# if st.button("Delete"):
#     delete_report(report_id)
#     st.success(f"Deleted report ID {report_id}")




