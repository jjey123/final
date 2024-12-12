import altair as alt
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(page_title="NBA Players Dataset", page_icon="🏀")

# Page title and description
st.title("🏀 NBA Players Dataset")
st.write(
    """
    This app visualizes player statistics from the NBA dataset.
    You can explore player performance based on their positions and ages!
    """
)

# Load the data from a CSV file and cache it for performance
@st.cache_data
def load_data():
    """Load NBA dataset."""
    return pd.read_csv("data/nba_data_processed.csv")

# Load the dataset
df = load_data()

# Widgets for user interaction
# Multiselect widget for selecting positions
positions = st.multiselect(
    "Select Positions:",
    options=df["Pos"].unique(),
    default=["C", "PG", "SG", "SF", "PF"],
)

# Slider widget for selecting a range of ages
ages = st.slider("Select Age Range:", 18, 40, (20, 30))

# Filter the dataframe based on user inputs
df_filtered = df[(df["Pos"].isin(positions)) & (df["Age"].between(ages[0], ages[1]))]

# Reshape the filtered data for visualization
df_reshaped = df_filtered.pivot_table(
    index="Age", columns="Pos", values="PTS", aggfunc="mean", fill_value=0
).sort_values(by="Age", ascending=True)

# Display the reshaped data as a table
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"Age": st.column_config.TextColumn("Age")},
)

# Prepare data for chart visualization
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="Age", var_name="Position", value_name="Average Points"
)

# Create and display an Altair line chart
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("Age:N", title="Age"),
        y=alt.Y("Average Points:Q", title="Average Points"),
        color=alt.Color("Position:N", title="Position"),
    )
    .properties(height=320, width=600)
    .configure_axisX(titleFontSize=14)
    .configure_axisY(titleFontSize=14)
    .configure_legend(labelFontSize=12)
)

# Render the chart
st.altair_chart(chart, use_container_width=True)
