from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time, datetime
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
        from_attributes = True

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
    isMainProfile: int

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("tanggalLahir")
    def parse_tanggal_lahir(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

    @property
    def formatted_tanggal_lahir(self):
        return self.tanggalLahir.strftime("%d %m %Y")

###############################
# profileRelation

class ProfileRelationBase(BaseModel):
    relation: str

class ProfileRelationCreate(ProfileRelationBase):
    pass

class ProfileRelationUpdate(ProfileRelationBase):
    pass

class ProfileRelation(ProfileRelationBase):
    id: int

    class Config:
        from_attributes = True

###############################
# doctor

class DoctorBase(BaseModel):
    nama: str
    pengalaman: int
    foto: str
    polyId: int

class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True

###############################
# appointment

class AppointmentBase(BaseModel):
    patientId: int
    doctorId: int
    facilityId: int
    status: str
    waktu: str
    metodePembayaran: str
    antrian: int
    relasiJudulPoliId: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        from_attributes = True

    # @field_validator("waktu")
    # def parse_waktu(cls, value):
    #     if isinstance(value, str):
    #         return int(value)
    #     return value

###############################
# Doctor Schedule

class DoctorScheduleBase(BaseModel):
    tanggal: date
    mulai: time
    selesai: time
    maxBooking: int
    currentBooking: int
    doctorId: int

class DoctorScheduleCreate(DoctorScheduleBase):
    pass

class DoctorScheduleUpdate(DoctorScheduleBase):
    pass

class DoctorSchedule(DoctorScheduleBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("tanggal")
    def parse_tanggal(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

    @field_validator("mulai")
    def parse_mulai(cls, value):
        if isinstance(value, str):
            return time.fromisoformat(value)
        return value

    @field_validator("selesai")
    def parse_selesai(cls, value):
        if isinstance(value, str):
            return time.fromisoformat(value)
        return value

    @property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")
    
    @property
    def formatted_mulai(self):
        return self.mulai.strftime("%H:%M:%S")
    
    @property
    def formatted_selesai(self):
        return self.selesai.strftime("%H:%M:%S")

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
        from_attributes = True

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
        from_attributes = True

###############################
# medical record

class MedicalRecordBase(BaseModel):
    patientId: int
    date: Optional[date]
    appointmentId: int
    relasiJudulPoliId : int

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    pass

class MedicalRecord(MedicalRecordBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("date")
    def parse_dateTime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

###############################
# Referral

class ReferralBase(BaseModel):
    fromFacilityId: int
    toFacilityId: int
    patientId: int
    tanggal: date
    alasan: str

class ReferralCreate(ReferralBase):
    pass

class ReferralDelete(ReferralBase):
    pass

class Referral(ReferralBase):
    id: int
    class Config:
        from_attributes = True

###############################
# relasiDokterRsPoli

class RelasiDokterRsPoliBase(BaseModel):
    doctorId: int
    relasiRsPoliId: int

class RelasiDokterRsPoliCreate(RelasiDokterRsPoliBase):
    pass

class RelasiDokterRsPoliUpdate(RelasiDokterRsPoliBase):
    pass

class RelasiDokterRsPoli(RelasiDokterRsPoliBase):
    id: int

    class Config:
        from_attributes = True

###############################
# relasiJudulPoli

class RelasiJudulPoliBase(BaseModel):
    judul: str
    tindakan: str
    polyclinicId: int

class RelasiJudulPoliCreate(RelasiJudulPoliBase):
    pass

class RelasiJudulPoliUpdate(RelasiJudulPoliBase):
    pass

class RelasiJudulPoli(RelasiJudulPoliBase):
    id: int

    class Config:
        from_attributes = True

###############################
# relasiRsPoli

class RelasiRsPoliBase(BaseModel):
    rsId: int
    poliId: int

class RelasiRsPoliCreate(RelasiRsPoliBase):
    pass

class RelasiRsPoliUpdate(RelasiRsPoliBase):
    pass

class RelasiRsPoli(RelasiRsPoliBase):
    id: int

    class Config:
        from_attributes = True

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
        from_attributes = True

    @field_validator("tanggal")
    def parse_tanggal(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value
    
    @property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")

###############################
# service

class Service(BaseModel):
    id: int
    icon: str
    name: str
    childText: str
    status: str

    class Config:
        from_attributes = True

###############################
# specialist and polyclinic

class SpecialistAndPolyclinic(BaseModel):
    id: int
    icon: str
    name: str

    class Config:
        from_attributes = True
