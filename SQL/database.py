# Importing necessary libraries
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()    # Calling the function

# db_url = dialect+driver://dbuser;dbpassword;dbhost;dbport;dbname
db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'

engine = create_engine(db_url)

session = sessionmaker(bind=engine)

db = session()

# To retrieve data from database
# query = text("select * from user")

# users = db.execute(query).fetchall()

# print(users)

# Commands to create tables from VScode directly
create_users = text("""
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
    );
""")

create_courses = text("""
CREATE TABLE IF NOT EXISTS courses(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    level VARCHAR(100) NOT NULL
    );
""")

create_enrollment = text("""
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    courseId INT,
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (courseId) REFERENCES courses(id)
    );
""")

# To execute the above, we use the below command
db.execute(create_users)
db.execute(create_courses)
db.execute(create_enrollment)
print("Tables has been created successfully")