# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey,Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()


class Specialization(Base):
    __tablename__ = 'specialization'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # Relationships - corrected names to match the back_populates in related models
    internal_doctors = relationship("InternalDoctor", back_populates="specialization")
    external_doctors = relationship("ExternalDoctor", back_populates="specialization")
    diagnoses = relationship("Diagnosis", back_populates="specialization")

    def __repr__(self):
        return f"Specialization(id={self.id}, name={self.name})"


class DoctorMixin:
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    specialization_id = Column('specialization', Integer, ForeignKey('specialization.id'), nullable=False)


class InternalDoctor(DoctorMixin, Base):
    __tablename__ = 'internal_doctor'

    # Relationships
    specialization = relationship("Specialization", back_populates="internal_doctors")
    visits = relationship("Visit", back_populates="internal_doctor")
    prescriptions = relationship("Prescribe", back_populates="doctor")


    def __repr__(self):
        return f"InternalDoctor(id={self.id}, name={self.name}, surname={self.surname})"


class ExternalDoctor(DoctorMixin, Base):
    __tablename__ = 'external_doctor'

    street = Column(String(50))
    postcode = Column(String(10))
    city = Column(String(50))

    # Relationships
    specialization = relationship("Specialization", back_populates="external_doctors")
    visits = relationship("Visit", back_populates="external_doctor")

    def __repr__(self):
        return f"ExternalDoctor(id={self.id}, name={self.name}, surname={self.surname})"


class Diagnosis(Base):
    __tablename__ = 'diagnosis'

    code = Column(Integer, primary_key=True)
    text = Column(String(100))
    specialization_id = Column('specialization', Integer, ForeignKey('specialization.id'), nullable=False)

    # Relationships
    specialization = relationship("Specialization", back_populates="diagnoses")
    reports = relationship("Report", back_populates="diagnosis")

    def __repr__(self):
        return f"Diagnosis(code={self.code}, text={self.text})"


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    birthdate = Column(Date)
    street = Column(String(50))
    postcode = Column(String(10))
    city = Column(String(50))

    # Relationships
    visits = relationship("Visit", back_populates="patient")
    prescriptions = relationship("Prescribe", back_populates="patient")


    def __repr__(self):
        return f"Patient(id={self.id}, name={self.name}, surname={self.surname})"


class Visit(Base):
    __tablename__ = 'visit'

    v_number = Column(Integer, primary_key=True)
    v_date = Column(Date)
    internal_doctor_id = Column('internal_doctor', Integer, ForeignKey('internal_doctor.id'), nullable=False)
    external_doctor_id = Column('external_doctor', Integer, ForeignKey('external_doctor.id'), nullable=False)
    patient_id = Column('patient', Integer, ForeignKey('patient.id'), nullable=False)

    # Relationships
    internal_doctor = relationship("InternalDoctor", back_populates="visits")
    external_doctor = relationship("ExternalDoctor", back_populates="visits")
    patient = relationship("Patient", back_populates="visits")
    reports = relationship("Report", back_populates="visit")
    prescriptions = relationship("Prescribe", back_populates="visit")


    def __repr__(self):
        return f"Visit(v_number={self.v_number}, v_date={self.v_date})"


class Report(Base):
    __tablename__ = 'report'

    visit_id = Column('visit', Integer, ForeignKey('visit.v_number'), primary_key=True)
    diagnosis_id = Column('diagnosis', Integer, ForeignKey('diagnosis.code'), primary_key=True)

    # Relationships
    visit = relationship("Visit", back_populates="reports")
    diagnosis = relationship("Diagnosis", back_populates="reports")

    def __repr__(self):
        return f"Report(visit_id={self.visit_id}, diagnosis_id={self.diagnosis_id})"

############################################################################################################3333
class Drug(Base):
    __tablename__ = 'drug'

    id = Column(Integer, primary_key=True)
    drug_name = Column(String(100), nullable=False)
    strength = Column(Integer, nullable=False)

    prescriptions = relationship("Prescribe", back_populates="drug")

    def __repr__(self):
        return f"Drug(id={self.id}, name={self.drug_name}, strength={self.strength})"

class Repeat(Base):
    __tablename__ = 'repeat'

    id = Column(Integer, primary_key=True)
    max_times = Column(Integer, nullable=False)
    interval = Column(Integer, nullable=False)

    prescriptions = relationship("Prescribe", back_populates="repeat")

    def __repr__(self):
        return f"Repeat(id={self.id}, max_times={self.max_times}, interval={self.interval})"

class Prescribe(Base):
    __tablename__ = 'prescribe'

    id = Column(Integer, primary_key=True)
    presc_date = Column(Date, nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('internal_doctor.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    direction = Column(String(100))
    dosage = Column(Integer, nullable=False)
    drug_id = Column(Integer, ForeignKey('drug.id'), nullable=False)
    repeat_id = Column(Integer, ForeignKey('repeat.id'))
    visit_id = Column(Integer, ForeignKey('visit.v_number'))

    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("InternalDoctor", back_populates="prescriptions")
    drug = relationship("Drug", back_populates="prescriptions")
    repeat = relationship("Repeat", back_populates="prescriptions")
    visit = relationship("Visit", back_populates="prescriptions")

    def __repr__(self):
        return f"Prescribe(id={self.id}, date={self.presc_date}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, drug_id={self.drug_id}, visit_id={self.visit_id})"
