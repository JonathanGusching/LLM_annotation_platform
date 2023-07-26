# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account

from shillelagh.backends.apsw.db import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(":memory:",adapter_kwargs={"gsheetsapi": {"service_account_info":dict(st.secrets["gcp_service_account"])}})
print(st.secrets)
print(credentials)
# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=10)
def run_query(query):
    rows = conn.execute(query)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]

#conn.execute(f'INSERT INTO "{sheet_url}"\nVALUES ("Sara", "Bird")')

rows = run_query(f'SELECT * FROM "{sheet_url}"')

print(rows)

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")