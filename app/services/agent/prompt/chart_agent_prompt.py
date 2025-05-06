import pyodbc
from typing_extensions import TypedDict
from typing import Annotated
from typing import List, Any
from langgraph.graph.message import add_messages
import pandas as pd


#--------------------------------------------------------------------------------
# ChatAgent class
#--------------------------------------------------------------------------------
class ChartAgentState(TypedDict):
    db: object
    context: dict
    user_input: str
    messages: Annotated[List[Any], add_messages]
    conn: pyodbc.Connection
    query_result: pd.DataFrame
    generated_sql: str
    plotly_json: str
    

#--------------------------------------------------------------------------------
# ChatAgentPrompts class
#--------------------------------------------------------------------------------
class ChartAgentPrompts:
    
    @staticmethod
    def get_agent_instruction() -> str:
        return f"""
            You are a helpful assistant with access to the following database tables and schema:
            {{table_info}}

            The user has asked the following question:
            "{{input}}"

            Your task is to generate a simple Microsoft SQL query that answers the user's question using the available tables.
            The SQL query should be directly related to the question and should only use the tables listed above.
            **General SQL Rules**
                - If the user mentions **'User'** (a reserved keyword), use square brackets: `SELECT * FROM [User]`, same for join statements.
                - When asked about **user's course attended** as well as the **courses that the user is missing*, consider:
                -- the *User.FK_Role_ID and Role.ID** to answer, 
                -- also notice that the Courses that User attended (or missed) are always related to the User's Role the user is assigned to. 
                -- The tables User, Course, Roles, Role_Course and User_Course have the relationship and data to answer that type of questions.            
                - When discribing the **user role**, use Role.Name instead of Role.ID.
                - **Do not use** `LIMIT` statements in SQL.
                - Round numerical answers to **two decimal places**.
                - **Avoid complex queries** (e.g., division inside queries).
                - Always **execute operations step by step**.
                - Use SQL Server-compatible syntax. Do not use backticks (`) for identifiers. Instead, use square brackets ([]) if necessary.
                - Please provide only the SQL query without any explanation or additional text.        
            """
    
    @staticmethod
    def get_chart_json(query_result_str, user_input) -> str:
        return f"""
        You are given the following data and a question. Based on the context and the data, generate the appropriate Plotly graph as a JSON object.

        Data context:
        {query_result_str}

        Question: {user_input}

        Instructions:
        1. Generate a Plotly graph in JSON format that best visualizes the provided data.
        2. Choose the most suitable chart type for the given data and question (e.g., bar chart, line chart, scatter plot, pie chart, etc.).
        3. Only return the JSON code for the Plotly graph, with no additional text, comments, or explanations.
        4. Ensure that all titles, axis labels, and chart settings are relevant and meaningful for the provided data and question.

        Provide only the JSON of the graph. No additional words or explanations are needed.
        Always make colorful graphs; there should be different colors in every graph.
        Don't write ```json
        """