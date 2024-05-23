# package: fastapi, bcrypt, sqlalchemy, python-jose

# test lokal uvicorn main:app --host 0.0.0.0 --port 8000 --reload --

# kalau deploy di server: pip install gunicorn
# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --daemon
# mematikan gunicorn (saat mau update):
# ps ax|grep gunicorn 
# pkill gunicorn

from os import path
from fastapi import Depends, Request, FastAPI, HTTPException

from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel

from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
models.BaseDB.metadata.create_all(bind=engine)

# from jose import jwt
import datetime

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI(title="Web service Medimate",
    description="Web service tubes kelompok 1 2024",
    version="0.0.1",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Dokumentasi API: [url]:8000/docs"}

######################### USERS

# create user 
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Error: Username sudah digunakan")
    return crud.create_user(db=db, user=user)

# hasil adalah akses token    
@app.post("/login") #,response_model=schemas.Token
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not authenticate(db,user):
        raise HTTPException(status_code=400, detail="Username atau password tidak cocok")

    # ambil informasi username
    user_login = crud.get_user_by_username(db,user.username)
    if user_login:
        access_token  = create_access_token(user.username)
        user_id = user_login.id
        return {"user_id":user_id,"access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="User tidak ditemukan, kontak admin")

#lihat detil user_id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token) 
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

######################## AUTH

# periksa apakah username ada dan passwordnya cocok
# return boolean TRUE jika username dan password cocok
def authenticate(db,user: schemas.UserCreate):
    user_cari = crud.get_user_by_username(db=db, username=user.username)
    if user_cari:
        return (user_cari.hashed_password == crud.hashPassword(user.password))
    else:
        return False    
    
SECRET_KEY = "ilkom_upi_top"

def create_access_token(username):
    # info yang penting adalah berapa lama waktu expire
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)    # .now(datetime.UTC)
    access_token = jwt.encode({"username":username,"exp":expiration_time},SECRET_KEY,algorithm="HS256")
    return access_token    

def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])  # bukan algorithm,  algorithms (set)
        username = payload["username"]  


    # exception jika token invalid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Unauthorize token, expired signature, harap login")
    except jwt.JWSError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWS Error")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWT Claim Error")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWT Error")   
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorize token, unknown error"+str(e))
    
    return {"user_name": username}

# internal untuk testing, jangan dipanggil langsung
# untuk swagger  .../doc supaya bisa auth dengan tombol gembok di kanan atas
# kalau penggunaan standard, gunakan /login

@app.post("/token", response_model=schemas.Token)
async def token(req: Request, form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    f = schemas.UserCreate
    f.username = form_data.username
    f.password = form_data.password
    if not authenticate(db,f):
        raise HTTPException(status_code=400, detail="username or password tidak cocok")

    #info = crud.get_user_by_username(form_data.username)
    # email = info["email"]   
    # role  = info["role"]   
    username  = form_data.username

    #buat access token\
    # def create_access_token(user_name,email,role,nama,status,kode_dosen,unit):
    access_token  = create_access_token(username)

    return {"access_token": access_token, "token_type": "bearer"}

####################################################################################################
# punya medimate

###################  profile

# create profile
@app.post("/create_profile/{user_id}")
def create_profile(user_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    if usr["user_id"] != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized access to create profile")

    return crud.create_profile(db=db, profile=profile)

# profile by user id
@app.get("/profile_user_id/{user_id}", response_model=list[schemas.Profile])
def read_profile_user_id(user_id : int, db: Session = Depends(get_db), token : str = Depends(oauth2_scheme)):
    usr = verify_token(token)
    return crud.get_profile_by_user_id(db, user_id)

# profile by profile id
@app.get("/profile/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id : int, db: Session = Depends(get_db), token : str = Depends(oauth2_scheme)):
    usr = verify_token(token)
    return crud.get_profile(db, profile_id)

# profile picture
path_img = '../img/profile_picture'
@app.get("/profile_picture/{profile_id}")
def read_profile_picture(profile_id:int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    profile = crud.get_profile(db,profile_id)
    if not(profile):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image = profile.profilePhoto
    if not(path.exists(path_img + nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    return FileResponse(path_img+nama_image)

# delete profile by profile id
@app.delete("/delete_profile/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    # Panggil fungsi untuk menghapus profil berdasarkan profile_id
    deleted_profile = crud.delete_profile(db, profile_id)
    if not deleted_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"message": "Profile deleted successfully"}

###################  doctor

# Get all doctor
@app.get("/doctor/", response_model=list[schemas.Doctor])
def read_all_doctor(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    doctor = crud.get_all_doctor(db)
    return doctor

# Get Doctor by ID
@app.get("/doctor/{doctor_id}", response_model = schemas.Doctor)
def read_doctor(doctor_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    doctor = crud.get_doctor_id(db, doctor_id)
    return doctor

# dooctor picture
path_img = '../img/doctor_picture'
@app.get("/doctor_picture/{doctor_id}")
def read_doctor_image(doctor_id:int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    doctor = crud.get_doctor_id(db,doctor_id)
    if not(doctor):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image = doctor.foto
    if not(path.exists(path_img + nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    return FileResponse(path_img+nama_image)

###################  appointments ############# BELUM WOY

# create appointment with profile id

# read appointment by profile id
@app.get("/appointment/{profile_id}", response_model=list[schemas.Appointment])
def read_appointment_profile_id(profile_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    appointment = crud.get_appointments_by_profile_id(db, profile_id)
    return appointment

# update appointment

# delete appointment by id
@app.delete("/delete_appointment/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    # Panggil fungsi untuk menghapus profil berdasarkan appointment_id
    deleted_appointment = crud.delete_appointment(db, appointment_id)
    if not deleted_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {"message": "Appointment deleted successfully"}

###################  articles

# get all health articles
@app.get("/health_article/", response_model=list[schemas.HealthArticle])
def read_all_health_article(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    article = crud.get_all_health_articles(db)
    return article

# Get Health Article by ID
@app.get("/health_article_id/{article_id}", response_model=schemas.HealthArticle)
def read_health_article(article_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    article = crud.get_health_article(db, article_id)
    return article

# article picture
path_img = '../img/article_picture'
@app.get("/article_picture/{article_id}")
def read_article_image(article_id:int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    article = crud.get_health_article(db,article_id)
    if not(article):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image = article.coverImage
    if not(path.exists(path_img + nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    return FileResponse(path_img+nama_image)

###################  Health Facility

# semua facility
@app.get("/health_facility/", response_model=list[schemas.HealthFacility])
def read_all_health_facility(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    healthFacility = crud.get_all_health_facilities(db)
    return healthFacility

# Get Health Facility by ID
@app.get("/health_facility_id/{facility_id}", response_model = schemas.HealthFacility)
def read_health_facility(facility_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    facility = crud.get_health_facility_by_id(db, facility_id)
    return facility

# health facility picture
path_img = '../img/health_facility_picture'
@app.get("/health_facility_picture/{health_facility_id}")
def read_health_facility_image(health_facility_id:int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    health_facility = crud.get_health_facility_by_id(db,health_facility_id)
    if not(health_facility):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image = health_facility.fotoFaskes
    if not(path.exists(path_img + nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    return FileResponse(path_img+nama_image)

###################  refferals ############# BELUM WOY

# create refferals

# read refferals by id
@app.get("/refferal/{refferal_id}", response_model=list[schemas.ReferralRead])
def read_refferal_by_id(refferal_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    refferal = crud.get_refferal(db, refferal_id)
    return refferal

###################  review ############# BELUM WOY

# create review


# read review by doctor id
@app.get("/review_doctor/{doctor_id}", response_model=list[schemas.Review])
def read_review_doctor(doctor_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    review_doc = crud.get_reviews_by_doctor_id(db, doctor_id)
    return review_doc

# read review by facility id
@app.get("/review_facility/{facility_id}", response_model=list[schemas.Review])
def read_review_facility(facility_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    usr = verify_token(token)

    review_fac = crud.get_reviews_by_facility_id(db, facility_id)
    return review_fac

###################  service #############

# semua service
@app.get("/services/", response_model=list[schemas.Service])
def read_services(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)): # db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)
    usr =  verify_token(token)
    service = crud.get_all_services(db)
    return service

# image service by id
path_img = "../img/service_icon/"
@app.get("/service_images/{service_id}")
def read_services_image(service_id:int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    service = crud.get_service_by_id(db,service_id)
    if not(service):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image = service.icon
    if not(path.exists(path_img + nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    return FileResponse(path_img+nama_image)

###################  specialist and polyclinic

# semua specialist and polyclinic
@app.get("/specialist_and_polyclinic/", response_model=list[schemas.SpecialistAndPolyclinic])
def read_specialist_and_polyclinic(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)): # db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)
    usr =  verify_token(token)
    specialist_and_polyclinic = crud.get_all_specialist_and_polyclinics(db)
    return specialist_and_polyclinic

# image specialist and polyclinic berdasarkan id
path_img = "../img/specialist_and_polyclinic/"
@app.get("/specialist_and_polyclinic_images/{specialist_and_polyclinic_id}")
def read_spe_image(specialist_and_polyclinic_id:int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    specialist_and_polyclinic = crud.get_polyclinic_by_id(db,specialist_and_polyclinic_id)
    if not(specialist_and_polyclinic):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image =  specialist_and_polyclinic.icon
    if not(path.exists(path_img + nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    fr =  FileResponse(path_img+nama_image)
    return fr

####################################################################################################