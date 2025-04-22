from pydantic import BaseModel
from typing import List, Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class RouteResponse(BaseModel):
    
    # Properties of the RouteResponse class
    next: Literal["FINISH", "EmailAgent", "Researcher", "SqlAgent", "RagPdfAgent"]
    
    
    #--------------------------------------------------------------------------------
    # Get route prompt for the supervisor agent
    #--------------------------------------------------------------------------------
    def get_route_prompt(options, members):
        
        system_prompt = (
            "You are a supervisor tasked with managing a conversation between the" 
            " following workers (agents): {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a task and respond with their results and status."
            "\n\nIMPORTANT: Follow these priority rules when deciding which worker to use:"
            
            "\n\n1. EmailAgent - HIGHEST PRIORITY for these patterns:"
            "\n   - ANY request containing phrases like 'send an email', 'email to', 'send to user'"
            "\n   - ANY request asking to notify or message a user"
            "\n   Examples:"
            "\n   - 'Send an email to user John with his completed courses'"
            "\n   - 'Email Sarah about her pending training'"
            "\n   - 'Send to user Mark the list of courses'"
            "\n   - 'Please email the completed courses to Jane'"
            "\n   NOTE: The EmailAgent will handle ALL the necessary steps including retrieving the user's email and course data."
            
            "\n\n2. RagPdfAgent - For queries about offline course content:"
            "\n   - Use when request mentions CORPORATE SCHOOL, inner/our documents, or files"
            "\n   - Use for any questions about course materials or content"
            
            "\n\n3. SqlAgent - For database queries and reports:"
            "\n   - Use for data retrieval about users, courses, roles or enrollment"
            "\n   - DO NOT use for email requests even if they mention user ata"
            "\n   - Examples: 'Show me all users', 'List courses for role manager', 'List the courses that the user completLeids/finished', 'list the courses that the user is missing/didn't finish'"
            
            "\n\n4. Researcher - For general information:"
            "\n   - Use for general questions not requiring database or document access"
            "\n   - Web research, general knowledge questions"
            
            "\n\n5. When the conversation is complete, respond with FINISH."
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next? Pay special attention to email-related requests - these MUST go to EmailAgent."
                    " Select one of: {options}"
                ),
            ]
        ).partial(options=str(options), members=", ".join(members))    
        
        return prompt