from dotenv import load_dotenv
from app import create_app
from config import HOST, PORT


load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
