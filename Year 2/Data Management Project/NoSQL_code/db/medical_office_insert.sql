insert into specialization values (1,  'neurology');
insert into specialization values (2,  'cardiology');
insert into specialization values (3,  'orthopedics');
insert into specialization values (4,  'otolaryngology');
insert into specialization values (5,  'pediatrics');
insert into specialization values (6,  'geriatrics');
insert into specialization values (7,  'psychology');
insert into specialization values (8,  'psychiatry');
insert into specialization values (9,  'dermatology');
insert into specialization values (10, 'everylogy');

insert into internal_doctor values (1,  'john',  	'smith',   	1);
insert into internal_doctor values (2,  'daniel',  'johnson', 	2);
insert into internal_doctor values (3,  'elizabeth','moore',	3);
insert into internal_doctor values (4,  'rose',   	'taylor',   4);
insert into internal_doctor values (5,  'anthony',  'white',    5);
insert into internal_doctor values (6,  'daniel',   'jackson',  6);
insert into internal_doctor values (7,  'anna',   	'wilson',   7);
insert into internal_doctor values (8,  'emily',   	'martinez', 8);
insert into internal_doctor values (9,  'michael',  'clark',    9);
insert into internal_doctor values (10, 'megan', 	'harris',  10);

insert into external_doctor values (1,  'robert',  	'lee',     'high street',     'e15 1az',  'london',    	 1);
insert into external_doctor values (2,  'albert',  	'brown',   'station road',    'dn2 6ln',  'doncaster', 	 2);
insert into external_doctor values (3,  'ethan',    'roberts', 'main street',     'ls3 1aa',  'leeds',  	 3);
insert into external_doctor values (4,  'liam',    	'martin',  'victoria road',   'ec4y 0be', 'london',    	 4);
insert into external_doctor values (5,  'jopshua',  'green',   'church road',     'ls10 2ag', 'hunslet',  	 5);
insert into external_doctor values (6,  'james',  	'hughes',  'george road',	  'sw1v 3jd', 'london',   	 6);
insert into external_doctor values (7,  'joe', 		'clarke',  'grove road',      'so40 0bb', 'southampton', 7);
insert into external_doctor values (8,  'linda',  	'turner',  'mill road',       'so40 0ef', 'southampton', 8);
insert into external_doctor values (9,  'abigail', 	'watson',  'albert road',     'dn9 1lp',  'doncaster', 	 9);
insert into external_doctor values (10, 'samantha', 'scott',   'manchester road', 'dn34 4bt', 'doncaster',  10);
insert into external_doctor values (11, 'charlotte','hall',    'broadway',  	  'sw1y 4ha', 'london',     10);

insert into patient values (1, 'david',  'hill',     to_date('01.01.1920', 'dd.mm.yyyy'), 'richmond road',  'ec4y 0ay', 'london');
insert into patient values (2, 'paul',   'scott',    to_date('10.02.1925', 'dd.mm.yyyy'), 'mill road',   	'ec4y 0dq', 'london');
insert into patient values (3, 'susan',  'king',     to_date('15.03.1930', 'dd.mm.yyyy'), 'south street',   'e4 0bs', 	'london');
insert into patient values (4, 'sarah',  'watson',   to_date('20.04.1945', 'dd.mm.yyyy'), 'north street',   'e4 0ee', 	'london');
insert into patient values (5, 'peter',  'clarke',   to_date('30.05.1951', 'dd.mm.yyyy'), 'est street',    	'l37 0aw', 	'liverpool');
insert into patient values (6, 'robert', 'white',    to_date('02.06.1965', 'dd.mm.yyyy'), 'west street', 	'l29 1ya', 	'liverpool');
insert into patient values (7, 'mary', 	 'bell',     to_date('22.07.1970', 'dd.mm.yyyy'), 'queen street',   'eh19 2ej', 'edinburgh');
insert into patient values (8, 'nala',  'campbell', to_date('01.09.1903', 'dd.mm.yyyy'), 'park lane', 		'eh52 5dl', 'edinburgh');
insert into patient values (9, 'john',   'cook',     to_date('11.09.1980', 'dd.mm.yyyy'), 'george street',  'sn6 6dd', 	'swindon');

insert into visit values (1,  to_date('02.01.2002', 'dd.mm.yyyy'), 1,  1,  1);
insert into visit values (2,  to_date('02.01.2003', 'dd.mm.yyyy'), 1,  1,  1);
insert into visit values (3,  to_date('01.01.2003', 'dd.mm.yyyy'), 1,  1,  8);
insert into visit values (4,  to_date('01.02.2002', 'dd.mm.yyyy'), 2,  9,  3);
insert into visit values (5,  to_date('01.09.2002', 'dd.mm.yyyy'), 2,  9,  3);
insert into visit values (6,  to_date('10.03.2002', 'dd.mm.yyyy'), 9,  3,  4);
insert into visit values (7,  to_date('20.04.2002', 'dd.mm.yyyy'), 4,  10, 5);
insert into visit values (8,  to_date('05.06.2002', 'dd.mm.yyyy'), 10, 8,  6);
insert into visit values (9,  to_date('05.02.2002', 'dd.mm.yyyy'), 10, 8,  6);
insert into visit values (10, to_date('05.12.2002', 'dd.mm.yyyy'), 10, 8,  6);
insert into visit values (11, to_date('02.08.1975', 'dd.mm.yyyy'), 5,  5,  7);
insert into visit values (12, to_date('10.09.2000', 'dd.mm.yyyy'), 7,  10, 7);
insert into visit values (13, to_date('10.09.2001', 'dd.mm.yyyy'), 7,  10, 7);
insert into visit values (14, to_date('10.09.2002', 'dd.mm.yyyy'), 7,  10, 7);
insert into visit values (15, to_date('01.08.2002', 'dd.mm.yyyy'), 6,  11, 8);
insert into visit values (16, to_date('02.01.2003', 'dd.mm.yyyy'), 7,  10, 7);
insert into visit values (17, to_date('02.01.2003', 'dd.mm.yyyy'), 9,  6,  9);
insert into visit values (18, to_date('09.01.2003', 'dd.mm.yyyy'), 9,  6,  9);
insert into visit values (19, to_date('16.01.2003', 'dd.mm.yyyy'), 9,  6,  9);
insert into visit values (20, to_date('02.01.2003', 'dd.mm.yyyy'), 4,  1,  2);

insert into diagnosis values (1,  'schizophrenia', 8);
insert into diagnosis values (2,  'depression', 8);
insert into diagnosis values (3,  'acne', 9);
insert into diagnosis values (4,  'alzheimer', 1);
insert into diagnosis values (5,  'legionella', 10);
insert into diagnosis values (6,  'occlusion of the aorta', 2);
insert into diagnosis values (7,  'ventricular dysfunction', 2);
insert into diagnosis values (8,  'external otitis', 4);
insert into diagnosis values (9,  'otitis media', 4);
insert into diagnosis values (10, 'laryngitis', 4);
insert into diagnosis values (11, 'pharyngitis', 4);
insert into diagnosis values (12, 'parkinson', 1);
insert into diagnosis values (13, 'alopecia', 9);
insert into diagnosis values (14, 'myocardial infarction', 2);
insert into diagnosis values (15, 'hypertension', 1);
insert into diagnosis values (16, 'bronchitis', 10);
insert into diagnosis values (17, 'pneumonia', 10);
insert into diagnosis values (18, 'tibia fracture', 3);
insert into diagnosis values (19, 'fibula fracture', 3);
insert into diagnosis values (20, 'torn left knee cruciate ligament', 3);
insert into diagnosis values (21, 'torn right knee cruciate ligament', 3);
insert into diagnosis values (22, 'stress from too much study', 7);
insert into diagnosis values (23, 'stress from too little study', 7);
insert into diagnosis values (24, 'stress from test', 7);
insert into diagnosis values (25, 'stress from exam', 7);

insert into report values (1,  4);
insert into report values (2,  4);
insert into report values (3,  12);
insert into report values (3,  2);
insert into report values (4,  6);
insert into report values (5,  14);
insert into report values (6,  13);
insert into report values (7,  9);
insert into report values (8,  1);
insert into report values (9,  2);
insert into report values (10, 15);
insert into report values (11, 16);
insert into report values (11, 8);
insert into report values (12, 22);
insert into report values (12, 24);
insert into report values (13, 23);
insert into report values (13, 24);
insert into report values (14, 22);
insert into report values (14, 25);
insert into report values (15, 12);
insert into report values (16, 1);
insert into report values (17, 3);
insert into report values (18, 3);
insert into report values (19, 3);
insert into report values (20, 9);
insert into report values (20, 10);

-- Insert drugs
INSERT INTO drug VALUES (1, 'Paracetamol', 500);
INSERT INTO drug VALUES (2, 'Ibuprofen', 200);
INSERT INTO drug VALUES (3, 'Aspirin', 100);
INSERT INTO drug VALUES (4, 'Amoxicillin', 250);
INSERT INTO drug VALUES (5, 'Cetirizine', 10);
INSERT INTO drug VALUES (6, 'Amoxicillin', 500);
INSERT INTO drug VALUES (7, 'Lorazepam', 1);
INSERT INTO drug VALUES (8, 'Metformin', 500);
INSERT INTO drug VALUES (9, 'Ibuprofen', 400);
INSERT INTO drug VALUES (10, 'Amlodipine', 5);
INSERT INTO drug VALUES (11, 'Paracetamol', 1000);
INSERT INTO drug VALUES (12, 'Atorvastatin', 10);

-- Insert repeat
INSERT INTO repeat VALUES (1, 5, 5);
INSERT INTO repeat VALUES (2, 3, 2);
INSERT INTO repeat VALUES (3, 10, 1);
INSERT INTO repeat VALUES (4, 2, 2);
INSERT INTO repeat VALUES (5, 4, 4);
INSERT INTO repeat VALUES (6, 2, 11);
INSERT INTO repeat VALUES (7, 7, 2);

-- Insert a non-repeatable prescription
INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (1, TO_DATE('2024-10-24', 'YYYY-MM-DD'), 1, 10, 30, 'Take one tablet every 8 hours', 500, 1, NULL, 1);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (2, TO_DATE('2022-11-25', 'YYYY-MM-DD'), 5, 5, 30, 'Take one tablet every 8 hours', 10, 5, NULL, 5);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (3, TO_DATE('2004-3-12', 'YYYY-MM-DD'), 6, 4, 40, 'Take one tablet every 12 hours', 500, 6, NULL, 6);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (4, TO_DATE('2017-04-11', 'YYYY-MM-DD'), 7, 7, 20, 'Take one tablet every 6 hours', 1, 7, NULL, 7);

-- Insert a repeatable prescription
INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (8, TO_DATE('2024-12-26', 'YYYY-MM-DD'), 8, 8, 60, 'Take one tablet every 8 hours', 500, 8, 1, 8);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (9, TO_DATE('2024-12-27', 'YYYY-MM-DD'), 8, 9, 40, 'Take one tablet every 12 hours', 400, 9, 2, 9);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (10, TO_DATE('2024-12-27', 'YYYY-MM-DD'), 1, 4, 30, 'Take one tablet every 6 hours', 1000, 10, 3, 10);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (11, TO_DATE('2024-12-28', 'YYYY-MM-DD'), 4, 4, 50, 'Take one tablet every 4 hours', 10, 11, 4, 11);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (12, TO_DATE('2024-12-28', 'YYYY-MM-DD'), 1, 7, 30, 'Take one tablet every 6 hours', 5, 7, 5, 12);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (13, TO_DATE('2024-11-29', 'YYYY-MM-DD'), 7, 8, 100, 'Take one tablet every day', 100, 7, 6, 13);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (14, TO_DATE('2000-12-29', 'YYYY-MM-DD'), 4, 2, 60, 'Take one tablet every 12 hours', 10, 1, 7, 14);

INSERT INTO prescribe (id, presc_date, patient_id, doctor_id, quantity, direction, dosage, drug_id, repeat_id, visit_id)
VALUES (16, TO_DATE('2024-12-29', 'YYYY-MM-DD'), 4, 4, 60, 'Take one tablet every 12 hours', 10, 1, 7, 14);


commit;