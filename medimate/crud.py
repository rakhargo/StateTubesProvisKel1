from sqlalchemy.orm import Session,  joinedload
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
    return db.query(models.Profile).filter(models.Profile.userId == user_id)

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
# profile relation

# Get profile relation by ID
def get_relation_id(db: Session, relation_id: int):
    return db.query(models.ProfileRelation).filter(models.ProfileRelation.id == relation_id).first()

# Get all profile relation
def get_all_profile_relations(db: Session):
    return db.query(models.ProfileRelation).all()

#######################################################################################################
# Doctor

# Get Doctor by ID
def get_doctor_id(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

# Get Doctor by poly ID
def get_doctor_poly_id(db: Session, poly_id: int):
    return db.query(models.Doctor).filter(models.Doctor.polyId == poly_id).all()

# Get all doctors
def get_all_doctors(db: Session):
    return db.query(models.Doctor).all()

#######################################################################################################
# Doctor Schedule

# Create Doctor Schedule
def create_doctor_schedule(db: Session, doctorSchedule: schemas.DoctorScheduleCreate):
    db_doctorSchedule = models.DoctorSchedule(**doctorSchedule.model_dump())
    db.add(db_doctorSchedule)
    db.commit()
    db.refresh(db_doctorSchedule)
    return db_doctorSchedule

# Update Doctor Schedule
def update_doctor_schedule(db: Session, doctor_schedule_id: int, doctorSchedule: schemas.DoctorScheduleUpdate):
    db_doctorSchedule = db.query(models.DoctorSchedule).filter(models.DoctorSchedule.id == doctor_schedule_id).first()
    if db_doctorSchedule:
        for key, value in doctorSchedule.model_dump(exclude_unset=True).items():
            setattr(db_doctorSchedule, key, value)
        db.commit()
        db.refresh(db_doctorSchedule)
    return db_doctorSchedule

# Get Doctor Schedule by ID
def get_doctor_schedule_id(db: Session, doctorSchedule_id: int):
    return db.query(models.DoctorSchedule).filter(models.DoctorSchedule.id == doctorSchedule_id).first()

# Get Doctor Schedule by doctor ID
def get_doctor_schedule_doctor_id(db: Session, doctor_id: int):
    return db.query(models.DoctorSchedule).filter(models.DoctorSchedule.doctorId == doctor_id).all()

# Get all doctors
def get_all_doctor_schedules(db: Session):
    return db.query(models.DoctorSchedule).all()

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
    return db.query(models.Appointment).\
            options(joinedload(models.Appointment.doctor), joinedload(models.Appointment.facility)).\
            filter(models.Appointment.id == appointment_id).first()

# Get Appointments by Profile ID
def get_appointments_by_profile_id(db: Session, profile_id: int):
    return db.query(models.Appointment).\
            options(joinedload(models.Appointment.doctor), joinedload(models.Appointment.facility)).\
            filter(models.Appointment.patientId == profile_id).all()

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

# Get Medical Records by appointment ID
def get_medical_records_by_appointment_id(db: Session, appointment_id: int):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.appointmentId == appointment_id).first()

# Get Medical Record by ID
def get_medical_record(db: Session, record_id: int):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.id == record_id).first()

# Create Medical Record
def create_medical_record(db: Session, medical_record: schemas.MedicalRecordCreate):
    db_medical_record = models.MedicalRecord(**medical_record.model_dump())
    db.add(db_medical_record)
    db.commit()
    db.refresh(db_medical_record)
    return db_medical_record

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
# referral

# Create Referral
def create_referral(db: Session, referral: schemas.ReferralCreate):
    db_referral = models.Referral(**referral.model_dump())
    db.add(db_referral)
    db.commit()
    db.refresh(db_referral)
    return db_referral

# Get referral by ID
def get_referral(db: Session, referral_id: int):
    return db.query(models.Referral).filter(models.Referral.id == referral_id).first()

#######################################################################################################
# relasiDokterRsPoli

# Get RelasiDokterRsPoli by ID
def get_relasi_dokter_rs_poli(db: Session, relasi_dokter_rs_poli_id: int):
    return db.query(models.RelasiDokterRsPoli).filter(models.RelasiDokterRsPoli.id == relasi_dokter_rs_poli_id).first()

# Get RelasiDokterRsPoli by ID
def get_relasi_dokter_rs_poli_id_id(db: Session, relasi_dokter_rs_poli_id: int, doctor_id:int):
    return db.query(models.RelasiDokterRsPoli).filter(models.RelasiDokterRsPoli.relasiRsPoliId == relasi_dokter_rs_poli_id, models.RelasiDokterRsPoli.doctorId == doctor_id).first()

# Get RelasiDokterRsPoli by doctorID
def get_relasi_dokter_rs_poli_doctor_id(db: Session, doctor_id: int):
    return db.query(models.RelasiDokterRsPoli).filter(models.RelasiDokterRsPoli.doctorId == doctor_id).all()

# Get RelasiDokterRsPoli by relasi rs poli id
def get_relasi_dokter_rs_poli_relasirspoli_id(db: Session, relasirspoli_id: int):
    return db.query(models.RelasiDokterRsPoli).filter(models.RelasiDokterRsPoli.relasiRsPoliId == relasirspoli_id).all()

# Get all RelasiDokterRsPoli
def get_all_relasi_dokter_rs_poli(db: Session):
    return db.query(models.RelasiDokterRsPoli).all()

#######################################################################################################
# relasiJudulPoli

# Get RelasiJudulPoli by ID
def get_relasi_judul_poli(db: Session, relasi_judul_poli_id: int):
    return db.query(models.RelasiJudulPoli).filter(models.RelasiJudulPoli.id == relasi_judul_poli_id).first()

# Get RelasiJudulPoli by poly ID
def get_relasi_judul_poli_id(db: Session, poli_id: int):
    return db.query(models.RelasiJudulPoli).filter(models.RelasiJudulPoli.polyclinicId == poli_id).all()

# Get all RelasiJudulPoli
def get_all_relasi_judul_poli(db: Session):
    return db.query(models.RelasiJudulPoli).all()

#######################################################################################################
# relasiRsPoli

# Get RelasiRsPoli by ID
def get_relasi_rs_poli(db: Session, relasi_rs_poli_id: int):
    return db.query(models.RelasiRsPoli).filter(models.RelasiRsPoli.id == relasi_rs_poli_id).first()

# Get RelasiRsPoli by poly ID
def get_relasi_rs_poli_id(db: Session, poli_id: int):
    return db.query(models.RelasiRsPoli).filter(models.RelasiRsPoli.poliId == poli_id).all()

# Get RelasiRsPoli by rs ID
def get_relasi_rs_poli_rs_id(db: Session, rs_id: int):
    return db.query(models.RelasiRsPoli).filter(models.RelasiRsPoli.rsId == rs_id).all()

# Get all RelasiRsPoli
def get_all_relasi_rs_poli(db: Session):
    return db.query(models.RelasiRsPoli).all()

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