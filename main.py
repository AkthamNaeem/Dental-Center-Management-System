from database.schema import create_schema
from ui.main import DentalCenterApp

def initialize_app():
    # Create database schema if it doesn't exist
    create_schema()
    
    # Run the application
    app = DentalCenterApp()
    app.mainloop()

if __name__ == "__main__":
    initialize_app()
