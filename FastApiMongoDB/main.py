import re
from fastapi import FastAPI, Path, Query,Depends, HTTPException
from mongoengine import connect
from mongoengine.queryset.visitor import Q
import json
from datetime import timedelta,datetime
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from models import Employee,User, NewEmployee, NewUser




app = FastAPI()
connect(db="FARM", host="localhost", port=27017)

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/get_all_employees")
def get_all_employees():
    employees = json.loads(Employee.objects().to_json())
    # print(employees)
    # employees_list = json.loads(employees)
    return {"employees":employees}



@app.get("/get_employee/{emp_id}")
def get_employee(emp_id: int = Path(..., gt=0)):
    # employee = json.loads(Employee.objects(emp_id=emp_id).to_json())
    employee = Employee.objects.get(emp_id=emp_id)
    employee_dict = {
        "emp_id": employee.emp_id,
        "name": employee.name,
        "age": employee.age,
        "teams": employee.teams,
        # "salary": employee.salary,
    }
    
    return employee_dict


@app.get("/search_employees")
def search_employees(name: str = Query(None), age: int = Query(None,gt=18)):
    employees = json.loads(Employee.objects.filter(Q(name__icontains=name)| Q(age=age)).to_json())
    
    return {"employees":employees}
    



@app.post("/add_employee")
def add_employee(employee: NewEmployee):
    new_employee = Employee(emp_id=employee.emp_id,
                            name=employee.name, 
                            age=employee.age, 
                            teams=employee.teams)
    new_employee.save()
    return {"message": "Employee added successfully"}



@app.post("/sign_up")
def sign_up(newuser: NewUser):
    new_user = User(username=newuser.username,
                    password=get_password_hash(newuser.password))
    new_user.save()
    return {"message": "User added successfully"}


def get_password_hash(password):
    return pwd_context.hash(password)




#Add authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def authenticate_user(username: str, password: str):
    try:
        user = json.loads( User.objects.get(username=username).to_json())
        password_check =pwd_context.verify(password, user["password"])
        return password_check
    except User.DoesNotExist:
        raise False


SECRET_KEY= "7d7204cbdbadb1194eb06eaf052dfae758a38c5f056e581bbdb05d69396c012d"
ALGORITHM= "HS256"
def create_access_token(data:dict ,expires_delta:timedelta=None):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({
        "exp": expire
    })
    # print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username= form_data.username
    password= form_data.password

    print(username,password)

    if authenticate_user(username, password):
        access_token = create_access_token(
            data={"sub":username}, expires_delta=timedelta(minutes=30)
        )
        return {"access_token":username, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")



@app.get("/")
def home(token: str = Depends(oauth2_scheme)):
    return {"token": token}