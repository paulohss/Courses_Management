
# This class is used to query the offline courses data in PDF format provided by CORPORATE SCHOOL.
class RagPdfContent:

    @staticmethod
    def get_context() -> str:
        return "Purpose: This tool is used to query the offline courses data in PDF format provided by CORPORATE SCHOOL (CORPORATE SCHOOL files is also known as: 'corporate school', 'inner documents', 'our documments', 'our files') "

    @staticmethod
    def get_name() -> str:
        return "pdf_query_tool"