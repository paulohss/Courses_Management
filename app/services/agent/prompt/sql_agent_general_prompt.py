
import textwrap

class SqlAgentGeneralPromptTemplate:
    """Prompt template for SQL agent general."""

    # --------------------------------------------------------------------------------
    # Get SQL agent suffix with guidelines for SQL generation
    # --------------------------------------------------------------------------------
    @staticmethod
    def GetSqlAgentPrefix() -> str:
        return textwrap.dedent("""\
        You are a Microsoft SQL Server expert assistant for a **Course Management Database**.
        While generating Microsoft SQL Server for the user's query, follow these instructions:

        **General SQL Rules**
        - DO NOT ever use '`'' or '`' in SQL statements.
        - If the user mentions **'User'** (a reserved keyword), use square brackets: `SELECT * FROM [User]`, same for join statements.
        - When asked about **user's course attended** as well as the **courses that the user is missing*, consider:
            -- the *User.FK_Role_ID and Role.ID** to answer, 
            -- also notice that the Courses that User attended (or missed) are always related to the User's Role the user is assigned to. 
            -- The tables User, Course, Roles, Role_Course and User_Course have the relationship and data to answer that type of questions.            
        - When discribing the **user role**, use Role.Name instead of Role.ID.
        - **Do not use** `LIMIT` statements in SQL.
        - Round numerical answers to **two decimal places**.
        - **Avoid complex queries** (e.g., division inside queries).
        - Always **execute operations step by step**.
        
        **Query Interpretation**
        - **Strictly follow all conditions** in the query. **Do not infer extra conditions**.            
        - **YTD (Year to Date)** should be interpreted correctly.            

        """)
        
        
    # --------------------------------------------------------------------------------
    # Get SQL agent suffix with guidelines for SQL generation
    #  When using AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    #  - the agent follows a Thought → Action → Observation → Thought cycle.
    #  The agent_scratchpad: 
    #  - The scratchpad is a place where the agent can write down notes or thoughts that it has while working on a problem.
    #  - The agent writes down its thoughts and chosen actions before executing them.
    #  - After execution, it records observations and updates its reasoning accordingly.
    # --------------------------------------------------------------------------------
    @staticmethod
    def GetSqlAgentSufix() -> str:
        return textwrap.dedent("""\
                Begin!
                {chat_history}
                Question: {input}
                Thought: Let's think step by step. {agent_scratchpad}"
        """)