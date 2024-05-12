from sqlalchemy.orm import Session
import models, schemas
import bcrypt
from sqlalchemy import desc

# replaced
SALT = b'$2b$12$UoS.62CnRhwU6YGBLYx.6.'

######### user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# get 100 users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# delete semua user
def delete_all_user(db: Session):
    jum_rec = db.query(models.User).delete()
    db.commit()
    return jum_rec

# 
def hashPassword(passwd: str):
    bytePwd = passwd.encode('utf-8')
    pwd_hash = bcrypt.hashpw(bytePwd, SALT)
    return pwd_hash










############  untuk cart ============================ GANTI INI WOY
def create_cart(db: Session, cart: schemas.Cart):
    db_cart = models.Cart(user_id = cart.user_id, item_id = cart.item_id, quantity = cart.quantity )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def delete_cart_by_id(db: Session, id_cart:int):
    hasil = db.query(models.Cart).filter(models.Cart.id == id_cart).delete()
    db.commit()
    return {"record_dihapus":hasil} 

# ada hapus semua cart berdasarkan user
# asumsikan kalau sudah selesai (sudah sampai ke user), isi cart dikosongkan
def delete_cart_by_userid(db: Session, user_id:int):
    hasil = db.query(models.Cart).filter(models.Cart.user_id == user_id).delete()
    db.commit()
    return {"record_dihapus":hasil} 

# semua belanja semua user, untuk debug, jangan digunakan
# def get_carts(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Cart).offset(skip).limit(limit).all()

def get_carts_by_userid(db: Session, user_id:int, skip: int = 0, limit: int = 100 ):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).offset(skip).limit(limit).all()

# true kalau keranjang kosong
def get_is_carts_empty_userid(db: Session, user_id:int):
    exists = db.query(models.Cart.id).filter(models.Cart.user_id == user_id).exists()
    if db.query(exists).scalar():
        return False
    else:
        return True

# ============
# status dan pembayaran

def pembayaran (db: Session, user_id:int):
    status = get_last_status(db,user_id=user_id)
    # hanya proses yang statusnya belum_bayar, selain itu abaikan 
    temp = status["status"]
    if temp.status=="belum_bayar":
        insert_status(db=db,user_id=user_id,status="sudah_bayar")
        return {"status":"status diupdate sudah bayar"}
    else:
        return {"status":"tidak diproses, cek status"}

def insert_status(db:Session, user_id:int, status: str):
    db_status = models.Status(user_id = user_id, status = status )
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

#   keranjang_kosong, belum_bayar, bayar, (pesanan_diterima atau pesanan_batal), pesanan_diproses, pesanaan_diantar, 
def get_last_status(db: Session,user_id:int):
    last_status = db.query(models.Status).filter(models.Status.user_id == user_id).order_by(desc(models.Status.timestamp)).first()
    if last_status:
        return {"status":last_status}
    else:
        #tidak ada status, cek cart
        if get_is_carts_empty_userid(db,user_id=user_id):
            #kosong, update status
            insert_status(db,user_id=user_id,status="keranjang_kosong")
            return get_last_status(db,user_id=user_id)

##==================== item

# ambil semua item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# ambil item dengan id tertentu
def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


# ambil item yang cocok dengan keyword di deskripsi
def get_item_by_keyword(db: Session, keyword: str):
    #Artikel.Benennung.like("%"+prop+"%")
    return db.query(models.Item).filter(models.Item.description.ilike("%"+keyword+"%")).all()
    #return db.query(models.Item).filter(models.Item.like("%"+keyword+"%")).first()

# tambah item
def create_item(db: Session, item: schemas.ItemBase):
    db_item = models.Item(title=item.title, description = item.description, price = item.price, img_name = item.img_name )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# delete semua item
def delete_all_item(db: Session):
    jum_rec = db.query(models.Item).delete()
    db.commit()
    return jum_rec