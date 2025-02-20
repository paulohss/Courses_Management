import os
import logging
from urllib.parse import quote_plus
from langchain.agents import create_sql_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_core.globals import set_verbose, set_debug

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
    
    
    # Create LLM agent
    def create_llm_agent(self):
        try:
            self.llm = ChatOpenAI(model="gpt-4")
            self.tool_kit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            # Use ConversationBufferMemory to store chat history in memory
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            self.agent_executor = create_sql_agent(
                llm=self.llm,
                toolkit=self.tool_kit,
                verbose=True,
                memory=self.memory
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
            
        if conversation == "":
           conversation = f"user: {new_question}\n"
        
        return conversation
    
    
    # Execute user query
    def execute_query(self, query: str) -> str:
        try:
            # Combine previous chat history with new question
            full_context = self.get_full_context(query)
            # Append and update memory with the new user query
            self.memory.chat_memory.messages.append({"role": "user", "content": query})
            # Use the combined context for the LLM call
            response = self.agent_executor.invoke(full_context)
            output = response.get('output', '')
            # Append assistant response to in-memory conversation history
            self.memory.chat_memory.messages.append({"role": "assistant", "content": output})
            return output
        
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}\nQuery: {query}")
            return "Sorry, I couldn't process your request."