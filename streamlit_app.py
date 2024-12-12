!pip install matplotlib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the NBA player statistics dataset
url = "https://drive.google.com/file/d/1GLG5k17RLeeFgFWS-ISxkjubnUu1cHJj/view?usp=drive_link"  # Ensure this path is correct

# Load the dataset
try:
    data = pd.read_csv(url)
except FileNotFoundError:
    st.error("The dataset file was not found. Please check the file path.")
    st.stop()

# Streamlit app starts here
st.title("NBA Player Statistics Viewer")
st.write("Explore NBA player statistics with filtering and visualization tools.")

# Display the raw data
st.header("Dataset Overview")
st.write("Here's a preview of the dataset:")
st.dataframe(data)

# Check if necessary columns exist
if 'Age' not in data.columns or 'PTS' not in data.columns:
    st.error("The dataset must contain 'Age' and 'PTS' columns.")
    st.stop()

# Filter by age
st.sidebar.header("Filters")
min_age = st.sidebar.slider("Minimum Age", int(data["Age"].min()), int(data["Age"].max()), int(data["Age"].min()))
max_age = st.sidebar.slider("Maximum Age", int(data["Age"].min()), int(data["Age"].max()), int(data["Age"].max()))

# Filter the data
filtered_data = data[(data["Age"] >= min_age) & (data["Age"] <= max_age)]

st.header("Filtered Data")
st.write(filtered_data)

# Visualization: Points vs Age
st.header("Points vs Age")
fig, ax = plt.subplots()
ax.scatter(filtered_data["Age"], filtered_data["PTS"], c="blue", alpha=0.7)
ax.set_title("Points vs Age")
ax.set_xlabel("Age")
ax.set_ylabel("Points")
st.pyplot(fig)

# End of the app
st.write("---")
st.write("Built with Streamlit")



