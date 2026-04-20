-- Customer Churn Analysis SQL Project
-- Dataset: Telco Customer Churn
-- Objective: Analyze customer behavior and identify churn patterns

#Creating Database.
Create database  churn_db;
use churn_db;

#Creating Table and importing dataset in the table.
Create table customers(
customerID varchar(20) primary key,
gender varchar(10),
SeniorCitizen int,
Partner varchar(5),
Dependents varchar(5),
tenure int,
PhoneService varchar(5),
MultipleLines varchar(30),
InternetService varchar(30),
OnlineSecurity varchar(30),
OnlineBackup varchar(30),
DeviceProtection varchar(30),
TechSupport varchar(30),
StreamingTV varchar(30),
StreamingMovies varchar(30),
Contract varchar(30),
PaperlessBilling varchar(5),
PaymentMethod varchar(50),
MonthlyCharges float,
TotalCharges varchar(50),
Churn varchar(5));

#Checking wether the dataset is properly imported or not meaning all the 7043 rows have been imported or not.
select count(*) from customers;

#Questions.
#Q What is the churn rate of customers?
select Churn,count(*) as customers,
round(count(*) * 100.0 /(select 
count(*)from customers) ,2) as percentage
from customers
group by Churn;
#Approximately 26.5% of customers have churned, indicating a significant retention issue.

#Q.How many customers have churn by contract?
select Contract,Churn,count(*)
from customers
group by Contract,Churn
order by contract,Churn;
#Customers with month-to-month contracts show the highest churn rate.

#Q.How many customers have churn by tenure group?
select case 
when tenure<12 then"0-12 Months"
when tenure between 12 and 24 then "12-24 Months"
when tenure between 25 and 48 then "25-48 Months"
else "48+ Months"
end as tenure_group
,Churn,count(*)
from customers
group by tenure_group,Churn
order by case when tenure_group = "0-12 Months"then 1
when tenure_group = "12-24 Months"then 2
when tenure_group = "25-48 Months"then 3
when tenure_group = "48+ Months" then 4
end,Churn;
#Customers with lower tenure (especially<12 months) are more likely to churn.

#Q.How many customers have churn by payment method?
select PaymentMethod,Churn,Count(*)
from customers
group by PaymentMethod,Churn
order by PaymentMethod,Churn;
#Customers using electronic check payment methods have higher churn rates.

#Q.What is the average spending of churn vs non-churn customers?
select Churn,Round(Avg(MonthlyCharges),2) as avg_monthly_charges,
Round(Avg(TotalCharges),2) as avg_total_charges
from customers 
group by Churn;
#Customers who churn tend to have higher monthly charges