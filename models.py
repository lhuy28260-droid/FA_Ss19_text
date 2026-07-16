from database import Base , Relationship
from sqlalchemy import Integer , Float , Column , String , ForeignKey
class Clinic(Base):
    __tablename__ = "clinics"
    id = Column(String(20),primary_key=True)
    clinic_name = Column(String(50),nullable=False)
    specialty = Column(String(50),nullable=False)

class Doctor(Base):
    id = Column(Integer,primary_key=True,autoincrement=True)
    doctor_code = Column(String(50),nullable=False,unique=True)
    salary = Column(Float,nullable=False)
    clinic_id = Column(String(20),ForeignKey("clinic_id"))
    clinic = Relationship("clinic",Base)

class License(Base):
    id = Column(Integer,primary_key=True,autoincrement=True)
    license_number = Column(String(30),nullable=False,unique=True)
    issue_by = Column(String(100),nullable=False)
    doctor_id = Column(Integer,ForeignKey("doctor_id"))
    doctor_id 