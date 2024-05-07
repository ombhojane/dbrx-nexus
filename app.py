import streamlit as st
import google.generativeai as genai
import sqlite3


def connect_to_database(db_path):
    # debugging
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Running a test query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("Connection successful. Found tables:", tables)
        else:
            print("Connection successful but no tables found.")
        
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Connect to the database
db_connection = connect_to_database('phones.db')

st.set_page_config(layout="wide")
MODEL_AVATAR_URL = "./icon.png"

GEMINI = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

DESCRIPTION = """
This app demonstrates how to use the DBRX Nexus AI to enhance customer experience by providing conversational responses to user queries. 
The app uses the DBRX model to generate SQL queries based on user questions and then executes the queries to retrieve information from a database. 
The retrieved information is then formatted into a conversational response and displayed to the user.

This is DBRX Nexus AI powered chatbot for Electronics Store. You can ask questions about products, brands, storage, color, price, and much more!
"""

st.title("Enhancing Customer Experience with Nexus")

st.markdown(DESCRIPTION)


with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def clear_chat_history():
    st.session_state["messages"] = []

st.button('Clear Chat', on_click=clear_chat_history)


# Function to generate SQL query
def generate_sql_query(user_input):
    prompt = f"Generate an SQL query to find information based on the user's question: '{user_input}'. Note: The table name is 'phones' and the columns are 'ProductName', 'Brand', 'Storage', 'Color', 'Price', 'QuantityInStock', and 'Location'. Note: GIve the query without '''sql at the start and end of the query. just give the query text content"
    response = model.generate_content(prompt)
    print(response.text)
    return response.text 

def execute_sql_query(query):
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        print(results)
        return results
    except Exception as e:
        return f"Error executing query: {str(e)}"

def format_response(user_input, query_results):
    if not query_results:
        return "No data found for your query."

    result_text = f"Found {len(query_results)} results: " + ', '.join([str(item) for sublist in query_results for item in sublist])
    
    prompt = f"Rephrase this in a more conversational and informative way based on the user's question: '{user_input}'. Here are the details: {result_text}. Answer the user's question in a conversational manner. Note: as its a conversational response, give the response in correct mannser with correct formatting"
    formatted_response = model.generate_content(prompt)
    print(formatted_response.text)
    return formatted_response.text

EXAMPLES = [
    "What colors do iPhones come in?",
    "How much does the Samsung Galaxy cost?",
    "Show me all products with more than 128GB of storage",
    "List all products under $500"
]
with st.sidebar:
    with st.container():
        st.title("Example Queries")
        for prompt in EXAMPLES:
            st.button(prompt, on_click=lambda prompt=prompt: handle_user_input(prompt))

def handle_user_input(user_input):
    with history:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate SQL query from user input
        sql_query = generate_sql_query(user_input)
        if sql_query:
            # Execute the generated SQL query
            query_results = execute_sql_query(sql_query)
            formatted_answer = format_response(user_input, query_results)
            
            with st.chat_message("assistant", avatar=MODEL_AVATAR_URL):
                st.markdown(formatted_answer)
                st.session_state["messages"].append({"role": "assistant", "content": formatted_answer})
        else:
            with st.chat_message("assistant", avatar=MODEL_AVATAR_URL):
                st.markdown("Failed to generate a valid SQL query.")
                st.session_state["messages"].append({"role": "assistant", "content": "Failed to generate a valid SQL query."})


main = st.container()
with main:
    history = st.container(height=400)
    with history:
        for message in st.session_state["messages"]:
            avatar = None
            if message["role"] == "assistant":
                avatar = MODEL_AVATAR_URL
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("Type your question:", max_chars=1000):
        handle_user_input(prompt)
