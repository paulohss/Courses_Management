from urllib.parse import quote_plus
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain import hub
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from sqlalchemy import create_engine
from app.services.agent.prompt.sql_agent_general_prompt import SqlAgentGeneralPromptTemplate
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig
from app.utils.logger_service import LoggerService
from langchain.prompts import PromptTemplate


class MSSQL_Agent:

    #--------------------------------------------------------------------------------
    # Define the __init__ method to initialize the SQL agent
    #--------------------------------------------------------------------------------
    def __init__(self, provider, model_name):
        try:
            self.logger = LoggerService.get_instance().get_logger(__name__)
            
            self.provider = provider or LLMConfig.PROVIDER
            self.model_name = model_name or LLMConfig.MODEL_NAME
            
            self.llm = LLMFactory.get_instance().get_llm(self.provider, self.model_name)
            self.create_db()            
            self.tools = None
            self.prompt_template = None
            self.system_message = None
            self.agent_executor = None
            if self.db and self.llm:
                self.set_tools()
                self.set_prompts("mssql", 5)
                if self.system_message:
                   self.initialize_agent()
            
        except Exception as e:
            self.logger.error(f"Error initializing SQL agent: {str(e)}")
            raise Exception("Initialization error: Please try again later.")
        

    #--------------------------------------------------------------------------------
    # Define the create_db method to create a database connection
    #--------------------------------------------------------------------------------
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
        

    #--------------------------------------------------------------------------------
    # Define the set_tools method to set up the tools for the SQL agent
    #--------------------------------------------------------------------------------
    def set_tools(self):
        try:
            toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            self.tools = toolkit.get_tools()
        except Exception as e:
            self.logger.error(f"Error setting tools: {str(e)}")
            raise Exception("Error setting tools.")

    #--------------------------------------------------------------------------------
    # Define the set_prompts method to set up the prompts for the SQL agent
    #--------------------------------------------------------------------------------
    def set_prompts(self, dialect, top_k):
        try:
            # Define the SQL rules
            sql_rules = SqlAgentGeneralPromptTemplate.get_mssql_rules()

            # Create a proper PromptTemplate object
            self.prompt_template = SqlAgentGeneralPromptTemplate.get_mssql_agent_prompt_template()
            
            # Format the system message using the prompt template
            self.system_message = self.prompt_template.format(
                dialect=dialect,
                top_k=top_k,
                sql_rules=sql_rules,
                tables="List of tables will be dynamically added here"
            )
        except Exception as e:
            self.logger.error(f"Error setting prompts: {str(e)}")
            raise Exception("Error setting prompts.")

    #--------------------------------------------------------------------------------
    # Define the set_custom_system_message method to set a custom system message
    #--------------------------------------------------------------------------------
    def set_custom_system_message(self, custom_system_message):
        try:
            self.system_message = custom_system_message
        except Exception as e:
            self.logger.error(f"Error setting custom system message: {str(e)}")
            raise Exception("Error setting custom system message.")

    #--------------------------------------------------------------------------------
    # Define the initialize_agent method to create the agent executor
    #--------------------------------------------------------------------------------
    def initialize_agent(self):
        try:
            self.agent_executor = create_react_agent(self.llm, self.tools, prompt=self.system_message)
        except Exception as e:
            self.logger.error(f"Error initializing agent: {str(e)}")
            raise Exception("Error initializing agent.")

    #--------------------------------------------------------------------------------
    # Define the get_agent_executor method to get the agent executor
    #--------------------------------------------------------------------------------
    def answer(self, question):
        try:
            response = self.agent_executor.invoke({"messages": [{"role": "user", "content": question}]})
            self.logger.info(f"Response: {response}")
            return response["messages"][-1].content
        except Exception as e:
            self.logger.error(f"Error answering question: {str(e)}")
            raise Exception("Error answering question.")

    #--------------------------------------------------------------------------------
    # Define the answer_full method to get the full response from the agent executor
    #--------------------------------------------------------------------------------
    def answer_full(self, question):
        try:
            response = self.agent_executor.invoke({"messages": [{"role": "user", "content": question}]})
            self.logger.info(f"Response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error answering full question: {str(e)}")
            raise Exception("Error answering full question.")

    #--------------------------------------------------------------------------------
    # Define the invoke method to process the state and return a response
    #--------------------------------------------------------------------------------
    def invoke(self, state):
        try:
            # Extract the query from the last message in the state
            messages = state.get("messages", [])
            if not messages:
                return {"messages": [{"content": "No query provided."}]}
                    
            # Get the query from the last message
            question = messages[-1].content
            last_message = None

            response = self.agent_executor.invoke({"messages": [{"role": "user", "content": question}]})
            
            if response and isinstance(response, dict) and "messages" in response:
                last_message = response["messages"][-1].content
                self.logger.info(f"Response: {last_message}")

            if last_message:
                return {"messages": [HumanMessage(content=last_message)], "next": "FINISH"}
            else:
                return {"messages": [HumanMessage(content="The Sql Agent could not find an answer!")], "next": "FINISH"}
        except Exception as e:
            self.logger.error(f"Error invoking agent: {str(e)}")
            return {"messages": [HumanMessage(content=f"Error: {str(e)}")], "next": "FINISH"}

