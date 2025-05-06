import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from app.utils.logger_service import LoggerService
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig
from app.services.agent.prompt.rag_pdf_content_prompt import RagPdfContent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from langchain_core.messages import HumanMessage
from llama_index.llms.langchain import LangChainLLM  # Import the wrapper
import traceback  # Import traceback for better error logging

#--------------------------------------------------------------------------------
# RAG PDF class
#--------------------------------------------------------------------------------
class RagPdfAgent:

    #--------------------------------------------------------------------------------
    # Initialize the RAG PDF Agent
    #--------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None):
        try:
            self.logger = LoggerService.get_instance().get_logger(__name__)

            # Define the relative path to the data_courses folder
            data_courses_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data_courses')
            self.combined_engine = self._load_pdfs_from_directory(data_courses_path)
            if self.combined_engine is None:
                raise ValueError("Failed to initialize combined query engine from PDFs.")

            # Use config if not provided
            provider = provider or LLMConfig.PROVIDER
            model_name = model_name or LLMConfig.MODEL_NAME

            # Get LangChain LLM from factory
            langchain_llm = LLMFactory.get_instance().get_llm(provider, model_name)

            # Check if LangChain LLM was successfully initialized
            if langchain_llm is None:
                error_msg = f"Failed to get LangChain LLM instance from factory for provider: {provider}, model: {model_name}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            self.logger.info(f"LangChain LLM instance obtained successfully: {type(langchain_llm)}")

            # Wrap the LangChain LLM for LlamaIndex compatibility
            # This creates a LlamaIndex LLM object from the LangChain one
            self.llm = LangChainLLM(llm=langchain_llm)
            self.logger.info(f"Wrapped LLM for LlamaIndex: {type(self.llm)}")

            # Define the tools for the agent
            self.tools = [
                QueryEngineTool(
                    query_engine=self.combined_engine,
                    metadata=ToolMetadata(
                        name=RagPdfContent.get_name(),
                        description=RagPdfContent.get_context(),
                    ),
                ),
            ]

            # Initialize the ReActAgent using the wrapped LlamaIndex LLM
            self.agent = ReActAgent.from_tools(self.tools, llm=self.llm, verbose=True, context=RagPdfContent.get_context())
            self.logger.info("ReActAgent initialized successfully for RagPdfAgent.")

        except Exception as e:
            # Log the full traceback for better debugging
            self.logger.error(f"Error initializing RagPdfAgent: {str(e)}\n{traceback.format_exc()}")
            raise


    #--------------------------------------------------------------------------------
    # Define the _build_index method to create or load an index for the documents
    #--------------------------------------------------------------------------------
    def _build_index(self, data, index_name):
        try:
            index = None
            print("Building index for PPDF RAG", index_name)
            index = VectorStoreIndex.from_documents(data, show_progress=True)
            index.storage_context.persist(persist_dir=index_name)
            return index
        
        except Exception as e:
            self.logger.error(f"Error building index for PPDF RAG: {str(e)}")
            return None


    #--------------------------------------------------------------------------------
    # Get the index for the documents
    #--------------------------------------------------------------------------------
    def _get_index(self, index_name):
        try:
            index = None
            print("loading index", index_name)
            index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=index_name)
            )
            return index
        
        except Exception as e:
            self.logger.error(f"Error loading index: {str(e)}")
            return None


    #--------------------------------------------------------------------------------
    # Define the _load_pdfs_from_directory method to load all PDFs from a directory
    #--------------------------------------------------------------------------------
    def _load_pdfs_from_directory(self, directory_path):
        try:
            if not os.path.exists("combined_pdfs"):                       
                pdf_reader = PDFReader()
                all_documents = []
                
                # Make sure the directory exists
                if not os.path.exists(directory_path):
                    print(f"Directory not found: {directory_path}")
                    return None

                # Iterate through all files in the directory
                for filename in os.listdir(directory_path):
                    if filename.lower().endswith('.pdf'):
                        file_path = os.path.join(directory_path, filename)
                        print(f"Processing {filename}...")
                        try:
                            pdf_data = pdf_reader.load_data(file=file_path)
                            all_documents.extend(pdf_data)
                        except Exception as e:
                            print(f"Error processing {filename}: {e}")
                
                # Create a single index from all documents
                if all_documents:
                    combined_index = self._build_index(all_documents, "combined_pdfs")
                    
            else:
                combined_index = self._get_index("combined_pdfs")
                                
            combined_engine = combined_index.as_query_engine()
            return combined_engine
        
        except Exception as e:
            self.logger.error(f"Error loading PDFs from directory: {str(e)}")
            return None        
        

    # --------------------------------------------------------------------------------
    # Invoke method to process the request and send the email
    # --------------------------------------------------------------------------------
    def invoke(self, state):
        try:
            # Extract the request from the last message in the state
            messages = state.get("messages", [])
            if not messages:
                return {"messages": [HumanMessage(content="No request provided.")]}

            request = messages[-1].content
            
            response = self.agent.query(request)
            return {"messages": [HumanMessage(content=str(response))]}
            
        except Exception as e:
            self.logger.error(f"Error extracting request: {str(e)}")
            return {"messages": [HumanMessage(content="Error extracting request.")]}
