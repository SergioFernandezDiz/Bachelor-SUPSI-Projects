CREATE TABLE specialization (
id 				INTEGER,
name			VARCHAR2(50),
PRIMARY KEY (id)
);

CREATE TABLE internal_doctor (
id 			 	INTEGER,
name 			VARCHAR2(50),
surname 		VARCHAR2(50),
specialization 	INTEGER NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (specialization) REFERENCES specialization
);

CREATE TABLE external_doctor (
id 				INTEGER,
name 			VARCHAR2(50),
surname 		VARCHAR2(50),
street			VARCHAR2(50),
postcode		VARCHAR2(10),
city	 		VARCHAR2(50),
specialization	INTEGER NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (specialization) REFERENCES specialization
);

CREATE TABLE diagnosis (
code	 		INTEGER,
text 			VARCHAR2(100),
specialization	INTEGER NOT NULL,
PRIMARY KEY (code),
FOREIGN KEY (specialization) REFERENCES specialization
);

CREATE TABLE patient (
id				INTEGER,
name 			VARCHAR2(50),
surname 		VARCHAR2(50),
birthdate		DATE,
street			VARCHAR2(50),
postcode		VARCHAR2(10),
city	 		VARCHAR2(50),
PRIMARY KEY (id)
);
 
CREATE TABLE visit (
v_number 		INTEGER,
v_date			DATE,
internal_doctor INTEGER NOT NULL,
external_doctor INTEGER NOT NULL,
patient 		INTEGER NOT NULL,
PRIMARY KEY (v_number),
FOREIGN KEY (internal_doctor) REFERENCES internal_doctor,
FOREIGN KEY (external_doctor) REFERENCES external_doctor,
FOREIGN KEY (patient) REFERENCES patient
);



CREATE TABLE report (
visit 			INTEGER,
diagnosis 		INTEGER,
PRIMARY KEY (visit, diagnosis),
FOREIGN KEY (visit) REFERENCES visit,
FOREIGN KEY (diagnosis) REFERENCES diagnosis
);

CREATE TABLE drug (
    id              INTEGER PRIMARY KEY,
    drug_name            VARCHAR(100) NOT NULL,
    strength        INTEGER NOT NULL
);

CREATE TABLE repeat (
    id              INTEGER PRIMARY KEY,
    max_times       INTEGER NOT NULL,
    interval        INTEGER NOT NULL
);

CREATE TABLE prescribe (
    id              INTEGER PRIMARY KEY,
    presc_date      DATE NOT NULL,
    patient_id      INTEGER NOT NULL,
    doctor_id       INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    direction       VARCHAR(100),
    dosage          INTEGER NOT NULL,
    drug_id         INTEGER NOT NULL,
    visit_id        INTEGER,
    repeat_id       INTEGER,

    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES internal_doctor(id),
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (repeat_id) REFERENCES repeat(id),
    FOREIGN KEY (visit_id) REFERENCES visit(v_number)
);