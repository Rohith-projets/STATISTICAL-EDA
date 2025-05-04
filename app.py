import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import chardet
from REL import *
from DIS import *
from CAT import *
from REG import *
from REL import *
# Function to detect file encoding
def detect_encoding(file):
    raw_data = file.read()
    file.seek(0)  # Reset file pointer to the beginning
    result = chardet.detect(raw_data)
    return result['encoding']

# Function to read uploaded file into a DataFrame
def read_file(file, encoding):
    try:
        if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file.type == "application/vnd.ms-excel":
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file, encoding=encoding)
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# Main function for the Streamlit app
def main():
    st.title("Seaborn Visualization App")
    # Sidebar for file upload
    with st.sidebar:
        st.header("Upload Data")
        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
        if uploaded_file is not None:
            # Detect encoding and read file
            encoding = detect_encoding(uploaded_file)
            df = read_file(uploaded_file, encoding)
            if df is not None:
                st.success("File successfully loaded!")
                st.write("Data Preview:")
                st.dataframe(df.head())
                # Option menu for selecting chart types
                selected_chart = option_menu(
                    "Select Chart Type",["Relational Plots","Distribution Plots","Categorical Plots","Regression Plots", "Matrix Plots",],
                    icons=["graph-up", "bar-chart", "box", "regression", "grid"],
                    menu_icon="cast",
                    default_index=0,
                )

    if uploaded_file is not None and df is not None:
        # Relational Plots
        if selected_chart == "Relational Plots":
            st.subheader("Relational Plots")
            chart_type = st.selectbox("Select Chart", ["Scatter Plot", "Line Plot","Relational Plot"])
            if chart_type=="Scatter Plot":
                show_scatterplot(df)
            elif chart_type=="Line Plot":
                show_lineplot(df)
            else:
                show_relplot(df)

        # Distribution Plots
        elif selected_chart == "Distribution Plots":
            st.subheader("Distribution Plots")
            chart_type = st.selectbox("Select Chart", ["Histogram", "KDE Plot", "ECDF Plot","Displot","Rugplot"])
            if chart_type=="Histogram":
                show_histplot(df)
            if chart_type=="KDE Plot":
                show_kdeplot(df)
            if chart_type=="ECDF Plot":
                show_ecdfplot(df)
            if chart_type=="Displot":
                show_displot(df)
            if chart_type=="Rugplot":
                show_rugplot(df)
            
        # Categorical Plots
        elif selected_chart == "Categorical Plots":
            st.subheader("Categorical Plots")
            chart_type = st.selectbox("Select Chart", ["boxplot","catplot","stripplot","swarmplot","boxplot","violinplot","boxenplot","pointplot","barplot","countplot"])
            if chart_type:
                eval(f'show_{chart_type}(df)')
        # Regression Plots
        elif selected_chart == "Regression Plots":
            st.subheader("Regression Plots")
            chart_type = st.selectbox("Select Chart", ["lmplot", "regplot"])
            if chart_type:
                eval(f'show_{chart_type}(df)')

        # Matrix Plots
        elif selected_chart == "Matrix Plots":
            st.subheader("Matrix Plots")
            chart_type = st.selectbox("Select Chart", ["heatmap", "clustermap"])
            if chart_type:
                eval(f'show_{chart_type}(df)')

main()
