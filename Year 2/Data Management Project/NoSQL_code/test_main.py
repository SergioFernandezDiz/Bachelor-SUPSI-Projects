from pyMongo import *
import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import configparser
import os

# Creates a connection to the SQL database using credentials from the config file.
def create_connection():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)

    db_config = config['database']
    username = db_config['username']
    password = db_config['password']
    host = db_config['host']
    port = db_config['port']
    service_name = db_config['service_name']

    connection_string = f"oracle+oracledb://{username}:{password}@{host}:{port}/{service_name}"

    engine = create_engine(connection_string)

    return engine

# Main function to handle different actions based on user input.
def main(action):
    engine = create_connection() # Create connection to SQL database.
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create a session factory for SQLAlchemy.

    with SessionLocal() as session:  # Start a session with the engine.

        if action == 'info':
            # Print available commands and their descriptions when 'info' is chosen.
            print("Possible commands:")
            print("SQL_Database:\n\t1. db_drop: SQL script to drop the database\n\t2. db_create: SQL script to create the database\n\t3. db_insert: SQL script to insert data into the database")
            print("SQL_Alchemy:\n\t1. s_queue1: finds and prints internal doctors named Daniel\n\t2. s_queue2: counts and prints the number of visits before 2002\n\t3. s_queue3: finds and prints doctors who visited David Hill\n\t4. s_queue4: finds and prints the most frequent diagnosis\n\t5. s_queue5: lists all prescriptions with patient, doctor, and drug details\n\t6. s_queue6: List of doctors and their prescription count (sorted by most prescriptions)\n\t7. s_queue7: finds and prints patients who received prescriptions from Dr. Rose Taylor")
            print("MongoDB:\n\t1. clear: clears the MongoDB prescription collection\n\t2. update: migrates prescriptions from SQL to MongoDB\n\t3. m_queue1: List of doctors and their prescription count (sorted by most prescriptions)\n\t4. m_queue2: finds and prints patients who received prescriptions from Dr. Rose Taylor")
            print("Execution Time Test:\n\t1. t_insert: Test the execution time for inserting a new prescription\n\t2. t_queue: Test the execution time for performing a queue to retrieve the doctor_id and patient_id from the older prescription.")
        elif action == 'db_drop':
            # Drop the database by executing the SQL script in the file.
            execute_sql_file(engine, './db/medical_office_drop.sql')
        elif action == 'db_create':
            # Create the database by executing the SQL script in the file.
            execute_sql_file(engine, './db/medical_office_create.sql')
        elif action == 'db_insert':
            # Insert data into the database by executing the SQL script in the file.
            execute_sql_file(engine, './db/medical_office_insert.sql')
        elif action == 'update':
            # Migrate prescriptions from SQL to MongoDB.
            migrate_prescriptions_to_mongodb(session)
        elif action == 'clear':
            # Clear the MongoDB 'prescribe' collection.
            clear_mongo_collection()
            print("Action: Clear completed. MongoDB collection has been cleared.")
        elif action == 'm_queue1':
            # Find doctors and their prescription counts in MongoDB, sorted by most prescriptions.
            print("\nList of doctors and their prescription count (sorted by most prescriptions):")
            prescribe_collection = create_mongo_connection()  # Connect to MongoDB.
            find_doctor_prescriptions_count(prescribe_collection, session)  # Perform the query.
        elif action == 'm_queue2':
            # Find patients who received prescriptions from Dr. Rose Taylor in MongoDB.
            print("\nPatient who received a prescription from the doctor Rose Taylor:")
            prescribe_collection = create_mongo_connection()  # Connect to MongoDB.
            find_patients_from_doctor_in_mongo(session, prescribe_collection)  # Perform the query.
        elif action == 's_queue1':
            # Find and print internal doctors named Daniel.
            print("\n1. Internal doctors named Daniel:")
            daniel_doctors = find_daniel_doctors(session)  # Query SQLAlchemy for doctors named Daniel.
            for doc in daniel_doctors:
                print(f"ID: {doc.id}, Name: {doc.name}, Surname: {doc.surname}")
        elif action == 's_queue2':
            # Count and print the number of visits before 2002.
            print("\n2. Number of visits before 2002:")
            old_visits = count_old_visits(session)  # Query SQLAlchemy for the visit count.
            print(f"Total visits: {old_visits}")
        elif action == 's_queue3':
            # Find and print doctors who visited patient "David Hill".
            print("\n3. Doctors who visited David Hill:")
            doctors = find_doctors_for_patient(session)  # Query SQLAlchemy for doctors.
            for doc in doctors:
                print(f"Internal doctor: {doc.internal_name} {doc.internal_surname}")
                print(f"External doctor: {doc.external_name} {doc.external_surname}")
        elif action == 's_queue4':
            # Find and print the most frequent diagnosis.
            print("\n4. Most frequent diagnosis:")
            diagnoses = find_most_frequent_diagnosis(session)  # Query SQLAlchemy for the frequent diagnosis.
            for diag in diagnoses:
                print(f"Diagnosis: {diag.text}, Occurrences: {diag.occurrence_count}")
        elif action == 's_queue5':
            # List all prescriptions with patient, doctor, and drug details.
            print("\n5. List all prescriptions with patient, doctor, and drug details:")
            prescriptions = list_all_prescriptions(session)  # Query SQLAlchemy for prescriptions.
            for prescription in prescriptions:
                print(f"Prescription ID: {prescription.prescription_id}, Date: {prescription.presc_date}, "
                      f"Patient: {prescription.patient_name} {prescription.patient_surname}, "
                      f"Doctor: {prescription.doctor_name} {prescription.doctor_surname}, "
                      f"Drug: {prescription.drug_name}, Quantity: {prescription.quantity}, "
                      f"Dosage: {prescription.dosage}, Repeat Max Times: {prescription.repeat_max_times}, "
                      f"Repeat Interval: {prescription.repeat_interval}")
        elif action == 's_queue6':
            # List doctors and their prescription count, sorted by most prescriptions.
            print("\n6. List of doctors and their prescription count (sorted by most prescriptions):")
            doctors_prescriptions = find_doctors_prescriptions_count(
                session)  # Query SQLAlchemy for doctors' prescriptions count.
            for doc in doctors_prescriptions:
                print(
                    f"Doctor: {doc.doctor_name} {doc.doctor_surname}, Number of prescriptions: {doc.prescriptions_count}")
        elif action == 's_queue7':
            # Find patients who received a prescription from Dr. Rose Taylor.
            print("\n7. Patient who received a prescription from the doctor Rose Taylor:")
            patient = find_patient_from_doctor(session)  # Query SQLAlchemy for patients of Dr. Rose Taylor.
            for p in patient:
                print(f"Name: {p.name}, Surname: {p.surname}")
        elif action == 't_insert':
            print("Testing MongoDB insert time...")
            test_mongodb_insert_time(session)
            print("\nTesting SQL_Alchemy insert time...")
            test_sql_insert_time(session)
        elif action == 't_queue':
            print("Testing MongoDB queue time...")
            prescribe_collection = create_mongo_connection()
            find_oldest_prescription(prescribe_collection)
            print("\nTesting SQL_Alchemy queue time...")
            find_oldest_prescription_sql(session)

        else:
            print("Invalid action.")  # Handle invalid actions.

if __name__ == "__main__":
    print("----------------------------------------------------------")
    parser = argparse.ArgumentParser(description="Choose an operation")
    parser.add_argument('action', choices=['update', 'clear', 'm_queue1', 'info','s_queue1','s_queue2','s_queue3','s_queue4','s_queue5','s_queue6','s_queue7','db_create','db_insert','db_drop','m_queue2','t_insert','t_queue'],
                        help="Action to perform: 'migrate', 'clear', 'queue1', 'queue2'")
    args = parser.parse_args()
    main(args.action)
    print("----------------------------------------------------------")

