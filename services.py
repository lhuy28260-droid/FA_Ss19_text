from typing import Optional
from sqlalchemy.orm import Session

from .models import Clinic, Doctor, License
from .schemas import ClinicCreate, DoctorCreate, DoctorUpdate


def create_clinic(db: Session, clinic_data: ClinicCreate) -> Clinic:
    clinic = Clinic(**clinic_data.model_dump())

    try:
        db.add(clinic)
        db.commit()
        db.refresh(clinic)
        return clinic
    except Exception:
        db.rollback()
        raise


def get_clinic_by_id(db: Session, clinic_id: int) -> Optional[Clinic]:
    return db.query(Clinic).filter(Clinic.id == clinic_id).first()


def get_clinics(db: Session,page: int = 1,limit: int = 10,search: str = ""):
    query = db.query(Clinic)

    if search:
        query = query.filter(Clinic.clinic_name.like(f"%{search}%"))

    total = query.count()

    clinics = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "data": clinics
    }


def create_doctor(db: Session,doctor_data: DoctorCreate) -> Doctor:

    clinic = db.query(Clinic).filter(Clinic.id == doctor_data.clinic_id).first()

    if clinic is None:
        raise ValueError("Clinic does not exist")

    exist = db.query(Doctor).filter(Doctor.doctor_code == doctor_data.doctor_code).first()

    if exist:
        raise ValueError("Doctor code already exists")

    doctor = Doctor(**doctor_data.model_dump())

    try:
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        return doctor

    except Exception:
        db.rollback()
        raise


def get_doctor_by_id(db: Session,doctor_id: int) -> Optional[Doctor]:

    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_doctors_by_clinic(db: Session,clinic_id: int):
    return db.query(Doctor).filter(Doctor.clinic_id == clinic_id).all()


def update_doctor(db: Session,doctor_id: int,doctor_update: DoctorUpdate) -> Optional[Doctor]:

    doctor = get_doctor_by_id(db, doctor_id)

    if doctor is None:
        return None

    update_data = doctor_update.model_dump(exclude_unset=True)

    if "clinic_id" in update_data:
        clinic = db.query(Clinic).filter(Clinic.id == update_data["clinic_id"]).first()

        if clinic is None:
            raise ValueError("Clinic does not exist")

    if "doctor_code" in update_data:
        exist = db.query(Doctor).filter(Doctor.doctor_code == update_data["doctor_code"],Doctor.id != doctor_id).first()

        if exist:
            raise ValueError("Doctor code already exists")

    for key, value in update_data.items():
        setattr(doctor, key, value)

    try:
        db.commit()
        db.refresh(doctor)
        return doctor

    except Exception:
        db.rollback()
        raise


def delete_license(db: Session,license_id: int) -> bool:

    license = db.query(License).filter(
        License.id == license_id
    ).first()

    if license is None:
        return False

    try:
        db.delete(license)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise

