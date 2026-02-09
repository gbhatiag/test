import os
from dotenv import load_dotenv
import mysql.connector
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from pydantic import BaseModel

# Determine environment and load the correct .env file
ENV_TYPE = os.getenv('ENV_TYPE', 'development')
env_file = os.path.join(os.path.dirname(__file__), '..', 'ENV', f"{'prod.env' if ENV_TYPE == 'production' else 'dev.env'}")
load_dotenv(dotenv_path=env_file)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_verify_token(token: str = Depends(oauth2_scheme)):
    if token != "sampletoken":  # Demo token: replace with real validation in production
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token

class Customer(BaseModel):
    name: str
    service_date: str

@app.post("/customers", response_model=List[Customer])
def get_service_customers(service_name: str, token: str = Depends(fake_verify_token)):
    db_config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'user'),
        'password': os.getenv('MYSQL_PASSWORD', 'password'),
        'database': os.getenv('MYSQL_DATABASE', 'servicedb')
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = """SELECT c.name, s.service_date \
               FROM customers c \
               JOIN services_taken s ON c.id = s.customer_id \
               WHERE s.service_name = %s"""
    cursor.execute(query, (service_name,))
    result = [Customer(name=row[0], service_date=str(row[1])) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return result
