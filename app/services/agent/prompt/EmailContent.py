from pydantic import BaseModel
from pydantic import Field
from langchain_core.prompts import ChatPromptTemplate

class EmailContent(BaseModel):
    """
    Schema for the structured output from the LLM for email content.
    """
    email_body: str = Field(..., description="The body of the email to be sent to the user.")
    
    
    def compose_email_prompt():
        prompt_template = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are an assistant that generates professional and friendly email content."
                    ),
                    (
                        "user",
                        "Write a professional and friendly email to {user_name}.\n"
                        "The email should include the following:\n"
                        "- A greeting\n"
                        "- A message about their {list_type} courses\n"
                        "- The list of courses (use bullet points):\n"
                        "{courses_text}\n"
                        "- A closing statement encouraging them to take action if needed."
                        "Sign off the email with no names, just this message: [This is an automated message, please do not reply.].\n\n"
                    ),
                ]
            )
        
        return prompt_template    