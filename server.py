from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
import schemas
from models import Prototype, User
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("---Starting System Canus Software---")
    print("Veryfying integrity of the database")
    Base.metadata.create_all(bind=engine)
    print("--- System Online ---")

    yield

    print("--- System Offline ---")

app = FastAPI(title="Prototypes API", lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == form_data.username).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    is_password_correct = auth.verify_password(
        form_data.password, user_db.hashed_password)

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    new_token = auth.create_token(user_db.email)
    return {"access_token": new_token, "token_type": "bearer"}


@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == user_data.email).first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered in the Systme..."
        )

    hashed_pw = auth.hash_password(user_data.password)

    new_user = User(email=user_data.email, hashed_password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/rut-secret")
def leearn_data_clasificated(token: str = Depends(oauth2_scheme)):

    payload = auth.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="¡Alert! invalid token, access denied"
        )

    return {
        "message": "¡Access granted!",
        "inf_the_token": payload
    }


@app.post("/api/prototypes", status_code=201, response_model=schemas.PrototypeResponse)
def create_prototype(
        prototype_data: schemas.PrototypeCreate,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):

    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="¡Alert! invalid token, access denied"
        )

    new_model = Prototype(**prototype_data.model_dump())
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return new_model


@app.get("/api/prototypes", response_model=list[schemas.PrototypeResponse])
def get_all_prototypes(db: Session = Depends(get_db)):
    all_prototypes = db.query(Prototype).all()
    return all_prototypes


@app.put("/api/prototypes/{prototype_id}", response_model=schemas.PrototypeResponse)
def update_prototype(prototype_id: int, new_hp: int, db: Session = Depends(get_db)):
    existing_prototype = db.query(Prototype).filter(
        Prototype.id == prototype_id).first()
    if existing_prototype is None:
        raise HTTPException(
            status_code=404, detail="The Prototype does not exist")
    existing_prototype.horsepower = new_hp
    db.commit()
    db.refresh(existing_prototype)

    return existing_prototype


@app.delete("/api/prototypes/{prototype_id}",)
def delete_prototype(prototype_id: int, db: Session = Depends(get_db)):
    delete_to_prototype = db.query(Prototype).filter(
        Prototype.id == prototype_id).first()
    if delete_to_prototype is None:
        return {"Error": "The prototype no longer exists or has been discontinued"}
    db.delete(delete_to_prototype)
    db.commit()
    return {"Message": f"The prototype with ID {prototype_id} It was successfully eleminated."}
