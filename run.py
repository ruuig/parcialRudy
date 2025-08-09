import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 3000)), debug=True)
