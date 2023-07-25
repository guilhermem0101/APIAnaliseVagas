from flask_frozen import Freezer
from app import create_app  # Import your app creation function

app = create_app()  # Create an instance of your Flask application
freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()  # Generate the static files
