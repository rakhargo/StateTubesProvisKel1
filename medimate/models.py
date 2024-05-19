from database import BaseDB
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy import DateTime
from sqlalchemy.ext.hybrid import hybrid_property

class User(BaseDB):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique = True, index = True)
    hashed_password = Column(String)

class Profile(BaseDB):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    nama = Column(String, unique=True, index=True)
    tanggalLahir = Column(Date)
    jenisKelamin = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    noTelepon = Column(String, nullable=False)
    email = Column(String, nullable=False)
    userPhoto = Column(String)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)

    @hybrid_property
    def formatted_tanggal_lahir(self):
        return self.tanggal_lahir.strftime("%d %m %Y")

class Doctor(BaseDB):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    nama = Column(String, unique=True, index=True)
    spesialisasi = Column(String, nullable=False)
    pengalaman = Column(Integer, nullable=False)
    foto = Column(String)

class Appointment(BaseDB):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True)
    patientId = Column(Integer, ForeignKey('profile.id'), nullable=False)
    doctorId = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    facilityId = Column(Integer, ForeignKey('healthFacility.id'), nullable=False)
    status = Column(String, nullable=False)
    waktu = Column(DateTime)

    @hybrid_property
    def formatted_dateTime(self):
        return self.dateTime.strftime("%d %m %Y %H:%M:%S")

class HealthArticle(BaseDB):
    __tablename__ = "healthArticle"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    coverImage = Column(String, nullable=False)
    topics = Column(String, nullable=False)
    recommendedDoctors = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    references = Column(String, nullable=False)
    
class HealthFacility(BaseDB):
    __tablename__ = "healthFacility"
    id = Column(Integer, primary_key=True)
    namaFasilitas = Column(String, nullable=False)
    alamatFasilitas = Column(String, nullable=False)
    kecamatanFasilitas = Column(String, nullable=False)
    kotaKabFasilitas = Column(String, nullable=False)
    kodePosFasilitas = Column(String, nullable=False)
    tingkatFasilitas = Column(String, nullable=False)
    jumlahPoliklinik = Column(String, nullable=False)
    daftarPoliklinik = Column(String, nullable=False)
    fotoFaskes = Column(String)
    logoFaskes = Column(String)

class MedicalRecord(BaseDB):
    __tablename__ = "medicalRecord"
    id = Column(Integer, primary_key=True)
    patientId = Column(Integer, ForeignKey('profile.id'), nullable=False)
    dateTime = Column(DateTime)
    jenisTes = Column(String, nullable=False)
    hasilTes = Column(String, nullable=False)

    @hybrid_property
    def formatted_dateTime(self):
        return self.tanggal.strftime("%d %m %Y %H:%M:%S")

class Referral(BaseDB):
    __tablename__ = "referral"
    id = Column(Integer, primary_key=True)
    fromFacilityId = Column(Integer, ForeignKey('healthFacility.id'), nullable=False)
    toFacilityId = Column(Integer, ForeignKey('healthFacility.id'), nullable=False)
    patientId = Column(Integer, ForeignKey('profile.id'), nullable=False)
    tanggal = Column(Date)
    alasan = Column(String, nullable=False)

    @hybrid_property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")

class Review(BaseDB):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    reviewerId = Column(Integer, ForeignKey('profile.id'), nullable=False)
    revieweeDoctorId = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    revieweeFaskesId = Column(Integer, ForeignKey('faskes.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    komentar = Column(String, nullable=False)
    tanggal = Column(Date)

    @hybrid_property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")

class Services(BaseDB):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    icon = Column(String)
    nama = Column(String, nullable=False)
    childText = Column(String, nullable=False)
    status = Column(String, nullable=False)


class SpecialistAndPolyclinic(BaseDB):
    __tablename__ = "specialistAndPolyclinic"
    id = Column(Integer, primary_key=True)
    icon = Column(String)
    name = Column(String, nullable=False)