# 1. Combine two tables

Table: Person

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| PersonId    | int     |
| FirstName   | varchar |
| LastName    | varchar |
+-------------+---------+
PersonId is the primary key column for this table.
Table: Address

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| AddressId   | int     |
| PersonId    | int     |
| City        | varchar |
| State       | varchar |
+-------------+---------+
AddressId is the primary key column for this table.

problem:
Write a SQL query for a report that provides the following information for
each person in the Person table, regardless if there is an address for each of
those people:

FirstName, LastName, City, State

solution:

Since the PersonId in table Address is the foreign key of table Person, we can join
this two table to get the address information of a person.

Considering there might not be an address information for every person, we should use
outer join instead of the default inner join.

select FirstName, LastName, City, State
from Person left join Address
on Person.PersonId = Address.PersonId

Different Types of SQL JOINs:

(INNER) JOIN: Returns records that have matching values in both tables

LEFT (OUTER) JOIN: Returns all records from the left table, and the
matched records from the right table

RIGHT (OUTER) JOIN: Returns all records from the right table, and the matched records from the left
table 

FULL (OUTER) JOIN: Returns all records when there is a match in
either left or right table

# 2. Second Highest Salary

Write a SQL query to get the second highest salary from the Employee table.

+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
For example, given the above Employee table, the query should return 200 as the second highest salary. If there is no second highest salary, then the query should return null.

+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+

solution:

using IFNULL and LIMIT clause

select
	IFNULL(
		select distinct Salary
		from Employee
		order by Salary DESC
		limit 1 OFFSET 1), 
	NULL) AS SecondHighestSalary










