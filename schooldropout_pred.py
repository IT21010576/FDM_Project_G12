import pickle
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import altair as alt
import matplotlib.pyplot as plt


st.set_page_config(page_title="Edufate", page_icon="🎓", layout="wide")


# loading the saved model
with open('C:/Users/DELL/Desktop/Miniproject/StudentDropout_Prediction_model.model', 'rb') as file:
    loaded_model = pickle.load(file)

# sidebar for navigation
# Define custom CSS for the sidebar
custom_css = """
<style>
#sidebar {
    background-color: #0077b6;  /* Background color - change as needed */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Add the sidebar with the specified styling
with st.sidebar:
    st.title("Predicting Educational Dropout")
    selected = option_menu('Navigation',
                           ['Prediction','Visualized Trends'],
                           icons=['mortarboard', 'bi bi-graph-up-arrow'],
                           default_index=0)

# Prediction page
if (selected == 'Prediction'):
    # page title
    st.markdown("<h1 style='font-size: 36px; font-weight: bold; color: #0077b6; text-align: left;'>Predicting whether a student will continue their current education</h1>", unsafe_allow_html=True)


    # Define a mapping for the categorical columns
    medu_mapping = {
        "none": 0,
        "4th grade": 1,
        "9th grade": 2,
        "12th grade": 3,
        "higher education": 4
    }

    mjob_mapping = {
        "at_home": 0,
        "teacher": 1,
        "services": 2,
        "health": 3,
        "other": 4
    }

    reason_mapping = {
        "course": 0,
        "other": 1,
        "home": 2,
        "reputation": 3
    }

    w_sTime_mapping = {
        "<2 hours": 0,
        "2 to 5 hours": 1,
        "5 to 10 hours": 2,
        ">10 hours": 3
    }

    ftime_mapping = {
        "scarce": 0,
        "limited": 1,
        "moderate": 2,
        "plenty": 3,
        "ample": 4
    }

    goingOut_mapping = {
        "very rarely": 0,
        "rarely": 1,
        "occasionally": 2,
        "regularly": 3,
        "daily": 4
    }

    Walc_mapping = {
        "very low": 0,
        "low": 1,
        "average": 2,
        "high": 3,
        "very high": 4
    }

    health_mapping = {
        "very bad": 0,
        "bad": 1,
        "average": 2,
        "good": 3,
        "very good": 4
    }

    # Function to create a styled dropdown for a categorical input
    # Function to create a dropdown for a categorical input
    def create_categorical_input_dropdown(mapping, input_label):
        options = [''] + list(mapping.keys())
        selected_option = st.selectbox(f'Select {input_label}:', options=options, key=input_label)
        encoded_value = mapping.get(selected_option, -1)
        return encoded_value
    
    # Custom CSS for styling the dropdown and text inputs
    custom_css = """
    <style>
    /* Style the dropdown and text inputs */
    div[data-baseweb="select"] {
        border: 2px solid #0077b6; /* Border color for dropdowns - change as needed */
        border-radius: 5px;
        background-color: #f0f0f0; /* Background color for dropdowns - change as needed */
        color: #333; /* Text color for dropdowns - change as needed */
        padding: 5px;
        font-size: 16px;
    }
    
    input[data-baseweb="input"] {
        border: 2px solid #0077b6; /* Border color for text inputs - change as needed */
        border-radius: 5px;
        background-color: #f0f0f0; /* Background color for text inputs - change as needed */
        color: #333; /* Text color for text inputs - change as needed */
        padding: 5px;
        font-size: 16px;
        font-weight: bold; /* Make text inputs bold */
    }
    /* Style the dropdown options */
    div[data-baseweb="menu"] {
        background-color: #f0f0f0; /* Background color of options - change as needed */
    }
    
    /* Style the selected option */
    div[data-baseweb="item"] {
        color: #0077b6; /* Selected option color - change as needed */
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Function to create a dropdown for a categorical input
    def create_categorical_input_dropdown(mapping, input_label):
        options = [''] + list(mapping.keys())
        selected_option = st.selectbox(f'Select {input_label}:', options=options, key=input_label)
        encoded_value = mapping.get(selected_option, -1)
        return encoded_value
    
    # Custom CSS for styling the dropdown and text inputs
    custom_css = """
    <style>
    /* Style the dropdown and text inputs */
    div[data-baseweb="select"] {
        border: 2px solid #0077b6; /* Border color for dropdowns - change as needed */
        border-radius: 5px;
        background-color: #f0f0f0; /* Background color for dropdowns - change as needed */
        color: #333; /* Text color for dropdowns - change as needed */
        padding: 5px;
        font-size: 16px;
    }
    
    input[data-baseweb="input"] {
        border: 2px solid #0077b6; /* Border color for text inputs - change as needed */
        border-radius: 5px;
        background-color: #f0f0f0; /* Background color for text inputs - change as needed */
        color: #333; /* Text color for text inputs - change as needed */
        padding: 5px;
        font-size: 16px;
        font-weight: bold; /* Make text inputs bold */
    }
    /* Style the dropdown options */
    div[data-baseweb="menu"] {
        background-color: #f0f0f0; /* Background color of options - change as needed */
    }
    
    /* Style the selected option */
    div[data-baseweb="item"] {
        color: #0077b6; /* Selected option color - change as needed */
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Encoding the input data from the user with the same style
    age_input = st.text_input("Enter Student's age*", key="age_input")
    medu_encoded = create_categorical_input_dropdown(medu_mapping, "Mother's education*")
    mjob_encoded = create_categorical_input_dropdown(mjob_mapping, "Mother's job*")
    reason_encoded = create_categorical_input_dropdown(reason_mapping, 'Reason for current education*')
    w_sTime_encoded = create_categorical_input_dropdown(w_sTime_mapping, 'Weekly Study Time*')
    pc_failures_input = st.text_input('Enter the number of failures encountered during the study time*', key="pc_failures_input")
    ftime_encoded = create_categorical_input_dropdown(ftime_mapping, "Student's free time*")
    goingOut_encoded = create_categorical_input_dropdown(goingOut_mapping, 'Frequency of going out*')
    Walc_encoded = create_categorical_input_dropdown(Walc_mapping, 'Weekend Alcohol Consumption*')
    health_encoded = create_categorical_input_dropdown(health_mapping, "Student's Health Status*")


    feature_names = ['age', 'medu', 'mjob', 'reason', 'w_sTime', 'pc_failures', 'ftime', 'goingOut', 'Walc', 'health']

    # Creating a button for Prediction
    if st.button('Display Prediction'):
        if age_input and medu_encoded != -1 and mjob_encoded != -1 and reason_encoded != -1 and w_sTime_encoded != -1 and pc_failures_input and ftime_encoded != -1 and goingOut_encoded != -1 and Walc_encoded != -1 and health_encoded != -1:
            # Prepare the input data as a DataFrame
            input_data_dict = pd.DataFrame({
                'age': np.array([int(age_input)], dtype='int32'),
                'medu': np.array([medu_encoded], dtype='int32'),
                'mjob': np.array([mjob_encoded], dtype='int32'),
                'reason': np.array([reason_encoded], dtype='int32'),
                'w_sTime': np.array([w_sTime_encoded], dtype='int32'),
                'pc_failures': np.array([int(pc_failures_input)], dtype='int32'),
                'ftime': np.array([ftime_encoded], dtype='int32'),
                'goingOut': np.array([goingOut_encoded], dtype='int32'),
                'Walc': np.array([Walc_encoded], dtype='int32'),
                'health': np.array([health_encoded], dtype='int32')
            })

            # You can pass the input data to your XGBoost model for prediction
            input_data_array = input_data_dict.to_numpy()
            input_data_array = input_data_array.reshape(1, -1)  # Ensure it's 2D for a single sample

            # Use the loaded model for prediction
            prediction = loaded_model.predict(input_data_array)

            # Convert prediction to a float and format it
            prediction = float(prediction)
            result = '🚀 Student is NOT a DROPOUT! 🌟' if prediction == 0.0 else '🚨 Student is a DROPOUT 😥'
            st.write(f'Predicted Outcome: {result}')
            
            # Add space between prediction and the visual
            st.write("")
            st.write("")
            st.write("")
            
            # Calculate feature importances
            importance_scores = loaded_model.feature_importances_
            feature_names = ['age', 'medu', 'mjob', 'reason', 'w_sTime', 'pc_failures', 'ftime', 'goingOut', 'Walc', 'health']
    
            # Create a DataFrame to store feature importances
            feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance_scores})
    
            # Sort the features by importance in descending order
            feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
            # Create a horizontal bar chart to display feature importance
            chart = alt.Chart(feature_importance_df).mark_bar().encode(
                x=alt.X('Importance:Q', title='Importance'),
                y=alt.Y('Feature:N', title='Feature', sort='-x'),
                color=alt.value('lightblue')
            ).properties(
                width=600,
                height=400,
                title='Feature Importance'
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Display the key below the visual
            st.write("Key:")
            st.write("- Age: Student's age")
            st.write("- Medu: Mother's education")
            st.write("- Mjob: Mother's job")
            st.write("- Reason: Reason for current education")
            st.write("- w_sTime: Weekly Study Time")
            st.write("- pc_failures: Number of failures encountered during the study time")
            st.write("- ftime: Student's free time")
            st.write("- goingOut: Frequency of going out")
            st.write("- Walc: Weekend Alcohol Consumption")
            st.write("- Health: Student's Health Status")

        else:
            st.error('Please fill in all mandatory input fields.')
    
if(selected == 'Visualized Trends'):
    # Load historical data
    file_path = "C:/Users/DELL/Desktop/Miniproject/SchoolDropout.csv"
    data = pd.read_csv(file_path)
    
 
     # Allow the user to select a feature for analysis
    selected_feature = st.selectbox("Select Feature", data.columns)

    # Allow the user to choose the type of visualization
    visualization_type = st.selectbox("Select Visualization Type", ["Line Chart", "Bar Chart", "Pie Chart"])

    # Display the chart only after the button is clicked
    if st.button('Display Trends'):
        # Create a new DataFrame to aggregate data based on the selected_feature and the dropout column
        aggregated_data = data.groupby([selected_feature, 'dropout']).size().unstack().fillna(0)

        if visualization_type == "Line Chart":
            # Create a line chart to show trends over the selected x-axis
            aggregated_data.plot(kind="line")
            plt.xlabel(selected_feature)
            plt.ylabel("Number of Dropouts")
            plt.title(f"Dropout Trends by {selected_feature}")
            st.pyplot(plt)

        elif visualization_type == "Bar Chart":
            # Create a bar chart to visualize dropout counts
            aggregated_data.plot(kind="bar", stacked=True)
            plt.xlabel(selected_feature)
            plt.ylabel("Number of Students")
            plt.title(f"Student Counts and Dropouts by {selected_feature}")
            st.pyplot(plt)

        elif visualization_type == "Pie Chart":
            # Create a pie chart to visualize dropout percentages
            dropout_percentages = aggregated_data.iloc[:, 1] / (aggregated_data.iloc[:, 0] + aggregated_data.iloc[:, 1]) * 100
            st.write(dropout_percentages)
            plt.pie(dropout_percentages, labels=dropout_percentages.index, autopct='%1.1f%%', startangle=90)
            plt.title(f"Dropout Percentage by {selected_feature}")
            st.pyplot(plt)