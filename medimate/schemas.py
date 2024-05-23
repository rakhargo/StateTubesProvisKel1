from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from typing import Optional

###############################
# user and token

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

###############################
# profile

class ProfileBase(BaseModel):
    nama: str
    tanggalLahir: date
    jenisKelamin: str
    alamat: str
    email: str
    noTelepon: str
    userPhoto: Optional[str] = None
    userId: int

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

    @field_validator("tanggalLahir")
    def parse_tanggal_lahir(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

###############################
# doctor

class DoctorBase(BaseModel):
    nama: str
    spesialisasi: str
    pengalaman: int
    foto: str

class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True

###############################
# appointment

class AppointmentBase(BaseModel):
    patientId: int
    doctorId: int
    facilityId: int
    status: str
    waktu: Optional[datetime]

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True

    @field_validator("waktu")
    def parse_waktu(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
    

###############################
# article

class HealthArticle(BaseModel):
    id: int
    title: str
    content: str
    coverImage: str
    topics: str
    recommendedDoctors: int
    references: str

    class Config:
        orm_mode = True

###############################
# health facillity

class HealthFacility(BaseModel):
    id: int
    namaFasilitas: str
    alamatFasilitas: str
    kecamatanFasilitas: str
    kotaKabFasilitas: str
    kodePosFasilitas: str
    tingkatFasilitas: str
    jumlahPoliklinik: str
    daftarPoliklinik: str
    fotoFaskes: str
    logoFaskes: str

    class Config:
        orm_mode = True

###############################
# medical record

class MedicalRecordBase(BaseModel):
    patientId: int
    dateTime: Optional[datetime]
    jenisTes: str
    hasilTes: str

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    pass

class MedicalRecord(MedicalRecordBase):
    id: int

    class Config:
        orm_mode = True

    @field_validator("dateTime")
    def parse_dateTime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

###############################
# Refferal

class ReferralRead(BaseModel):
    id: int
    fromFacilityId: int
    toFacilityId: int
    patientId: int
    tanggal: date
    alasan: str

    class Config:
        orm_mode = True

###############################
# Review

class ReviewBase(BaseModel):
    reviewerId: int
    revieweeDoctorId: int
    revieweeFaskesId: int
    rating: int
    komentar: str
    tanggal: date

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True

    @field_validator("tanggal")
    def parse_tanggal(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value
    

###############################
# service

class Service(BaseModel):
    id: int
    icon: str
    nama: str
    childText: str
    status: str

    class Config:
        orm_mode = True

###############################
# specialist and polyclinic

class SpecialistAndPolyclinic(BaseModel):
    id: int
    icon: str
    name: str

    class Config:
        orm_mode = True
