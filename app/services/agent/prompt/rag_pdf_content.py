
# This class is used to query the offline courses data in PDF format provided by CORPORATE SCHOOL.
class RagPdfContent:

    @staticmethod
    def get_context() -> str:
        return "offline_courses_data"

    @staticmethod
    def get_name() -> str:
        return "Purpose: This tool is used to query the offline courses data in PDF format provided by CORPORATE SCHOOL (aka: 'corporate school', 'inner documents', 'our documments', 'our files') "