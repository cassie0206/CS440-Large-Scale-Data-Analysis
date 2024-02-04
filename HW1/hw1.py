import sys

# Use this file to write your queries. Submit this file in Brightspace after finishing your homework.

#TODO: Write your username and answer to each query as a string in the return statements in the functions below. 
# Do not change the function names. 

#Your resulting tables should have the attributes in the same order as appeared in the sample answers. 

#Make sure to test that python prints out the strings (your username and SQL queries) correctly.

#usage: python hw1.py or python3 hw1.py
# make sure the program prints out your SQL statements correctly. That means the autograder will read you SQL correctly. Running the Python file will not execute your SQL statements (just prints them).

def username():
	return "chan1000"
    
def query1():
	'''
	return """
    SELECT Patients.FirstName || ' ' || Patients.LastName AS PatientName, Doctors.FirstName || ' ' || Doctors.LastName AS DoctorName, Vitals.DateTime AS vital_time, Vitals.Temperature, Drugs.Name AS drug_name, Prescriptions.Dosage  
    FROM Appointments NATURAL JOIN Vitals NATURAL JOIN Prescriptions JOIN Drugs ON Prescriptions.DrugID = Drugs.ID NATURAL JOIN Patients JOIN Doctors ON Appointments.DoctorID = Doctors.DoctorID;
	"""
	'''
	return """
	SELECT PatientName, DoctorName, vital_time, Temperature, drug_name, Dosage
	FROM
	(SELECT FirstName || ' ' || LastName AS PatientName, PatientID FROM Patients)
	NATURAL JOIN
	(SELECT FirstName || ' ' || LastName AS DoctorName, DoctorID FROM Doctors)
	NATURAL JOIN
	Appointments
	NATURAL JOIN
	(SELECT AppointmentID, DateTime AS vital_time, Temperature FROM Vitals)
	NATURAL JOIN
	Prescriptions
	NATURAL JOIN
	(SELECT ID AS DrugID, Name AS drug_name FROM Drugs);
	"""

def query2():
	#TODO: Practice again
	return """	
	SELECT Patients.FirstName || ' ' || Patients.LastName AS PatientName, Doctors.FirstName || ' ' || Doctors.LastName AS DoctorName, Vitals.DateTime AS vital_time, Vitals.Temperature, Drugs.Name AS drug_name, Prescriptions.Dosage  
    FROM Appointments A 
	RIGHT OUTER JOIN Patients ON A.PatientID = Patients.PatientID
	FULL OUTER JOIN Doctors ON A.DoctorID = Doctors.DoctorID
	LEFT OUTER JOIN Prescriptions ON Prescriptions.AppointmentID = A.AppointmentID
	FULL OUTER JOIN Drugs ON Prescriptions.DrugID = Drugs.ID
	LEFT OUTER JOIN Vitals ON Vitals.AppointmentID = A.AppointmentID;
	"""

def query3():
	return """
	SELECT Patients.FirstName || ' ' || Patients.LastName AS PatientName, Doctors.FirstName || ' ' || Doctors.LastName AS DoctorName, Vitals.DateTime AS vital_time, Vitals.Temperature, Drugs.Name AS drug_name, Prescriptions.Dosage
	FROM Patients
	LEFT OUTER JOIN Appointments ON Appointments.PatientID = Patients.PatientID
	LEFT OUTER JOIN Doctors ON Appointments.DoctorID = Doctors.DoctorID
	LEFT OUTER JOIN Prescriptions ON Prescriptions.AppointmentID = Appointments.AppointmentID
	LEFT OUTER JOIN Vitals ON Vitals.AppointmentID = Appointments.AppointmentID
	LEFT OUTER JOIN Drugs ON Prescriptions.DrugID = Drugs.ID;
	"""
	
def query4():
	return """
	SELECT P1.FirstName || ' ' || P1.LastName AS Patient1, P2.FirstName || ' ' || P2.LastName AS Patient2, P1.City
	FROM Patients P1 JOIN Patients P2 ON P1.City = P2.City AND P1.PatientID < P2.PatientID;
	"""

def query5():
	return """
	SELECT P.FirstName || ' ' || P.LastName AS Patient, D.FirstName || ' ' || D.LastName AS Doctor, P.Age, A.AppointmentDateTime
	FROM Appointments A NATURAL JOIN Patients P
	JOIN Doctors D ON A.DoctorID = D.DoctorID
	WHERE P.Age = D.Age;
	"""

def query6():
	#TODO
	'''
	return """
	select City, ZipCode 
	from Patients
	where City not in (select City from Doctors);
	"""
	'''
	return """
	select City, Zipcode
	from Patients
	except
	select City, ZipCode
	from Doctors;
	"""

def query7():
	return """
	select 'diagonsis is Healthy' AS appointment_type, count(AppointmentID) as appointments_count 
	from Appointments A
	where A.Diagnosis = "Healthy"
	union all
	select 'reason is Checkup' as appointment_type, count(AppointmentID) as appointments_count
	from Appointments A
	where A.Reason like '%Checkup%';
	"""

def query8():
	return """
	select P.FirstName || ' ' || P.LastName as PatientName, avg(V.Temperature) as avg_temp, count(V.RecordID) as temp_count
	from Appointments A natural join Patients P NATURAL JOIN Vitals V
	where P.City = 'Springfield'
	group by P.PatientID
	having temp_count >= 2;
	"""

def query9():
	return """
	select A.AppointmentID, P.FirstName || ' ' || P.LastName as PatientName, D.FirstName || ' ' || D.LastName as DoctorName
	from Appointments A NATURAL JOIN Prescriptions P NATURAL JOIN Patients P
	JOIN Doctors D on D.DoctorID = A.DoctorID
	JOIN Drugs on Drugs.ID = P.DrugID
	where Drugs.Name = 'Ibuprofen'
	intersect
	select A.AppointmentID, P.FirstName || ' ' || P.LastName as PatientName, D.FirstName || ' ' || D.LastName as DoctorName
	from Appointments A NATURAL JOIN Prescriptions P NATURAL JOIN Patients P
	JOIN Doctors D on D.DoctorID = A.DoctorID
	JOIN Drugs on Drugs.ID = P.DrugID
	where Drugs.Name = 'Amoxicillin';
	"""

def query10():
	return """
	select D.specialty, count(distinct D.DoctorID) as number_doctors, count(distinct A.AppointmentID) as number_patients, count(Prescriptions.DrugID)
	from Doctors D left outer join Appointments A on D.DoctorID = A.DoctorID 
	left outer join Prescriptions on A.AppointmentID = Prescriptions.AppointmentID
	group by D.Specialty;
	"""

#Do not edit below

def main():
	query_options = {1: query1(), 2: query2(), 3: query3(), 4: query4(), 5: query5(), 6: query6(), 7: query7(), 8: query8(), 
		9: query9(), 10: query10()}
	
	if len(sys.argv) == 1:
		if username() == "username":
			print("Make sure to change the username function to return your username.")
			return
		else:
			print(username())
		for query in query_options.values():
			print(query)
	elif len(sys.argv) == 2:
		if sys.argv[1] == "username":
			print(username())
		else:
			print(query_options[int(sys.argv[1])])

	
if __name__ == "__main__":
   main()

