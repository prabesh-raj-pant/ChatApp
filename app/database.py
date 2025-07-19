 

from sqlmodel import  create_engine

from dotenv import load_dotenv
import os

load_dotenv()
 
db_url =os.getenv('DATABASE_URL',123)
 
engine = create_engine(db_url )


