import streamlit as st
import pickle
import pandas as pd
import subprocess
import sys

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import xgboost and install if not available
try:
    import xgboost as xgb
except ImportError as e:
    install('xgboost')
    import xgboost as xgb

from datetime import datetime

# Function to load the model
@st.cache_resource
def load_model():
    try:
        model = pickle.load(open('uber_fare.pickle', 'rb'))
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load the model
model = load_model()

if model is not None:
    # Function to determine the time of day
    def get_time_of_day(hour):
        am_rush = 7 <= hour < 10
        pm_rush = 16 <= hour < 19
        daytime = 10 <= hour < 16
        nighttime = hour >= 19 or hour < 7
        return am_rush, pm_rush, daytime, nighttime

    # Define your input function
    def get_user_input():
        # Input fields
        time = st.text_input('Time (HH:MM)', '12:00')
        distance = st.number_input('Distance (in miles)', min_value=0.0, step=0.1)
        passenger_count = st.number_input('Passenger Count', min_value=1, step=1)

        # Process time input
        hour = int(time.split(':')[0])
        am_rush, pm_rush, daytime, nighttime = get_time_of_day(hour)

        # Create a dictionary of the inputs
        data = {
            'distance': distance,
            'passenger_count': passenger_count,
            'am_rush': am_rush,
            'pm_rush': pm_rush,
            'daytime': daytime,
            'nighttime': nighttime
        }
        features = pd.DataFrame(data, index=[0])
        return features

    # Streamlit app layout
    st.title('Uber Taxi Fare Prediction')

    # Get user input
    user_input = get_user_input()

    # Display user input
    st.subheader('User Input:')
    st.write(user_input)

    # Make predictions
    try:
        prediction = model.predict(user_input)
        st.subheader('Predicted Fare:')
        st.write(prediction)
    except Exception as e:
        st.error(f"Error making predictions: {e}")
else:
    st.error("Model could not be loaded.")
