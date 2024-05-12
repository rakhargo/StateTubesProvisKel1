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

from jose import jwt
import datetime

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI(title="Web service BarayaFood",
    description="Web service untuk quiz provis Mei 2024",
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

#hapus ini kalau salt sudah digenerate
# @app.get("/getsalt")
# async def getsalt():
#     hasil = bcrypt.gensalt()
#     return {"message": hasil}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Dokumentasi API: [url]:8000/docs"}

# nanti disembunyikan, untuk iniisasi tambah user dan items, biar nggak manual setiap db diganti
# hati2 ini menghapus data di tabel item dan user
# @app.put("/init")
# async def init(db: Session = Depends(get_db)):
#     crud.delete_all_item(db)
#     crud.delete_all_user(db)
#     u = schemas.UserCreate
#     u.username = "default"
#     u.password = "ilkomupi"
#     crud.create_user(db,u)
    
#     i = schemas.ItemCreate
#     i.title = "Mie Bakso"
#     i.description = "Mie Bakso gurih dengan bakso yang besar"
#     i.img_name = "bakso.png"
#     i.price = 12000
#     crud.create_item(db,i)

#     i = schemas.ItemCreate
#     i.title = "Nasi Goreng"
#     i.description = "Nasi goreng enak dan melimpahr"
#     i.img_name = "nasi_goreng.png"
#     i.price = 10000
#     crud.create_item(db,i)

#     i = schemas.ItemCreate
#     i.title = "Nasi Kuning"
#     i.description = "Nasi kuning lezat pisan"
#     i.img_name = "nasi_kuning.png"
#     i.price = 17000
#     crud.create_item(db,i)

#     i = schemas.ItemCreate
#     i.title = "Kupat Tahu"
#     i.description = "Kupat Tahu dengan kuah melimpah"
#     i.img_name = "kupat_tahu.png"
#     i.price = 5000
#     crud.create_item(db,i)

#     i = schemas.ItemCreate
#     i.title = "Pecel Lele"
#     i.description = "Pecel lele dengan ikan lele yang segar"
#     i.img_name = "pecel_lele.png"
#     i.price = 11000
#     crud.create_item(db,i)

#     i = schemas.ItemCreate
#     i.title = "Ayam Geprek"
#     i.description = "Pecel lele dengan ikan lele yang segar"
#     i.img_name = "ayam_geprek.png"
#     i.price = 11000
#     crud.create_item(db,i)

#     return {"message": "OK"}


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


# untuk debug saja, nanti rolenya admin?
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme) ):
#     usr =  verify_token(token)
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

#lihat detil user_id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token) 
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
























# tambah item ke keranjang
# response ada id (cart), sedangkan untuk paramater input  tidak ada id (cartbase)
@app.post("/carts/"  ) # response_model=schemas.Cart 
def create_item_user_cart(
    cart: schemas.CartBase, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token) #bisa digunakan untuk mengecek apakah user cocok (tdk boleh akses data user lain)
    return crud.create_cart(db=db, cart=cart)

# untuk semua isi cart, hanya untuk debug
# @app.get("/carts/", response_model=list[schemas.Cart])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
#     usr =  verify_token(token) #bisa digunakan untuk mengecek apakah user cocok (tdk boleh akses data user lain)
#     carts = crud.get_carts(db, skip=skip, limit=limit)
#     return carts

#ambil isi cart milik seorang user
@app.get("/carts/{user_id}", response_model=list[schemas.Cart])
def read_users(user_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token) #bisa digunakan untuk mengecek apakah user cocok (tdk boleh akses data user lain)
    carts = crud.get_carts_by_userid(db, user_id=user_id,skip=skip, limit=limit)
    return carts

# hapus item cart berdasarkan cart id
@app.delete("/carts/{cart_id}")
def delete_item_user_cart(cart_id:int,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme) ):
    usr =  verify_token(token) #bisa digunakan untuk mengecek apakah user cocok (tdk boleh akses data user lain)
    return crud.delete_cart_by_id(db,cart_id)


# hapus item cart berdasarkan user id
@app.delete("/clear_whole_carts_by_userid/{user_id}")
def delete_item_user_cart(user_id:int,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme) ):
    usr =  verify_token(token) #bisa digunakan untuk mengecek apakah user cocok (tdk boleh akses data user lain)
    return crud.delete_cart_by_userid(db,user_id=user_id)


#### ITEMS

# create item, tapi hanya untuk internal, role terpisah? nanti saja kalau sempat
# kalau sudah selsai disembunyikan agar mhs tdk menambah item random
# @app.post("/items/", response_model=schemas.ItemBase)
# def create_item(item: schemas.ItemBase, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
#     usr =  verify_token(token)
#     return crud.create_item(db=db, item=item)

# semua item
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# image item berdasarkan id
path_img = "../img/"
@app.get("/items_image/{item_id}")
def read_image(item_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)
    item = crud.get_item_by_id(db,item_id)
    if not(item):
        raise HTTPException(status_code=404, detail="id tidak valid")
    nama_image =  item.img_name # "bakso.png" #dummy
    if not(path.exists(path_img+nama_image)):
        raise HTTPException(status_code=404, detail="File dengan nama tersebut tidak ditemukan")
    
    fr =  FileResponse(path_img+nama_image)
    return fr   

# cari item berdasarkan deskripsi
@app.get("/search_items/{keyword}")
def cari_item(keyword:str,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token)

    return crud.get_item_by_keyword(db,keyword)

###################  status

#status diset manual dulu karena cukup rumit kalau ditangani constraitnya

#keranjang terisi --> user checkout dan siap bayar
@app.post("/set_status_harap_bayar/{user_id}")
def set_status_harap_bayar(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.insert_status(db=db,user_id=user_id,status="belum_bayar")

#user membayar
@app.post("/pembayaran/{user_id}")
def bayar(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.pembayaran(db=db,user_id=user_id)


#user sudah bayar --> penjual menerima 
@app.post("/set_status_penjual_terima/{user_id}")
def set_status_penjual_terima(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.insert_status(db=db,user_id=user_id,status="pesanan_diterima")

# user sudah bayar --> penjual menolak
# isi keranjang dikosongkan
@app.post("/set_status_penjual_tolak/{user_id}")
def set_status_penjual_terima(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    # isi cart dikosongkan
    crud.delete_cart_by_userid(db,user_id=user_id)
    return crud.insert_status(db=db,user_id=user_id,status="pesanan_ditolak")


# penjual menerima --> pesanan diantar
@app.post("/set_status_diantar/{user_id}")
def set_status_penjual_terima(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.insert_status(db=db,user_id=user_id,status="pesanaan_diantar")


# pesanan diantar -->pesanan diterima
@app.post("/set_status_diterima/{user_id}")
def set_status_penjual_terima(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    #cart dikosongkan
    #idealnya isi cart dipindahkan ke transaksi untuk arsip transaksi
    crud.delete_cart_by_userid(db,user_id=user_id)
    return crud.insert_status(db=db,user_id=user_id,status="pesanan_selesai")


@app.get("/get_status/{user_id}")
def last_status(user_id:int,  db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token) #bisa digunakan untuk mengecek apakah user cocok (tdk boleh akses data user lain)
    return crud.get_last_status(db,user_id)


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
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)    # .now(datetime.UTC)
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
