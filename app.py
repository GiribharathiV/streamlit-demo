import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('house_data.csv')

# Call the function to load data
data = load_data()

# Standardize feature columns to lowercase for consistency
data['basement'] = data['basement'].str.lower()
data['airconditioning'] = data['airconditioning'].str.lower()
data['furnishingstatus'] = data['furnishingstatus'].str.lower()

# App Title
st.title("House Data Explorer")

# Sidebar filters
st.sidebar.header("Filter Options")

# Price Range Filter
price_range = st.sidebar.slider(
    "Price Range (in million)", 
    min_value=int(data['price'].min() / 1e6), 
    max_value=int(data['price'].max() / 1e6), 
    value=(
        int(data['price'].min() / 1e6), 
        int(data['price'].max() / 1e6)
    ),
    key="price_slider"
)
filtered_data = data[
    (data['price'] >= price_range[0] * 1e6) & 
    (data['price'] <= price_range[1] * 1e6)
]

# Area Range Filter
min_area, max_area = st.sidebar.slider(
    "Area Range (sq. ft.)",
    min_value=int(data['area'].min()),
    max_value=int(data['area'].max()),
    value=(
        int(data['area'].min()), 
        int(data['area'].max())
    ),
    key="area_slider"
)
filtered_data = filtered_data[
    (filtered_data['area'] >= min_area) & 
    (filtered_data['area'] <= max_area)
]

# Number of Stories Filter
stories = st.sidebar.multiselect(
    "Select Number of Stories", 
    options=sorted(data['stories'].unique()),
    default=data['stories'].unique(),  # All selected by default
    key="stories_multiselect"
)
if stories:
    filtered_data = filtered_data[filtered_data['stories'].isin(stories)]

# Feature Filters
features = {
    "Basement": "basement",
    "Air Conditioning": "airconditioning",
    "Furnishing Status": "furnishingstatus",
}
for feature_name, feature_col in features.items():
    options = sorted(data[feature_col].unique())
    selected_options = st.sidebar.multiselect(
        f"Select {feature_name}", 
        options=options, 
        default=options,  # Default to all options
        key=f"{feature_col}_multiselect"
    )
    filtered_data = filtered_data[filtered_data[feature_col].isin(selected_options)]

# Display filtered dataset
st.write(f"Showing {len(filtered_data)} houses:")
if st.checkbox("Show raw data", key="raw_data_checkbox"):
    st.write(filtered_data)

# Visualization: Price Distribution
st.subheader("Price Distribution")
st.bar_chart(filtered_data['price'])

# Visualization: Area vs Price
st.subheader("Area vs Price")
st.scatter_chart(data=filtered_data, x="area", y="price", use_container_width=True)

# Visualization: Feature Counts
st.subheader("Feature Counts")
feature = st.selectbox(
    "Choose a Feature to Analyze",
    options=features.keys(),
    key="feature_selectbox"
)
feature_col = features[feature]
feature_counts = filtered_data[feature_col].value_counts()
st.bar_chart(feature_counts)
