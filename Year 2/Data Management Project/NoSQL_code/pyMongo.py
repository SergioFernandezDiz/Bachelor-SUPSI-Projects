from pymongo import MongoClient
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
from datetime import time as t
from medical_queries import *
import time


# Creates a connection to the collection in MongoDB.
def create_mongo_connection():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['medical_office']
    return db['prescribe']

# Clears all documents from the "prescribe" collection in MongoDB.
def clear_mongo_collection():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['medical_office']
    prescribe_collection = db['prescribe']
    prescribe_collection.delete_many({}) # Deletes all documents in the collection.
    print("All documents have been deleted from the 'prescribe' collection.")

# Migrates prescriptions from SQL database to MongoDB.
def migrate_prescriptions_to_mongodb(session: Session):

    prescribe_collection = create_mongo_connection()
    prescriptions = session.query(Prescribe).all() # Retrieve all prescriptions from SQL.

    for prescription in prescriptions:
        # Retrieve associated drug and repeat information from SQL.
        drug = session.query(Drug).filter(Drug.id == prescription.drug_id).first()
        repeat = session.query(Repeat).filter(Repeat.id == prescription.repeat_id).first() if prescription.repeat_id else None

        # Convert the prescription date (which is of type datetime.date) to datetime.datetime
        presc_date = datetime.combine(prescription.presc_date, t(0, 1))

        # Create the prescription data to be inserted into MongoDB.
        prescription_data = {
            "prescription_id": prescription.id,
            "presc_date": presc_date,
            "patient_id": prescription.patient_id,
            "doctor_id": prescription.doctor_id,
            "quantity": prescription.quantity,
            "direction": prescription.direction,
            "dosage": prescription.dosage,
            "drug": {
                "drug_name": drug.drug_name,
                "strength": drug.strength
            },
            "visit_id": prescription.visit_id
        }

        # Manage the 2 different prescriptions
        if repeat:
            prescription_data["repeat"] = {
                "max_times": repeat.max_times,
                "interval": repeat.interval
            }


        # Check if the prescription already exists in MongoDB by its prescription_id.
        existing_prescription = prescribe_collection.find_one({"prescription_id": prescription_data["prescription_id"]})
        if existing_prescription:

            # Remove the _id field from the existing document before comparison
            existing_prescription_copy = existing_prescription.copy()
            existing_prescription_copy.pop('_id', None)  # Remove the _id field

            # Update the document if there are any differences.
            if existing_prescription_copy != prescription_data:
                prescribe_collection.update_one(
                    {"prescription_id": prescription_data["prescription_id"]},
                    {"$set": prescription_data}
                )
                print(f"Updated prescription ID: {prescription_data['prescription_id']}")
            # if we don't have differences.
            else:
                print(f"Already inserted ID: {prescription_data['prescription_id']}")

        # Insert the new prescription
        else:
            prescribe_collection.insert_one(prescription_data)
            print(f"Inserted prescription ID: {prescription_data['prescription_id']}")

    return prescribe_collection

# Counts the number of prescriptions for each doctor in MongoDB.
def find_doctor_prescriptions_count(prescribe_collection, session: Session):

    pipeline = [
        {
            "$group": { # Group by doctor_id and count the number of prescriptions
                "_id": "$doctor_id",
                "prescriptions_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"prescriptions_count": -1} # Sort the result in descending order
        }
    ]

    results = list(prescribe_collection.aggregate(pipeline))
    # For each doctor retrive from SQL Database the name and Surname, finaly print results.
    for result in results:
        doctor_id = result['_id']
        prescriptions_count = result['prescriptions_count']

        doctor = session.query(InternalDoctor).filter(InternalDoctor.id == doctor_id).first()

        if doctor:
            print(f"Doctor: {doctor.name} {doctor.surname} (ID: {doctor_id}) -> {prescriptions_count} prescriptions")
        else:
            print(f"Doctor ID: {doctor_id} not found.")

# Finds patients who received prescriptions from Dr. Rose Taylor in MongoDB.
def find_patients_from_doctor_in_mongo(session,collection):


    doctor_id = find_doctor_id(session, 'rose', 'taylor')
    prescriptions = collection.find({"doctor_id": doctor_id})

    for prescription in prescriptions:
        patient_id = prescription.get("patient_id")
        patient = session.query(Patient).filter(Patient.id == patient_id).first()

        if patient:
            print(f"Patient: {patient.name} {patient.surname} (ID: {patient.id})")

def test_mongodb_insert_time(session: Session):
    prescribe_collection = create_mongo_connection()

    prescription_data = {
        "prescription_id": 999,
        "presc_date": datetime.now(),
        "patient_id": 1,
        "doctor_id": 1,
        "quantity": 10,
        "direction": "Take one tablet every 8 hours",
        "dosage": 500,
        "drug_id": 1,
        "visit_id": 1,
        "repeat_id": None
    }

    start_time = time.time()

    prescribe_collection.insert_one(prescription_data)

    end_time = time.time()
    elapsed_time = (end_time - start_time)*1000
    print(f"Time to insert into MongoDB: {elapsed_time} milliseconds")

    prescribe_collection.delete_one({"prescription_id": prescription_data["prescription_id"]})
    print("Inserted prescription has been deleted from MongoDB.")

def find_oldest_prescription(prescribe_collection):
    start_time = time.time()
    oldest_prescription = prescribe_collection.find_one(
        {},
        sort=[("presc_date", 1)]
    )

    doctor_id = oldest_prescription.get("doctor_id")
    patient_id = oldest_prescription.get("patient_id")
    print(f"Oldest Prescription ID: {oldest_prescription['prescription_id']}")
    print(f"Doctor ID: {doctor_id}, Patient ID: {patient_id}")
    end_time = time.time()
    elapsed_time = (end_time - start_time)*1000
    print(f"Time to execute queue into MongoDB: {elapsed_time} milliseconds")
