from fastapi import FastAPI, Form, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from src.database import User, get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

app = FastAPI()
templates = Jinja2Templates(directory="template")
app.mount("/static", StaticFiles(directory="template"), name="static")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/signup", response_class=HTMLResponse)
def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
def create_user(request: Request, email: str = Form(...),
                password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=email, hash_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return templates.TemplateResponse("signup.html", {"request": request,
                                                      "user": new_user})

# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")
