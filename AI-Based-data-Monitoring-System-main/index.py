import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
# Load data from a file
def load_data(file_path):

  return pd.read_csv(file_path)
def check_null_values (df):

  return df.isnull().sum()
def check_duplicates (df):

 return df.duplicated().sum()
def detect_anomalies(df, columns):
 
 df_numeric = df [columns].select_dtypes(include=[np.number])
 if df_numeric.empty:
    return pd.DataFrame() # Return empty DataFrame if no numeric columns
# Handle missing values: Fill NaNs with the median of each column
 df_numeric.fillna(df_numeric.median(), inplace=True)
 model =IsolationForest(contamination=0.05, random_state=42)
 df_numeric['anomaly'] = model.fit_predict(df_numeric)
 anomalies= df[df_numeric['anomaly'] == -1] # Use df_numeric for filtering
 return anomalies
# Streamlit UI
st.title("AI-Based Data Quality Monitoring")
# Upload File
uploaded_file= st.file_uploader("Upload CSV File", type=["csv", "xlsx"])
if uploaded_file:
 file_path = uploaded_file.name
 data= load_data(uploaded_file)
 st.subheader(" Data Preview")
 st.dataframe(data.head())
# Perform Data Quality Checks
 null_values = check_null_values(data)
 st.subheader(" Missing Values")
 st.write(null_values)
# Bar Chart for Missing Values
 st.subheader("Missing Values Visualization")
 fig, ax = plt.subplots()
 sns.barplot(x=null_values.index, y=null_values.values, ax=ax, palette="coolwarm")
 ax.set_ylabel("Count")
 ax.set_title("Missing Values Per Column")
 st.pyplot(fig)
# Duplicate Rows
 duplicates= check_duplicates(data)
 st.subheader("Duplicate Rows")
 st.write(f"Total Duplicates: {duplicates}")
#MPie Chart for Duplicates
 st.subheader("Duplicate Rows Distribution")
 fig, ax= plt.subplots()
 labels = ["Unique Rows", "Duplicates"]
 values= [len(data)- duplicates, duplicates]
 ax.pie(values, labels= labels, autopct="%1.1f%%", colors=["skyblue", "red"])
 st.pyplot(fig)
# Anomaly Detection
 st.subheader(" Select Columns for Anomaly Detection")
 selected_columns = st.multiselect("Choose Numeric Columns", data.select_dtypes (include=[np.number]).columns)
 if selected_columns:
  anomalies =detect_anomalies (data, selected_columns)
  st.subheader(" Detected Anomalies")
  st.dataframe(anomalies)
#Box Plot for Anomalies
  st.subheader(" Anomaly Detection Visualization")
  fig, ax = plt.subplots (figsize=(8, 5))
  sns.boxplot(data=data[selected_columns], ax=ax, palette="Set2")
  ax.set_title("Box Plot for Outlier Detection")
  st.pyplot(fig)