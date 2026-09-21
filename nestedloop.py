# name generator random string generator for 50 strings 
import random

first_names = [
    "Rohit", "Mohit", "Livesh", "Vishal", "Gourav",
    "Aman", "Ankit", "Arjun", "Rahul", "Karan",
    "Nikhil", "Sahil", "Harsh", "Yash", "Akash",
    "Deepak", "Manish", "Abhishek", "Sumit", "Varun"
]

last_names = [
    "Sharma", "Kumar", "Gupta", "Verma", "Singh",
    "Jain", "Patel", "Malhotra", "Mehta", "Chopra"
]

# Generate 50 random names
for i in range(50):
    name = random.choice(first_names) + " " + random.choice(last_names)
    print(name)