# from database import db
# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel, Field
# from sqlalchemy import text
# import os
# from dotenv import load_dotenv
# import bcrypt
# import uvicorn
# from middleware import create_token, verify_token

# load_dotenv()

# # Defining the app
# app = FastAPI(title="Simple API App", version="1.0.0")

# # Adding token validity period
# token_time = int(os.getenv("token_time"))


# class Users(BaseModel):
#     name: str = Field(..., example="Jay jay")
#     email: str = Field(..., example="jay@publica.io")
#     password: str = Field(..., example="@gfjeoi")
#     userType: str = Field(..., example="student")


# @app.post("/signup")
# def signUp(input: Users):
#     try:
#         duplicate_query = text("""
#               SELECT * FROM users
#               WHERE email = :email
#                               """)
#         existing = db.execute(duplicate_query, {"email": input.email})
#         if existing:
#             print("Email already exist")
#             # raise HTTPException(status_code=400, detail="Email already exists")

#         query = text("""
#             INSERT INTO users (name, email, password)
#             VALUES (:name, :email, :password)
#         """)

#         # Add password encryption
#         salt = bcrypt.gensalt()
#         hashedPassword = bcrypt.hashpw(input.password.encode("utf-8"), salt)
#         print(hashedPassword)

#         db.execute(query, {"name": input.name,
#                    "email": input.email, "password": hashedPassword, "userType": input.userType})
#         db.commit()

#         return {"message": "user created successfully",
#                 "data": {"name": input.name, "email": input.email, "userType": input.userType}}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=e)


# class LoginRequest(BaseModel):
#     email: str = Field(..., example="jdoe@gmail.com")
#     password: str = Field(..., example="sam11")


# @app.post("/login")
# def login(input: LoginRequest):
#     try:
#         query = text("""
#         SELECT * FROM users WHERE email = :email
# """)
#         result = db.execute(query, {"email": input.email}).fetchone()

#         if not result:
#             raise HTTPException(
#                 status_code=400, detail="invalid email or password")

#         verified_password = bcrypt.checkpw(input.password.encode(
#             'utf-8'), result.password.encode('utf-8'))

#         if not verified_password:
#             raise HTTPException(
#                 status_code=404, detail="invalid email or password")

#         encoded_token = create_token(details={
#             "email": result.email,
#             "userType": result.userType
#         }, expiry=token_time)

#         return {
#             "message": "Login Successful",
#             "token": encoded_token

#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# class Courses(BaseModel):
#     title: str = Field(..., example="Electrical Machine")
#     level: str = Field(..., example="200 level")


# @app.post("/courses")
# def addcourses(input: Courses, user_data=Depends(verify_token)):
#     try:
#         print(user_data)

#         if user_data['userType'] != 'admin':
#             raise HTTPException(
#                 status_code=401, detail="You are not authorized to add a course")
#         query = text("""
#             INSERT INTO courses(title, level)
#             VALUES(:title, :level)
#         """)

#         db.execute(query, {"title": input.title, "level": input.level})
#         db.commit()
#         return {"message": "Course added successfully",
#                 "data": {"title": input.title, "level": input.level}}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# if __name__ == "__main__":
#     uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))


from middleware import create_token, verify_token
from database import db
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn
import jwt
load_dotenv()
app = FastAPI(title="Simple App", version="1.0.0")
token_time = int(os.getenv("token_time"))


class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    userType: str = Field(..., example="student")


@app.post("/signup")
def signUp(input: Simple):
    try:
        duplicate_query = text("""
            SELECT * FROM users
            WHERE email = :email
                             """)
        existing = db.execute(
            duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        query = text("""
            INSERT INTO users (name, email, password,userType)
            VALUES (:name, :email, :password, :userType)
        """)
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(
            input.password.encode('utf-8'), salt).decode()
        print(hashedPassword)
        db.execute(query, {"name": input.name, "email": input.email,
                   "password": hashedPassword, "userType": input.userType})
        db.commit()
        return {"message": "User created successfully",
                "data": {"name": input.name, "email": input.email, "usertype": input.userType}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
# Building a login endpoint


class LoginRequest(BaseModel):
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")


@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
            SELECT * FROM users WHERE email = :email
            """)
        result = db.execute(query, {"email": input.email}).fetchone()

        if not result:
            raise HTTPException(
                status_code=404, detail="Invalid email or password")
        input_password = str(result["password"])
        verified_password = bcrypt.checkpw(input.password.encode(
            'utf-8'), input_password.encode('utf-8'))
        if not verified_password:
            raise HTTPException(
                status_code=404, detail="Invalid email or password")
        encoded_token = create_token(details={
            "email": result.email,
            "userType": result.userType
        }, expiry=token_time)
        return {
            "message": "Login Successful",
            "token": encoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class courseRequest(BaseModel):
    title: str = Field(..., example="Backend Course")
    level: str = Field(..., example="Beginner")


@app.post("/courses")
def addcourses(input: courseRequest, user_data=Depends(verify_token)):
    try:
        print(user_data)
        if user_data['userType'] != 'admin':
            raise HTTPException(
                status_code=401, detail="You are not authorized to add a course")
        query = text("""
            INSERT INTO courses(title, level)
            VALUES (:title,:level)
""")
        db.execute(query, {"title": input.title, "level": input.level})
        db.commit()
        return {"message": "Courses added successfully",
                "data": {"title": input.title, "level": input.level}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
