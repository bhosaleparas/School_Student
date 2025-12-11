from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import database

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="School API", version="1.0.0")



# function to get database session
def get_db_session():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/schools/", response_model=dict)
def create_school(name: str, address: str, email: str, db: Session = Depends(get_db_session)):
    # Check if email already exists
    existing_school = db.query(models.School).filter(models.School.email == email).first()
    if existing_school:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new school
    new_school = models.School(name=name, address=address, email=email)
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    
    return {
        "id": new_school.id,
        "name": new_school.name,
        "address": new_school.address,
        "email": new_school.email,
        "message": "School created successfully"
    }




@app.get("/schools/", response_model=List[dict])
def get_all_schools(db: Session = Depends(get_db_session)):
    schools = db.query(models.School).all()
    
    result = []
    for school in schools:
        result.append({
            "id": school.id,
            "name": school.name,
            "address": school.address,
            "email": school.email,
            "student_count": len(school.students)
        })
    
    return result



@app.get("/schools/{school_id}", response_model=dict)
def get_school(school_id: int, db: Session = Depends(get_db_session)):
    school = db.query(models.School).filter(models.School.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    return {
        "id": school.id,
        "name": school.name,
        "address": school.address,
        "email": school.email
    }



# Students

@app.post("/students/", response_model=dict)
def create_student(name: str, age: int, email: str, school_id: int, db: Session = Depends(get_db_session)):
    # Check if email already exists
    existing_student = db.query(models.Student).filter(models.Student.email == email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if school exists
    school = db.query(models.School).filter(models.School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Create new student
    new_student = models.Student(name=name, age=age, email=email, school_id=school_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return {
        "id": new_student.id,
        "name": new_student.name,
        "age": new_student.age,
        "email": new_student.email,
        "school_id": new_student.school_id,
        "message": "Student created successfully"
    }



@app.get("/students/", response_model=List[dict])
def get_all_students(db: Session = Depends(get_db_session)):
    students = db.query(models.Student).all()
    
    result = []
    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "email": student.email,
            "school_id": student.school_id,
            "school_name": student.school.name if student.school else None
        })
    
    return result





@app.get("/students/{student_id}", response_model=dict)
def get_student_with_school(student_id: int, db: Session = Depends(get_db_session)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "email": student.email,
        "school": {
            "id": student.school.id,
            "name": student.school.name,
            "address": student.school.address,
            "email": student.school.email
        } if student.school else None
    }
    
    
    
    

@app.get("/schools/{school_id}/students", response_model=List[dict])
def get_students_by_school(school_id: int, db: Session = Depends(get_db_session)):
    # Check if school exists
    school = db.query(models.School).filter(models.School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    students = db.query(models.Student).filter(models.Student.school_id == school_id).all()
    
    result = []
    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "email": student.email
        })
    
    return result



@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "School Management API",
        "endpoints": {
            "schools": {
                "create_school": "POST /schools/",
                "get_all_schools": "GET /schools/",
                "get_school": "GET /schools/{id}",
                "get_school_students": "GET /schools/{id}/students"
            },
            "students": {
                "create_student": "POST /students/",
                "get_all_students": "GET /students/",
                "get_student_with_school": "GET /students/{id}"
            }
        }
    }