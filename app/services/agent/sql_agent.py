
from urllib.parse import quote_plus
from langchain.agents import create_sql_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_core.globals import set_debug
from langchain_core.messages import HumanMessage
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig
from app.utils.logger_service import LoggerService
from app.services.agent.prompt.sql_agent_general_prompt import SqlAgentGeneralPromptTemplate
 
class SqlAgent:
    
    # --------------------------------------------------------------------------------
    # Initialize the SQL agent
    # --------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None, verbose=False):
        try:
            self.logger = LoggerService.get_instance().get_logger(__name__)
            
            self.provider = provider or LLMConfig.PROVIDER
            self.model_name = model_name or LLMConfig.MODEL_NAME
            
            set_debug(verbose)
            self.create_db()            
            self.create_llm_agent()
            
        except Exception as e:
            self.logger.error(f"Error initializing SQL agent: {str(e)}")
            raise Exception("Initialization error: Please try again later.")
    
    
    # --------------------------------------------------------------------------------
    # Create database connection
    # --------------------------------------------------------------------------------
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
    
    

    # --------------------------------------------------------------------------------
    # Create LLM agent
    # --------------------------------------------------------------------------------
    def create_llm_agent(self):
        try:
            self.llm = LLMFactory.get_instance().get_llm(self.provider, self.model_name)
            self.tool_kit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            # Use ConversationBufferMemory to store chat history in memory
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            
            # Create custom prompt with SQL guidelines
            self.prefix = SqlAgentGeneralPromptTemplate.GetSqlAgentPrefix()
            self.suffix = SqlAgentGeneralPromptTemplate.GetSqlAgentSufix()
            
            self.agent = create_sql_agent(
                llm=self.llm,
                toolkit=self.tool_kit,
                verbose=True,
                memory=self.memory,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                prefix=self.prefix,
                suffix=self.suffix,
                agent_executor_kwargs=dict(handle_parsing_errors=True)
            )
        except Exception as e:
            self.logger.error(f"Error creating LLM agent: {str(e)}")
            raise Exception("LLM agent initialization error.")
    

    # --------------------------------------------------------------------------------    
    # Combine previous chat history with new question
    # --------------------------------------------------------------------------------
    def get_full_context(self, new_question: str) -> str:        
        conversation = ""
        for msg in self.memory.chat_memory.messages:
            conversation += f"{msg['role']}: {msg['content']}\n"
        conversation += f"user: {new_question}\n"
            
        return conversation if conversation else f"user: {new_question}\n"
    
        
    # --------------------------------------------------------------------------------
    # Execute user query
    # --------------------------------------------------------------------------------
    def invoke(self, state):
        try:
            # Extract the query from the last message in the state
            messages = state.get("messages", [])
            if not messages:
                return {"messages": [{"content": "No query provided."}]}
                
            # Get the query from the last message
            query = messages[-1].content
            
            # Use our existing implementation logic
            full_context = self.get_full_context(query)
            response = self.agent.invoke({"input": query, "chat_history": full_context})
            
            output = response.get("output", "Sorry, I couldn't process your request.")
            if "intermediate_steps" in response:
                for step in response["intermediate_steps"]:
                    if "observation" in step:
                        output = step["observation"]
            
            # Save to memory
            self.memory.chat_memory.messages.append({"role": "assistant", "content": output})
            
            # Return in the format expected by agent_node
            return {"messages": [HumanMessage(content=output)]}
            
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}")
            return {"messages": [HumanMessage(content=f"Sorry, I couldn't process your request: {str(e)}")]}