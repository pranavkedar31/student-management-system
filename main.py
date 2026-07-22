from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allowed domains
    allow_credentials=False,          # Allow cookies and auth headers
    allow_methods=["*"],             # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],             # Allow all request headers
)



connection=psycopg2.connect(os.getenv("DATABASE_URL"))


cursor= connection.cursor()

# class based validation
class Student(BaseModel):
    id:int= None
    name:str=None
    course:str=None

# get all students

@app.get("/students")
def get_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print(rows)
    
    result=[]
    for row in rows:
         result.append({
             "id":row [0],
             "name":row [1],
             "course":row [2],
         })
    return result

#Get single student

@app.get("/students/{id}")
def get_single_student(id: int):
   cursor.execute("SELECT * FROM students WHERE id=%s",(id,))
   row=cursor.fetchone()
   return{
            "id":row [0],
            "name":row [1],
            "course":row [2],
            }
   
# Create New Student Record

@app.post("/students")
def create_student_record(student: Student):
   cursor.execute("INSERT INTO students VALUES (%s, %s, %s)",(student.id,student.name,student.course))
   connection.commit()
   return {
       "message":"Student Record Created Successfully"
   }
   
# Replace Student Record

@app.put("/students/{id}")
def replace_student_record(id:int,student:Student):
    cursor.execute("UPDATE students SET id=%s,name=%s,course=%s WHERE id=%s",(student.id,student.name,student.course,id))
    connection.commit()
    return{
        "message":"Student Record Replaced Successfully"
    }

#Update Student Record
@app.patch("/students/{id}")
def  update_student_record(id:int,student:Student):
    if(student.id != None):
        cursor.execute("UPDATE students SET id=%s where id=%s",(student.id,id))
        connection.commit()
    if(student.name != None):
        cursor.execute("UPDATE students SET name=%s where id=%s",(student.name,id))
        connection.commit()
    if(student.course != None):
        cursor.execute("UPDATE students SET coures=%s where id=%s",(student.course,id))
        connection.commit()
    return{
        "message":"Student Record Updated Successfully"
    }
    
#Delete Student Record
@app.delete("/students/{id}")
def delete_student_record(id:int):
    cursor.execute("DELETE FROM students where id=%s",(id,))
    connection.commit()
    return{
        "message":"Student Data Deleted Successfully"
    }