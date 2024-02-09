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
	return """
    select DISTINCT FirstName, LastName, max(Temperature) as Temperature
	from Patients natural join Appointments natural join Vitals;
	"""

def query2():
	# TODO: substring(string, start, number)
	return """
	select FirstName, LastName, max(Temperature) as Temperature, substring(DateTime, 1, 10) as date
	from Patients natural join Appointments natural join Vitals
	group by substring(DateTime, 1, 10);
	"""

def query3():
	# TODO: limit()
	return """
	select City, avg(Temperature) as avg_temp, count(Temperature) as temp_count
	from Patients natural join Appointments natural join Vitals
	group by City
	limit 1;
	"""
	
def query4():
	#TODO: first one is incorrect if there are more than one maximum age then limit 2 is not true
	'''
	return """
	select PatientID, FirstName, LastName, Age, StreetAddress, City, ZipCode
	from Patients
	where Age in (select Age from Patients order by Age DESC limit 2);
	"""
	'''
	return """
	select PatientID, FirstName, LastName, Age, StreetAddress, City, ZipCode
	from Patients
	where Age in (
	select max(Age)
	from Patients
	union
	select max(Age)
	from Patients
	where Age < (select max(Age) from Patients)
	);
	"""

def query5():
	# TODO
	'''
	return """
	#incorrect
	select PatientID, FirstName, LastName, max(Age) as Age, StreetAddress, City, ZipCode
	from Patients 
	group by City
	order by PatientID;
	"""
	'''
	return """
	select PatientID, FirstName, LastName, Age, StreetAddress, City, ZipCode
	from Patients P
	where Age = (select max(Age) from Patients where P.City = Patients.City);
	"""

def query6():
	# TODO
	return """
	with temp as(select ID, count(AppointmentID) as prescription_count
	from Drugs left outer join Prescriptions on Drugs.ID = Prescriptions.DrugID
   	group by ID)
	select ID, Name, prescription_count,
	case
		when prescription_count = (select max(prescription_count) from temp) then 'highest prescribed drug'
		when prescription_count = (select min(prescription_count) from temp) then 'lowest prescribed drug'
		else 'between'
	end as description
	from Drugs natural join temp
	where description != 'between';
	"""

def query7():
	# TODO
	return """
	select P.FirstName || ' ' || P.LastName as PatientName, D.FirstName || ' ' || D.LastName as DoctorName, DateTime as vital_time, Temperature, (select avg(Temperature) from Vitals) as avg_temp
	from Patients P natural join Appointments natural join Vitals join Doctors D on D.DoctorID = Appointments.DoctorID;
	"""

def query8():
	return """
	select P.FirstName || ' ' || P.LastName as PatientName, D.FirstName || ' ' || D.LastName as DoctorName, DateTime as vital_time, Temperature, (select max(Temperature) from Vitals natural join Appointments where Appointments.PatientID = P.PatientID) as patient_high
	from Patients P natural join Appointments A
	natural join Vitals
	join Doctors D on D.DoctorID = A.DoctorID;
	"""

def query9():
	# TODO: string can do comparison
	return """
	with temp as(
		select Specialty as specialty, count(DoctorID) as doctor_count
		from Doctors
		group by Specialty
	)
	select T1.specialty, T1.doctor_count, T2.specialty, T2.doctor_count
	from temp T1 join temp T2
	on T1.doctor_count = T2.doctor_count and T1.specialty < T2.specialty;
	"""

def query10():
	# TODO: if there is no group by, it will be incorrect.
	'''
	return """
	select A.City, (select 
	case
		when count(DoctorID) != 0 then count(DoctorID)
		else NULL  
		end
		from Doctors where A.City=Doctors.City) as doctor_count,	
	(select 
	case
		when count(PatientID) != 0 then count(PatientID)
		else NULL
		end
		from Patients where A.City=Patients.City) as patient_count,
	(select
	case 
		when count(AppointmentID) != 0 then count(AppointmentID)
		else NULL
		end
		from Appointments natural join Patients join Doctors on Doctors.DoctorID = Appointments.DoctorID where A.City = Doctors.City AND A.City = Patients.City) as appointment_count
	from (select City from Patients union select City from Doctors) as A;
	"""
	'''
	return """
	select A.City,
	(select 
	case
		when count(DoctorID) != 0 then count(DoctorID)
		else NULL  
	end
	from Doctors where A.City=Doctors.City group by Doctors.City) as doctor_count,	
	(select 
	case
		when count(PatientID) != 0 then count(PatientID)
		else NULL
	end
	from Patients where A.City=Patients.City group by Patients.City) as patient_count,
	(select
	case 
		when count(AppointmentID) != 0 then count(AppointmentID)
		else NULL
	end
	from Appointments natural join Patients join Doctors on Doctors.DoctorID = Appointments.DoctorID where A.City = Doctors.City AND A.City = Patients.City group by Doctors.City) as appointment_count
	from (select City from Patients union select City from Doctors) as A;
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
   