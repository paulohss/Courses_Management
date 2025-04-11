from pydantic import BaseModel
from pydantic import Field
from langchain_core.prompts import ChatPromptTemplate

class EmailExtractedInfo(BaseModel):
    """
    Schema for the structured output from the LLM.
    """
    user_name: str = Field(..., description="The name of the user/person mentioned in the request.")
    email_type: str = Field(..., description="The type of email requested (either 'pending' or 'completed').")
    
    
    def get_extract_user_msg_type_prompt():
        prompt_template = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are an assistant that extracts structured information from user requests."
                    ),
                    (
                        "user",
                        "Analyze the following request and extract the following information:\n"
                        "1. The name of the user mentioned in the request.\n"
                        "2. The type of email requested (either 'pending' courses or 'completed' courses).\n\n"
                        "Request: {request}\n\n"
                        "Respond in the following JSON format:\n"
                        "{{\n"
                        "    \"user_name\": \"<Extracted User Name>\",\n"
                        "    \"email_type\": \"<pending|completed>\"\n"
                        "}}"
                    ),
                ]
            )
        
        return prompt_template    