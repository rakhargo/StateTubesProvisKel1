from sqlalchemy.orm import Session
import models, schemas
import bcrypt
from sqlalchemy import desc

# replaced
SALT = b'$2b$12$UoS.62CnRhwU6YGBLYx.6.'

#######################################################################################################
# User

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

# hash password
def hashPassword(passwd: str):
    bytePwd = passwd.encode('utf-8')
    pwd_hash = bcrypt.hashpw(bytePwd, SALT)
    return pwd_hash

#######################################################################################################
# profile

# Create Profile
def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Get Profile by profile id
def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

# Get Profile by User ID
def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(models.Profile).filter(models.Profile.userId == user_id).first()

# Update Profile
def update_profile(db: Session, profile_id: int, profile: schemas.ProfileUpdate):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if db_profile:
        for key, value in profile.model_dump(exclude_unset=True).items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile

# Delete Profile
def delete_profile(db: Session, profile_id: int):
    db.query(models.Profile).filter(models.Profile.id == profile_id).delete()
    db.commit()
    return {"message": "Profile deleted successfully"}

#######################################################################################################
# Doctor

# Get Doctor by ID
def get_doctor_id(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

# Get all doctors
def get_all_doctors(db: Session):
    return db.query(models.Doctor).all()

#######################################################################################################
# Appointments

# Create Appointment
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# Get Appointment
def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

# Get Appointments by Profile ID
def get_appointments_by_profile_id(db: Session, profile_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patientId == profile_id).all()

# Update Appointment
def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentUpdate):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment:
        for key, value in appointment.model_dump(exclude_unset=True).items():
            setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment

# Delete Appointment
def delete_appointment(db: Session, appointment_id: int):
    db.query(models.Appointment).filter(models.Appointment.id == appointment_id).delete()
    db.commit()
    return {"message": "Appointment deleted successfully"}

# Get all Appointments
def get_all_appointments(db: Session):
    return db.query(models.Appointment).all()

#######################################################################################################
# Articles

# Get Health Article by ID
def get_health_article(db: Session, article_id: int):
    return db.query(models.HealthArticle).filter(models.HealthArticle.id == article_id).first()

# Get all Health Articles
def get_all_health_articles(db: Session):
    return db.query(models.HealthArticle).all()

#######################################################################################################
# health facility

# Get Health Facility by ID
def get_health_facility_by_id(db: Session, facility_id: int):
    return db.query(models.HealthFacility).filter(models.HealthFacility.id == facility_id).first()

# Get all Health Facilities
def get_all_health_facilities(db: Session):
    return db.query(models.HealthFacility).all()

#######################################################################################################
# medical records

# Get Medical Records by Profile ID
def get_medical_records_by_profile_id(db: Session, profile_id: int):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.patientId == profile_id).all()

# Get Medical Record by ID
def get_medical_record(db: Session, record_id: int):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.id == record_id).first()

# Update Medical Record
def update_medical_record(db: Session, record_id: int, record: schemas.MedicalRecordUpdate):
    db_record = db.query(models.MedicalRecord).filter(models.MedicalRecord.id == record_id).first()
    if db_record:
        for key, value in record.model_view(exclude_unset=True).items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

#######################################################################################################
# refferals

# Get Referral by ID
def get_referral(db: Session, referral_id: int):
    return db.query(models.Referral).filter(models.Referral.id == referral_id).first()

# Get all Referrals
def get_all_referrals(db: Session):
    return db.query(models.Referral).all()

#######################################################################################################
# review

# Create Review
def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.model_view())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Get Review by ID
def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

# Get all Reviews
def get_all_reviews(db: Session):
    return db.query(models.Review).all()

# Get Reviews by Doctor ID
def get_reviews_by_doctor_id(db: Session, doctor_id: int):
    return db.query(models.Review).filter(models.Review.revieweeDoctorId == doctor_id).all()

# Get Reviews by Facility (Faskes) ID
def get_reviews_by_facility_id(db: Session, facility_id: int):
    return db.query(models.Review).filter(models.Review.revieweeFaskesId == facility_id).all()

#######################################################################################################
# service

# Get all services
def get_all_services(db: Session):
    return db.query(models.Services).all()

# Get Service by ID
def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Services).filter(models.Services.id == service_id).first()

#######################################################################################################
# polyclinic

# Get all polyclinic
def get_all_specialist_and_polyclinics(db: Session):
    return db.query(models.SpecialistAndPolyclinic).all()

# Get Polyclinic by ID
def get_polyclinic_by_id(db: Session, polyclinic_id: int):
    return db.query(models.SpecialistAndPolyclinic).filter(models.SpecialistAndPolyclinic.id == polyclinic_id).first()