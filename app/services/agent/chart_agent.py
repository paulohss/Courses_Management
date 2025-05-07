import json
import pandas as pd
import pandas as pd
import pyodbc
from langchain.sql_database import SQLDatabase
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.prompts import PromptTemplate
from app.services.llm.llm_factory import LLMFactory
from langchain_core.messages import HumanMessage
from app.utils.logger_service import LoggerService
from app.services.llm.llm_setting import LLMConfig
from app.services.agent.prompt.chart_agent_prompt import ChartAgentState, ChartAgentPrompts

#--------------------------------------------------------------------------------
# ChatAgent class
#--------------------------------------------------------------------------------
class ChartAgent:
    
    #--------------------------------------------------------------------------------
    # Initialize the EmailAgent
    #--------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None):
        try:
            self.logger = LoggerService.get_instance().get_logger(__name__)    
            # Use config if not provided
            provider = provider or LLMConfig.PROVIDER
            model_name = model_name or LLMConfig.MODEL_NAME

            # Get LLM from factory
            self.llm = LLMFactory.get_instance().get_llm(provider, model_name)
            self.build_langgraph()
            
        except Exception as e:
            self.logger.error(f"Error initializing ChatAgentState: {e}")
            raise

    #--------------------------------------------------------------------------------
    # Initialize the ChatAgentState
    #--------------------------------------------------------------------------------
    def connect_to_database(self, state: ChartAgentState):
        try:            
            self.logger.info("connect_to_database STARTING")            
            db_type = "SQL Server"
            server = "User-PC"  # Replace with your server name
            database = "CourseManagement"  # Replace with your database name
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

            # Establish connection
            state["db_type"] = db_type
            state["conn"] = pyodbc.connect(conn_str)
            state["db"] = SQLDatabase.from_uri(f"mssql+pyodbc:///?odbc_connect={conn_str}")
            state["context"] = state["db"].get_context()
            self.logger.info(f"Connected to {db_type} database.")
            
            return state
            
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            


    #--------------------------------------------------------------------------------
    # Build the language graph for the agent
    #--------------------------------------------------------------------------------
    def build_langgraph(self):
        try:
            graph_builder = StateGraph(ChartAgentState)
            
            graph_builder.add_node("connect_to_database", self.connect_to_database)
            graph_builder.add_node("run_query", self.run_query)
            graph_builder.add_node("generate_plotly_graph", self.generate_plotly_graph)
            
            graph_builder.add_edge(START, "connect_to_database")
            graph_builder.add_edge("connect_to_database", "run_query")
            graph_builder.add_edge("run_query", "generate_plotly_graph")
            graph_builder.add_edge("generate_plotly_graph", END)
            
            self.graph = graph_builder.compile()
            self.logger.info("Language graph built successfully.")
            
        except Exception as e:
            self.logger.error(f"Error building language graph: {e}")
            raise


    #--------------------------------------------------------------------------------
    # Run SQL query based on user input
    #--------------------------------------------------------------------------------        
    def run_query(self, state: ChartAgentState):
        try:
            self.logger.info("run_query STARTING")
            user_input = state["user_input"]            

            prompt = PromptTemplate(
                template=ChartAgentPrompts.get_agent_instruction(),
                input_variables=["input", "table_info"],
            )

            _input = prompt.format_prompt(input=user_input, table_info=state["context"]["table_info"])
            output = self.llm.invoke(_input.to_string())

            c = state["conn"].cursor()
            query = output.content.strip()  # Ensure the query is clean

            # Debug: Log the generated query
            self.logger.info(f"Generated Query: {query}")

            # Replace backticks with square brackets (if any)
            query = query.replace("`", "").replace("`", "").replace("sql", "")

            self.logger.info(f"Sanitized Query: {query}")

            # Execute the query
            c.execute(query)
            columns = [description[0] for description in c.description]
            results = c.fetchall()
            self.logger.info(f"Query Results: {results}")
            self.logger.info(f"Query Columns: {columns}")
                    
            # Validate columns and results
            if not columns or not results:
                raise ValueError("No data returned from the query.")
            
            # Create a dictionary to hold the column data
            dict_data = {}
            for i, col in enumerate(columns):
                col_data = [row[i] for row in results]
                dict_data[col] = col_data
            
            self.logger.info(f"Dictionary Data: {dict_data}")
            # Create DataFrame from the dictionary
            df = pd.DataFrame(dict_data)
            
            state["query_result"] = df
            self.logger.info(f"Query Results (DF): \n{df}")
            
            state["messages"] = [{"role": "assistant", "content": output.content}]
            self.logger.info(f"Messages: {state['messages']}")
            self.logger.info("run_query COMPLETED")
            
            return state
        
        except Exception as e:
            self.logger.error(f"Error running query: {e}")
            import traceback
            traceback.print_exc()
            state["query_result"] = None
            state["messages"] = [{"role": "assistant", "content": str(e)}]
            return state            


    #--------------------------------------------------------------------------------
    # Generate Plotly graph based on query result
    #--------------------------------------------------------------------------------
    def generate_plotly_graph(self, state: ChartAgentState):
        try:
            self.logger.info("Generating Plotly graph data...")
            user_input = state["user_input"]
            query_result = state.get("query_result")

            # Check if query_result is None
            if query_result is None:
                raise ValueError("Query result is empty. Cannot generate a graph.")

            query_result_str = query_result.to_string(na_rep="None")
            self.logger.info(f"Query Result String: {query_result_str}")

            template_string = ChartAgentPrompts.get_chart_json(query_result_str, user_input)

            prompt = PromptTemplate(
                template=template_string,
                input_variables=["user_input", "query_result"],
            )
            _input = prompt.format_prompt(user_input=user_input, query_result=query_result_str)
            response = self.llm.invoke(_input.to_string())
            output = response.content if response else None
            state["plotly_json"] = output
            self.logger.info("generate_plotly_graph COMPLETED!")
            
            return state
            
        except Exception as e:
            self.logger.error(f"Error generating Plotly graph: {e}")
            state["plotly_json"] = None

        return state        
    
    
    #--------------------------------------------------------------------------------
    # Invoke the agent to generate a graph
    #--------------------------------------------------------------------------------
    def invoke(self, state):
        try:
            if not self.graph:
                self.logger.error("Graph is not initialized. Ensure build_langgraph is called.")
                return None
                
            self.logger.info(f"ChartAgent invoked with state: {state}")
            
            # Extract the query from the last message in the state
            messages = state.get("messages", [])
            if not messages:
                self.logger.error("No messages found in state")
                return {"messages": [{"content": "No query provided."}]}
            
            user_input = messages[-1].content
                    
            if not user_input:
                self.logger.error("No user input found in messages")
                return {"messages": [{"content": "No user query found."}]}
                
            self.logger.info(f"Extracted user input: {user_input}")
            
            # Initialize a proper ChartAgentState
            prompt_user = ChartAgentState()
            prompt_user["user_input"] = user_input
           
            # Execute sub-graph with more verbose logging
            self.logger.info("Starting graph execution...")

            # Run the graph directly instead of streaming
            result = self.graph.invoke(prompt_user)
            self.logger.info(f"Graph execution completed: {result}")
            
            # Process the result
            if result and "plotly_json" in result and result["plotly_json"]:
                self.logger.info("Plotly data generated successfully")
                parsed_data = json.loads(result["plotly_json"])
                
                # Create a message with chart data
                message = HumanMessage(
                    content=f"I've created a visualization based on your query: '{user_input}'"
                )                
                return {
                    "messages": [message],
                    "next": "FINISH",  # Signal to move on to the next step
                    "chart_data": parsed_data["data"],
                    "chart_layout": parsed_data["layout"]
                }
            else:
                self.logger.warning("No visualization data generated")
                return {
                    "messages": [{"content": "I couldn't generate a chart for your query."}],
                    "next": "FINISH"  # Signal to move on to the next step
                }                
                           
   
        except Exception as e:
            self.logger.error(f"Error in ChartAgent: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return {
                "messages": [{"content": f"Failed to process chart request: {str(e)}"}],
                "next": "FINISH"  # Signal to move on even in case of error
            }