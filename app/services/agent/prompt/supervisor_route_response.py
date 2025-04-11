from pydantic import BaseModel
from typing import List, Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class RouteResponse(BaseModel):
    """
    Response model for supervisor routing decisions.
    
    This class defines a structured output format using Pydantic:
    
    1. Creates a schema that enforces what values the supervisor can return
       when deciding the next step in the workflow.
    
    2. By inheriting from Pydantic's BaseModel, it gains automatic data
       validation, serialization, and documentation capabilities.
    
    3. The 'next' field uses Python's Literal type to restrict valid values to only
       three specific options: "FINISH", "Researcher", or "SqlAgent". Any other value
       would cause a validation error.
    
    4. Used with .with_structured_output(RouteResponse) to instruct the LLM to
       format its response according to this schema, ensuring the supervisor agent
       always returns one of the three valid routing options.
    
    5. Controls workflow routing:
       - "EmailAgent" → Send to email agent
       - "Researcher" → Send to researcher agent
       - "SqlAgent" → Send to SQL agent
       - "FINISH" → End the workflow
    """
    next: Literal["FINISH", "EmailAgent", "Researcher", "SqlAgent"]
    
    
    #--------------------------------------------------------------------------------
    # Get route prompt for the supervisor agent
    #--------------------------------------------------------------------------------
    def get_route_prompt(options, members):
        
        system_prompt = (
            "You are a supervisor tasked with managing a conversation between the" 
            " following workers (agents): {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a task and respond with their results and status."
            "Worker (agents) specialties:"
            "\n**1. EmailAgent ** When the user asks to **send an email** to a user (Example: Send an email to **user** with his completed courses)."
            "\n**2. Researcher ** For general information gathering, online research, web research, and non-database questions"
            "  2.1 Exemple: When the user asks about general information, research topics, or any data that would require web search."
            "\n**3. SqlAgent ** For database queries, SQL operations, and data retrieval from the Course Management system"
            "\ 3.1 Exemple: When the user asks about database information, users, courses, roles, or any data that would require SQL queries."
            "\n4. When finished, respond with FINISH."
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?" 
                    " Or should we FINISH? Select one of: {options}"
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))    
        
        return prompt