import os
from app import create_app
from app.utils.logger_service import LoggerService

# Print the log directory path
logger = LoggerService.get_instance().get_logger(__name__)
logger_service = LoggerService.get_instance()
print(f"Log files are saved in: {os.path.abspath(logger_service.log_dir)}")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)