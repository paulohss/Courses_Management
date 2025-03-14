import os
import logging
import textwrap
from urllib.parse import quote_plus
from langchain.agents import create_sql_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_core.globals import set_verbose, set_debug
from langchain.prompts import MessagesPlaceholder

class sql_langchain_course_management:
    
    # Initialize the SQL agent
    def __init__(self, verbose=False):
        try:
            # Configure logging
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            logging.basicConfig(
                filename=os.path.join(log_dir, 'sql_agent.log'),
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
            
            set_debug(verbose)
            self.create_db()
            self.create_llm_agent()
            
        except Exception as e:
            self.logger.error(f"Error initializing SQL agent: {str(e)}")
            raise Exception("Initialization error: Please try again later.")
    
    
    # Create database connection
    def create_db(self):
        try:
            self.server = "User-PC"
            self.database = "CourseManagement"
            self.conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(self.conn_str)}")
            self.db = SQLDatabase(self.engine)
        except Exception as e:
            self.logger.error(f"Error creating database connection: {str(e)}")
            raise Exception("Database connection error.")
    
    
    # Get SQL agent suffix with guidelines for SQL generation
    def GetSqlAgentPrefix(self) -> str:
        return textwrap.dedent("""\
            You are a Microsoft SQL Server expert assistant for a **Course Management Database**.
            While generating Microsoft SQL Server for the user's query, follow these instructions:

            **General SQL Rules**
            - If the user mentions **'User'** (a reserved keyword), use square brackets: `SELECT * FROM [User]`, same for join statements.
            - When asked about **user's course attended** as well as the **courses that the user is missing*, consider the *User.FK_Role_ID** to answer, notice that the Courses the *User should attend are always related to the Role* the user is assigned to. The tables User, Course, Roles, Role_Course and User_Course have the relationship and data to answer that type of questions.            
            - **Do not use** `LIMIT` statements in SQL.
            - Round numerical answers to **two decimal places**.
            - **Avoid complex queries** (e.g., division inside queries).
            - Always **execute operations step by step**.
            **Query Interpretation**
            - **Strictly follow all conditions** in the query. **Do not infer extra conditions**.            
            - **YTD (Year to Date)** should be interpreted correctly.            

            """)


    # Get SQL agent suffix with guidelines for SQL generation
    #  When using AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    #  - the agent follows a Thought → Action → Observation → Thought cycle.
    #  The agent_scratchpad: 
    #  - The scratchpad is a place where the agent can write down notes or thoughts that it has while working on a problem.
    #  - The agent writes down its thoughts and chosen actions before executing them.
    #  - After execution, it records observations and updates its reasoning accordingly.
    def GetSqlAgentSufix(self) -> str:
        return textwrap.dedent("""\
                Begin!
                {chat_history}
                Question: {input}
                Thought: Let's think step by step. {agent_scratchpad}"
        """)


    # Create LLM agent
    def create_llm_agent(self):
        try:
            self.llm = ChatOpenAI(model="gpt-4")
            self.tool_kit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            # Use ConversationBufferMemory to store chat history in memory
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            
            # Create custom prompt with SQL guidelines
            self.prefix = self.GetSqlAgentPrefix()
            self.suffix = self.GetSqlAgentSufix()
            
            self.agent_executor = create_sql_agent(
                llm=self.llm,
                toolkit=self.tool_kit,
                verbose=True,
                memory=self.memory,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                prefix=self.prefix,
                suffix=self.suffix
            )
        except Exception as e:
            self.logger.error(f"Error creating LLM agent: {str(e)}")
            raise Exception("LLM agent initialization error.")
    
    
    # Combine previous chat history with new question
    def get_full_context(self, new_question: str) -> str:        
        conversation = ""
        for msg in self.memory.chat_memory.messages:
            conversation += f"{msg['role']}: {msg['content']}\n"
        conversation += f"user: {new_question}\n"
            
        return conversation if conversation else f"user: {new_question}\n"
    
    
    # Execute user query
    def execute_query(self, query: str) -> str:
        try:
            full_context = self.get_full_context(query)
            response = self.agent_executor.invoke({"input": query, "chat_history": full_context})

            output = response.get("output", "Sorry, I couldn't process your request.")
            if "intermediate_steps" in response:
                for step in response["intermediate_steps"]:
                    if "observation" in step:
                        output = step["observation"]

            self.memory.chat_memory.messages.append({"role": "assistant", "content": output})
            return output
        
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}\nQuery: {query}")
            return "Sorry, I couldn't process your request."