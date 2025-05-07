import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig
from app.services.bll.user_service import UserService
from app.utils.logger_service import LoggerService
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from app.services.agent.prompt.email_content_prompt import EmailContent
from app.services.agent.prompt.email_extracted_info_prompt import EmailExtractedInfo

#--------------------------------------------------------------------------------
# EmailAgent class
#--------------------------------------------------------------------------------
class EmailAgent:

    #--------------------------------------------------------------------------------
    # Initialize the EmailAgent
    #--------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None):

        self.logger = LoggerService.get_instance().get_logger(__name__)

        # Use config if not provided
        provider = provider or LLMConfig.PROVIDER
        model_name = model_name or LLMConfig.MODEL_NAME

        # Get LLM from factory
        self.llm = LLMFactory.get_instance().get_llm(provider, model_name)

        # Email configuration
        self.smtp_server = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", 587))
        self.email_sender = os.environ.get("EMAIL_SENDER", "")
        self.email_password = os.environ.get("EMAIL_PASSWORD", "")

        if not self.email_sender or not self.email_password:
            self.logger.warning("Email sender or password not configured in environment variables")



    # --------------------------------------------------------------------------------
    # Send email using SMTP
    # --------------------------------------------------------------------------------
    def _send_email(self, recipient_email, subject, body):
        try:
            message = MIMEMultipart()
            message["From"] = self.email_sender
            message["To"] = recipient_email
            message["Subject"] = subject

            # Attach the body
            message.attach(MIMEText(body, "plain"))

            # Create secure connection and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.sendmail(self.email_sender, recipient_email, message.as_string())

            return True, "Email sent successfully"

        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            return False, f"Error sending email: {str(e)}"


    # --------------------------------------------------------------------------------
    # Compose email body using LLM
    # --------------------------------------------------------------------------------
    def _compose_email_body(self, user_name, list_type, course_list):
        try:
            # Format the course list
            courses_text = "\n".join([f"- {course}" for course in course_list]) if course_list else "No courses found."

            # Step 1: Define the prompt template
            prompt_template = EmailContent.compose_email_prompt()

            # Step 2: Combine the prompt template with the structured LLM
            structured_llm = self.llm.with_structured_output(EmailContent)
            email_chain = prompt_template | structured_llm

            # Step 3: Process the input through the chain
            email_content = email_chain.invoke(
                {
                    "user_name": user_name,
                    "list_type": list_type,
                    "courses_text": courses_text,
                }
            )

            # Step 4: Extract the email body
            return email_content.email_body

        except Exception as e:
            self.logger.error(f"Error composing email body: {str(e)}")
            return f"Error composing email body: {str(e)}"


    # --------------------------------------------------------------------------------
    # Extract user email and type from the request
    # --------------------------------------------------------------------------------
    def _extract_user_email_and_type(self, request):
        try:
            # Step 1: Define the prompt template
            prompt_template = EmailExtractedInfo.get_extract_user_msg_type_prompt()

            # Step 2: Combine the prompt template with the structured LLM
            structured_llm = self.llm.with_structured_output(EmailExtractedInfo)
            extraction_chain = prompt_template | structured_llm

            # Step 3: Process the request through the chain
            extracted_info = extraction_chain.invoke({"request": request})

            # Step 4: Extract the structured data
            user_name = extracted_info.user_name
            email_type = extracted_info.email_type

            if not user_name or not email_type:
                raise ValueError("Failed to extract user name or email type from the request.")

            # Step 5: Use UserService to retrieve the user's email
            user_service = UserService()  # Instantiate UserService
            user = user_service.get_user_by_name(user_name)
            if not user or not user.get("email"):
                raise ValueError("Failed to extract user email from the request.")

            if not user or not user.get("user_course_list"):
                raise ValueError("Failed to extract user course list.")

            user_email = user["email"]
            course_list = user["user_course_list"]
            return user_name, user_email.strip(), email_type, course_list

        except Exception as e:
            self.logger.error(f"Error extracting user email and type: {str(e)}")
            return None, None, None, None


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

            # Step 1: Extract user name, email, and email type
            user_name, user_email, email_type, course_list = self._extract_user_email_and_type(request)

            if not user_name or not user_email or not email_type or not course_list:
                return {"messages": [HumanMessage(content="Could not find the user or their email.")]}

            # Step 3: Compose the email body
            email_body = self._compose_email_body(user_name, email_type, course_list)

            # Step 4: Send the email
            subject = f"Your {email_type.capitalize()} Courses"
            success, message = self._send_email(user_email, subject, email_body)

            if success:
                return {"messages": [HumanMessage(content=f"Email sent successfully to {user_name} ({user_email}).")], "next": "FINISH"}
            else:
                return {"messages": [HumanMessage(content=f"Failed to send email: {message}")], "next": "FINISH"}

        except Exception as e:
            self.logger.error(f"Error processing email request: {str(e)}")
            return {"messages": [HumanMessage(content=f"Error processing email request: {str(e)}")], "next": "FINISH"}