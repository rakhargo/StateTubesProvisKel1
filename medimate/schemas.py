from pydantic import BaseModel


# item
class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    img_name:str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True

# user

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True


# cart

# shopping cart
class CartBase(BaseModel):
    item_id : int
    user_id : int
    quantity : int  

class Cart(CartBase):
    id : int
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
