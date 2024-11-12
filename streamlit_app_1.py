import invoke_agent as agenthelper
import streamlit as st
import json
import pandas as pd

# Streamlit page configuration
## st.set_page_config(page_title="Co. Portfolio Creator", page_icon=":robot_face:", layout="wide")

# Title
## st.title("Co. Portfolio Creator")

# Display a text box for input
## prompt = st.text_input("Please enter your query?", max_chars=2000)
## prompt = prompt.strip()

# Display a primary button for submission
## submit_button = st.button("Submit", type="primary")

# Display a button to end the session
## end_session_button = st.button("End Session")

# ------------------- Create Sidebar Chat ----------------------

# Increase the default width of the main area by 50%
st.set_page_config(layout="wide")

# stSidebarContent
# stAppViewContainer
page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    # background-image: url("https://img.freepik.com/premium-vector/sky-blue-gradient-web-brochure-template-background-illustration-simple-plain-background_784842-323.jpg");
    background-color: #f8f8fa;
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    </style>
    """
with st.sidebar:
    st.markdown("")
    st.subheader('**_How_ _to_ _Use:_**', divider="blue")
    st.write('''
    1. 📄 Upload relevant files in CSV format (maximum 10 files).
    
    ''')
    st.markdown("")
    st.markdown("")
    uploaded_files = st.file_uploader("Upload Files (e.g. production data, maintenance log, quality log, customer data, etc.). (.csv)", type=("csv"), accept_multiple_files=True)
    st.markdown("")
    st.markdown("")
    st.write('''
    2. Wait for the files to upload.
    
    3. Ask Questions! 📊

    ''')
    st.markdown("")
    st.subheader("_Example_ _Use_ _Case_", divider="blue")
    st.write('''
        Upload wastage and maintenance data files to do root cause analysis of your production waste
    ''')
    st.markdown("")
    end_session_button = st.button("End Session")
    st.markdown("")

# st.header("Start asking questions about your business data", divider="gray")
# First Row - Buttons (Using Columns)
col1, col2 = st.columns(2)  # Create two columns

with col1:
    st.markdown(
        """
        <button style="
            background-color: #d7ecff; /* Primary blue color */
            color: black;
            padding: 10px 15px;
            border: 2px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
            cursor: pointer;
            width: 100%; /* Make button take full width of column */
            margin: 0 5px;
        "><b>_Text2DataAnalysis_</b> Co-Pilot</button>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <a href="https://processdatav2.vercel.app/" target="_blank">
            <button style="
                background-color: #f6f5fd; /* Transparent background for outline */
                color: black; /* Primary blue color for text */
                padding: 10px 15px;
                border: 2px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s ease, color 0.3s ease; /* Hover effects */
                cursor: pointer;
                width: 100%; /* Make button take full width of column */
                margin: 0 5px;
            "> <b>Click here</b> for other AI Co-Pilots</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Second Row - Header
st.markdown(
    """
    <h2>Start asking questions about your business data</h2>
    <hr style="border-top: 1px solid gray; margin-top: 10px;">
    """,
    unsafe_allow_html=True,
)

# Display a button to end the session
# end_session_button = st.button("End Session")

# Session State Management for History
if 'history' not in st.session_state:
    st.session_state['history'] = []

user_query = st.chat_input(placeholder="Ask me anything about your data!")

# Function to parse and format response
def format_response(response_body):
    try:
        # Try to load the response as JSON
        data = json.loads(response_body)
        # If it's a list, convert it to a DataFrame for better visualization
        if isinstance(data, list):
            return pd.DataFrame(data)
        else:
            return response_body
    except json.JSONDecodeError:
        # If response is not JSON, return as is
        return response_body

# Handling user input and sending to agent
if user_query:
    st.session_state['history'].append({"question": user_query, "answer": "..."})  # Placeholder for initial answer
    
    event = {
        "sessionId": "MYSESSION",
        "question": user_query
    }

    # Call to the agent (adjusting as per the original code structure)
    response = agenthelper.lambda_handler(event, None)

    try:
        # Parse and format the response as needed
        if response and 'body' in response and response['body']:
            response_data = json.loads(response['body'])
            all_data = format_response(response_data['response'])
            the_response = response_data['trace_data']
        else:
            print("Invalid or empty response received")
            all_data = "Error: No response"
            the_response = "Apologies, an error occurred"

    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        all_data = "Error: Invalid response format"
        the_response = "Apologies, an error occurred"

    # Display formatted response and trace data
    st.sidebar.text_area("Formatted Response", value=all_data, height=300)
    # Display previous chat messages
    for message in st.session_state['history']:
        st.write(message)
    # Append the new message to the chat history
    st.session_state['history'].append(user_input)
    st.session_state['history'].append(response)
    #st.session_state['history'].append({"question": user_query, "answer": the_response})

    st.session_state['trace_data'] = the_response
    st.write(the_response)  # Display the response to the user

# If session is ended
if end_session_button:
    st.session_state['history'].append({"question": "Session Ended", "answer": "Thank you for using AnyCompany Support Agent!"})
    event = {
        "sessionId": "MYSESSION",
        "question": "placeholder to end session",
        "endSession": True
    }
    agenthelper.lambda_handler(event, None)
    st.session_state['history'].clear()
