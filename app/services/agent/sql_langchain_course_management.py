from urllib.parse import quote_plus
from langchain.agents import *
from urllib.parse import quote_plus
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_core.globals import set_verbose, set_debug
import logging
import os

# ---------------------------------------------------------------------------------------------------------
# This class is a wrapper for the SQL agent that is used to interact with the CourseManagement database.
# ---------------------------------------------------------------------------------------------------------
class sql_langchain_course_management:
    
        # ------------
        # Constructor 
        # ------------   
        def __init__(self, verbose = False):   
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
                return "Sorry, there was an error initializing the SQL assistant. Please try again later."

                    
        # ----------------
        # Create database
        # ----------------
        def create_db(self):
            try:
                self.server = "User-PC"
                self.database = "CourseManagement"
                self.conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
                self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(self.conn_str)}")
                self.db = SQLDatabase(self.engine)
                
            except Exception as e:
                self.logger.error(f"Error creating database connection: {str(e)}")
                return "Sorry, I couldn't connect to the database. Please check your connection settings."

            
        # ---------------------
        # Create LLM agent
        # ---------------------    
        def create_llm_agent(self):
            try:
                self.llm = ChatOpenAI(model="gpt-4")
                self.tool_kit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
                self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
                self.agent_executor = create_sql_agent(
                            llm=self.llm,
                            toolkit=self.tool_kit,
                            verbose=True,
                            memory=self.memory
                        )
                
            except Exception as e:
                self.logger.error(f"Error creating LLM agent: {str(e)}")
                return "Sorry, I couldn't initialize the AI assistant. Please try again later."


        # ---------------------
        # Talk to the agent
        # ---------------------
        def execute_query(self, query: str) -> str:
            try:
                response = self.agent_executor.invoke(query)
                return response['output']
            
            except Exception as e:
                self.logger.error(f"Error executing query: {str(e)}\nQuery: {query}")
                return "Sorry, I couldn't process your request. Please try rephrasing your question."