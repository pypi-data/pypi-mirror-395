from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, URL
from mambo.db.declarative_base import Base
from mambo.db.security.admin_seeds import AdminSeedSettings
class DbConnection:
    def __init__(self) -> None:
        load_dotenv()
        env_validator = self.env_validator()
        if not env_validator:
            self.gen_env_base()
            raise EnvironmentError("Missing required environment variables in .env file.")
        self.DB_NAME: str = os.getenv('DB_NAME', 'skoob')
        self.DB_USER: str = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'password')
        self.DB_HOST: str = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
        self.connect()

    def connect(self) -> None:
        self.engine = create_engine(URL.create(
            drivername='postgresql+psycopg2',
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME
        ))
        Base.metadata.create_all(self.engine)
        
    def env_validator(self) -> bool:
        if not os.path.exists('.env'):
            return False
        required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
        for var in required_vars:
            if os.getenv(var) is None:
                return False
        return True
    
    def gen_env_base(self) -> None:
        settings = AdminSeedSettings(
            DB_NAME='mambo',
            DB_USER='postgres',
            DB_PASSWORD='dbpassword',
            DB_HOST='localhost',
            DB_PORT=5432,
            JWT_SECRET_KEY='supersecretkey',
            GOOGLE_SECRET_KEY='xxxxxxxxxxxxxxxxxxxxxxxxx',
            GOOGLE_CLIENT_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
            GOOGLE_GEMINI_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            GOOGLE_REDIRECT_CALLBACK_URI='http://localhost:3030/users/auth/google/callback',
            GOOGLE_REDIRECT_FRONTEND_URI='http://localhost:3000',
            API_URL='http://127.0.0.1:3030',

            # ===== admins por defecto =====
            ADMIN1_NAME='FerBackend0!!2',
            ADMIN1_EMAIL='ferdhaban@gmail.com',
            ADMIN1_PASSWORD='Sup3r:-admin!',
        )
        
        for key, value in settings.model_dump().items():
            with open('.env', 'a') as f:
                f.write(f"{key}={value}\n")