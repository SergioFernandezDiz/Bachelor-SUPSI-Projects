from sqlalchemy import select, func
from models import InternalDoctor, Visit, Patient, Report, Diagnosis, ExternalDoctor, Drug, Prescribe, Repeat
from sqlalchemy import text
from datetime import datetime
import time


# Finds all internal doctors named "Daniel" ordered by their ID.
def find_daniel_doctors(session):
    stmt = (
        select(InternalDoctor)
        .where(func.lower(InternalDoctor.name) == 'daniel')
        .order_by(InternalDoctor.id)
    )
    return session.execute(stmt).scalars().all()

# Counts the number of visits recorded before 2002.
def count_old_visits(session):
    stmt = (
        select(func.count())
        .select_from(Visit)
        .where(Visit.v_date < func.to_date('2002-01-01', 'YYYY-MM-DD'))
    )
    return session.execute(stmt).scalar()

# Finds doctors (both internal and external) who have visited patient "David Hill".
def find_doctors_for_patient(session):
    stmt = (
        select(
            InternalDoctor.name.label('internal_name'),
            InternalDoctor.surname.label('internal_surname'),
            ExternalDoctor.name.label('external_name'),
            ExternalDoctor.surname.label('external_surname')
        )
        .select_from(Visit)
        .join(InternalDoctor, Visit.internal_doctor_id == InternalDoctor.id)
        .join(ExternalDoctor, Visit.external_doctor_id == ExternalDoctor.id)
        .join(Patient, Visit.patient_id == Patient.id)
        .where(
            func.lower(Patient.name) == 'david',
            func.lower(Patient.surname) == 'hill'
        )
        .distinct()
    )
    return session.execute(stmt).all()

# Finds the most frequent diagnosis in the reports.
def find_most_frequent_diagnosis(session):
    diagnosis_counts = (
        select(
            Report.diagnosis_id,
            func.count().label('count')
        )
        .group_by(Report.diagnosis_id)
        .subquery()
    )
    max_count_stmt = select(func.max(diagnosis_counts.c.count))
    max_count = session.execute(max_count_stmt).scalar()

    stmt = (
        select(
            Diagnosis.text.label('text'),
            func.count().label('occurrence_count')
        )
        .join(Report)
        .group_by(Diagnosis.text)
        .having(func.count() == max_count)
    )
    return session.execute(stmt).all()
#-----------------------------------------------------#
# Finds patients who have received a prescription from Dr. Rose Taylor.
def find_patient_from_doctor(session):
    stmt = (
        select(
            Patient.name.label('name'),
            Patient.surname.label('surname')
        )
        .join(Prescribe, Prescribe.patient_id == Patient.id)
        .join(InternalDoctor, InternalDoctor.id == Prescribe.doctor_id)
        .where(
            func.lower(InternalDoctor.name) == 'rose',
            func.lower(InternalDoctor.surname) == 'taylor'
        )
        .distinct()
    )

    return session.execute(stmt).all()


# Lists all prescriptions with details about patients, doctors, and drugs.
def list_all_prescriptions(session):
    stmt = (
        select(
            Prescribe.id.label('prescription_id'),
            Prescribe.presc_date,
            Patient.name.label('patient_name'),
            Patient.surname.label('patient_surname'),
            InternalDoctor.name.label('doctor_name'),
            InternalDoctor.surname.label('doctor_surname'),
            Drug.drug_name.label('drug_name'),
            Prescribe.quantity,
            Prescribe.dosage,
            Repeat.max_times.label('repeat_max_times'),
            Repeat.interval.label('repeat_interval')
        )
        .join(Patient, Prescribe.patient_id == Patient.id)
        .join(InternalDoctor, Prescribe.doctor_id == InternalDoctor.id)
        .join(Drug, Prescribe.drug_id == Drug.id)
        .join(Repeat, Prescribe.repeat_id == Repeat.id, isouter=True)
        .order_by(Prescribe.id)
    )
    return session.execute(stmt).all()

# Counts the number of prescriptions made by each internal doctor.
def find_doctors_prescriptions_count(session):
    stmt = (
        select(
            InternalDoctor.name.label('doctor_name'),
            InternalDoctor.surname.label('doctor_surname'),
            func.count(Prescribe.id).label('prescriptions_count')
        )
        .join(Prescribe, Prescribe.doctor_id == InternalDoctor.id)
        .group_by(InternalDoctor.name, InternalDoctor.surname)
        .order_by(func.count(Prescribe.id).desc())
    )
    return session.execute(stmt).all()

# Executes the SQL commands.
def execute_sql_file(engine, file_path):
    with open(file_path, 'r') as file:
        sql_commands = file.read()

    commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]

    with engine.connect() as connection:
        for command in commands:
            try:
                connection.execute(text(command))
                print(f"Executed: {command}")
            except Exception as e:
                print(f"Error executing SQL command: {command}\nError: {e}")

# Finds the ID of an internal doctor given the name and surname.
def find_doctor_id(session, doctor_name, doctor_surname):
    stmt = (
        select(InternalDoctor.id)
        .where(
            func.lower(InternalDoctor.name) == doctor_name.lower(),
            func.lower(InternalDoctor.surname) == doctor_surname.lower()
        )
    )

    return session.execute(stmt).scalar_one()

def test_sql_insert_time(session):
    prescription_data = Prescribe(
        id=1000,
        presc_date=datetime.now(),
        patient_id=1,
        doctor_id=1,
        quantity=10,
        direction="Take one tablet every 8 hours",
        dosage=500,
        drug_id=1,
        visit_id=1,
        repeat_id=None
    )

    start_time = time.time()

    session.add(prescription_data)
    session.commit()

    end_time = time.time()
    elapsed_time = (end_time - start_time)*1000

    print(f"Time to insert into SQLAlchemy (SQL): {elapsed_time} milliseconds")

    session.delete(prescription_data)
    session.commit()
    print("Inserted prescription has been deleted from SQL database.")


def find_oldest_prescription_sql(session):
    start_time = time.time()

    oldest_prescription = session.query(Prescribe).order_by(Prescribe.presc_date).first()

    if oldest_prescription:
        doctor_id = oldest_prescription.doctor_id
        patient_id = oldest_prescription.patient_id

        doctor = session.query(InternalDoctor).filter(InternalDoctor.id == doctor_id).first()
        patient = session.query(Patient).filter(Patient.id == patient_id).first()

        print(f"Oldest Prescription ID: {oldest_prescription.id}")
        print(f"Doctor ID: {doctor_id}, Patient ID: {patient.id}")
    else:
        print("No prescriptions found.")

    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    print(f"Time to execute queue into SQLAlchemy: {elapsed_time} milliseconds")