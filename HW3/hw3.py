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
	#TODO: practice
	return """
    select first_name, last_name, salary,
	lag(salary, 1) over (partition by country = 'Germany' order by salary DESC) - salary as diff
	from employee
	where country = 'Germany'
	order by salary DESC;
	"""

def query2():
	#TODO: practice + window alias 
	return """
	select first_name, last_name, salary, country,
	rank() over (partition by country order by country, salary desc) as rank,
	ntile(4) over (partition by country order by country, salary desc) as quartile
	from employee
	where country = 'Germany' or country = 'United Kingdom'
	order by country, salary desc
	"""

def query3():
	#TODO: practice!!!
	return """
	with temp as(
	select count(employee_id) as cnt, age, gender
	from employee
	where age >= 24 and age <= 30
	group by gender, age
	)
	select age, gender,
	sum(cnt) over (partition by gender order by age) as employee_num
	from temp;
	"""
	
def query4():
	#TODO: pratice
	return """
	select first_name, last_name, age, gender, salary,
	rank() over (partition by gender order by salary desc) as rank1,
	rank() over (order by salary desc) as rank2
	from employee
	where age=24;
	"""

def query5():
	#TODO: pratice
	return """
	with temp as (
	select department, 
	avg(salary) over (partition by department) as avg_salary
	from employee
	)
	select distinct temp.department, 
	avg_salary,
	case
	when avg_salary >= 200000 then 'High'
	when avg_salary < 200000 and avg_salary >= 180000 then 'Medium'
	else 'Low'
	end as salary_bracket
	from employee natural join temp
	order by department;
	"""

def query6():
	return """
	select 
	sum(
	case
		when security_clearance = 1 then 1
		else 0
		end
	) as low_clearance,
	sum(
	case
		when security_clearance = 2 then 1
		else 0
		end
	) as moderate_clearance,
	sum(
	case
		when security_clearance = 3 then 1
		else 0
		end
	) as high_clearance,
	sum(
	case
		when security_clearance = 4 then 1
		else 0
		end
	) as very_high_clearance,
	sum(
	case
		when security_clearance = 5 then 1
		else 0
		end
	) as top_secret_clearance
	from company_info;
	"""

def query7():
	#TODO:practice!!
	return """
	with temp as (
	select employee_id,
	case
		when age < 30 then 'Young'
		when age >= 30 and age < 50 then 'Middle-aged'
		else 'Senior'
	end as age_group
	from employee
	)
	select distinct age_group as 'Age Group', Gender, 
	count(employee_id) over (partition by age_group, gender) as 'Num Employees'
	from employee natural join temp;
	"""

def query8():
	return """
	select first_name, last_name,
	json_extract(employee.extra, '$.email') as email
	from employee
	where json_extract(employee.extra, '$.email') like "%@ftc.gov";
	"""

def query9():
	#TODO: practice
	return """
	with temp as (
	select distinct employee_id, count(value) over (partition by employee_id) as total
	from employee, json_each(json_extract(extra, '$.tags'))
	)
	select avg(total) as avg_tags_per_employee
	from temp;
	"""

def query10():
	#TODO: practice
	return """
	select count(*) as num_employees
	from employee
	where json_extract(employee.extra, '$.cell_phone') is not null
	and json_extract(employee.extra, '$.home_phone') is not null;
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
