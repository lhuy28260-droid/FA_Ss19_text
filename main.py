from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import engine, get_db
from .models import Base
from . import schemas, service

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic Management API")


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc.orig)
        }
    )


@app.post("/clinics",response_model=schemas.ClinicResponse,status_code=201)
def create_clinic(clinic: schemas.ClinicCreate,db: Session = Depends(get_db)):
    try:
        return service.create_clinic(db, clinic)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Cannot create clinic"
        )


@app.get("/clinics",response_model=schemas.ClinicListResponse)
def get_clinics(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    db: Session = Depends(get_db)
):
    return service.get_clinics(
        db,
        page,
        limit,
        search
    )


@app.get("/clinics/{clinic_id}",response_model=schemas.ClinicDetailResponse)
def get_clinic(clinic_id: int,db: Session = Depends(get_db)):
    clinic = service.get_clinic_by_id(db,clinic_id)

    if clinic is None:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    return clinic


@app.post("/doctors",response_model=schemas.DoctorResponse,status_code=201)
def create_doctor(doctor: schemas.DoctorCreate,db: Session = Depends(get_db)):
    try:
        return service.create_doctor(db,doctor)

    except ValueError as e:

        if str(e) == "Doctor code already exists":
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Cannot create doctor"
        )


@app.get("/doctors",response_model=list[schemas.DoctorResponse])
def get_doctors_by_clinic(clinic_id: int,db: Session = Depends(get_db)):
    return service.get_doctors_by_clinic(db,clinic_id)


@app.get("/doctors/{doctor_id}",response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int,db: Session = Depends(get_db)):
    doctor = service.get_doctor_by_id(db,doctor_id)

    if doctor is None:
        raise HTTPException(status_code=404,detail="Doctor not found")

    return doctor


@app.patch("/doctors/{doctor_id}",response_model=schemas.DoctorResponse)
def update_doctor(doctor_id: int,doctor_update: schemas.DoctorUpdate,db: Session = Depends(get_db)):
    try:
        doctor = service.update_doctor(
            db,
            doctor_id,
            doctor_update
        )

        if doctor is None:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        return doctor

    except ValueError as e:

        if str(e) == "Doctor code already exists":
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Cannot update doctor"
        )


@app.delete("/licenses/{license_id}")
def delete_license(license_id: int,db: Session = Depends(get_db)):
    deleted = service.delete_license(db,license_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )

    return {
        "message": "Deleted"
    }