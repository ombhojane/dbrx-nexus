
# DBRX Nexus AI

DBRX Nexus AI is a conversational AI application is designed to interact with users via natural language, generate SQL queries based on user queries, execute them against a database, and format the responses in a conversational manner.



## Features

- Natural Language Understanding: Converts user inputs into SQL queries.
- Database Interaction: Executes SQL queries on a database and retrieves relevant information.
- Response Formatting: Uses LLM to format database query results into conversational responses.
- Interactive UI: Built with Streamlit, providing a seamless user interaction interface.




## Installation

Clone the Repository:

```bash
  git clone https://github.com/ombhojane/dbrx-nexus.git
  cd dbrx-nexus
```

Install Dependencies:

```bash
  pip install streamlit sqlite3 google-generativeai
```
    
Set Environment Variables:
'GEMINI_API_KEY': Get Gemini API Key from aistudio

Run the Application:
```bash
  streamlit run app.py
```

## Usage/Examples

Start the application, and the Streamlit UI will be available in your web browser. Type a question related to the data in your SQLite database, and the application will:

- Generate an SQL query.
- Execute the query.
- Format the response in a user-friendly way.

## Live Demo

- https://huggingface.co/spaces/ombhojane/dbrx-nexus
- https://dbrx-nexus.streamlit.app/
