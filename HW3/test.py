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
    lag(salary, 1) over (order by salary desc) - salary as diff
    from employee
    where country='Germany';
	"""

def query2():
	#TODO: practice + window alias 
	return """
	select first_name, last_name, salary, country,
	rank() over (partition by country order by salary desc) as rank,
	ntile(4) over (partition by country order by salary desc) as quartile
	from employee
	where country='Germany' or country='United Kingdom';
	"""

def query3():
	#TODO: practice!!!
	return """
	select distinct age, gender,
	count(employee_id) over (partition by gender order by age)
	from employee
	where age >= 24 and age <= 30;
	"""
	
def query4():
	#TODO: pratice
	return """
	select first_name, last_name, age, gender, salary,
	rank() over (partition by gender order by salary desc) as rank1,
	rank() over (order by salary desc)
	from employee
	where age=24;
	"""

def query5():
	#TODO: pratice!!!
	return """
	select distinct department,
	avg(salary) over (partition by department) as average_salary,
	case
        when avg(salary) over (partition by department) >= 200000 then 'High'
		when avg(salary) over (partition by department) < 200000 and avg(salary) over (partition by department) >= 180000 then 'Medium'
		else 'Low'
	end as salary_bracket
	from employee;
	"""

def query6():
	return """
	select 
	sum(
	case 
        when security_clearance=1 then 1
		else 0
	end
    ) as low_clearance,
	sum(
	case
        when security_clearance=2 then 1
		else 0
	end
    ) as moderate_clearance,
	sum(
	case
        when security_clearance=3 then 1
		else 0
	end
    ) as high_clearance,
	sum(
	case
        when security_clearance=4 then 1
		else 0
	end
    ) as very_high_clearance,
	sum(
	case
        when security_clearance=5 then 1
		else 0
	end
    ) as top_secret_clearance
	from company_info;
	"""

def query7():
	#TODO:practice!!
	return """
	select 'Middle-aged' as 'Age Group', gender,
	count(employee_id) over (partition by gender) as 'Age Group'
	from employee
	where age >= 30 and age < 50
	union
	select 'Senior' as 'Age Group', gender,
	count(employee_id) over (partition by gender) as 'Age Group'
	from employee
	where age >= 50
	union
	select 'Young' as 'Age Group', gender,
	count(employee_id) over (partition by gender) as 'Age Group'
	from employee
	where age < 30;
	"""

def query8():
	return """
	select first_name, last_name, json_extract(employee.extra, '$.email') as email
	from employee
	where json_extract(employee.extra, '$.email') like "%@ftc.gov";
	"""

def query9():
	#TODO: practice
	return """
	with temp as (
	select count(value) as total
	from employee, json_each(json_extract(employee.extra, '$.tags'))
	group by employee_id
    )
	select avg(total) as avg_tags_per_employee from temp;
	"""

def query10():
	#TODO: practice
	return """
	with temp as (
	select employee_id
	from employee
	where json_extract(employee.extra, '$.cell_phone') is not null
	intersect
	select employee_id
	from employee
	where json_extract(employee.extra, '$.home_phone') is not null
    )
	select count(employee_id) as num_employee from temp;
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
