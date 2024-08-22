import os
import gspread  # Corrected import statement
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:\\ANGLE\\python project\\yasaranglebelearn-db34409d3f0c.json"

# Define the scope and credentials for accessing Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), scope)
client = gspread.authorize(creds)


# Access the specific Google Sheets document by its spreadsheet ID
spreadsheet_id = "1_2rAj3WIYH5dswTwm2SZZwZITS5GoLuBSupLdKQaGrI"  # Replace with your actual spreadsheet ID
spreadsheet = client.open_by_key(spreadsheet_id)

# Access a specific worksheet by its ID (gid)
worksheet = spreadsheet.get_worksheet_by_id(106742000)  # Replace with your actual gid

# Fetch all values from the sheet and convert them to a DataFrame
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])  # Skip the header row in the data

# Streamlit App Interface
st.title("Teacher's Data Dashboard")

# Display the DataFrame


# Filter the DataFrame
st.subheader('Filter Data')
columns = df.columns.to_list()  # Get the list of columns

selected_columns = st.multiselect('Select columns to filter by', columns)  # Allow multiple column selections

filtered_df = df.copy()  # Create a copy of the DataFrame to apply filters

for column in selected_columns:
    unique_values = filtered_df[column].unique()  # Get unique values for the selected column
    selected_value = st.selectbox(f'Select value for {column}', unique_values)
    filtered_df = filtered_df[filtered_df[column] == selected_value]  # Apply filter for each column

# Drop the filtered columns before displaying the result (if you want to hide filtered columns)
filtered_df = filtered_df.drop(columns=selected_columns)

# Display the filtered DataFrame
st.subheader('Filtered Data')
st.write(filtered_df)
