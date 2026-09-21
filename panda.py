import pandas as pd

# Mock student data
data = {
    "Roll No": [
        f"{i:03d}" for i in range(1, 51)
    ],

    "Name": [
        "Rohit Sharma", "Mohit Kumar", "Livesh Garg", "Vishal Verma",
        "Gourav Singh", "Aman Gupta", "Ankit Sharma", "Arjun Kumar",
        "Rahul Verma", "Karan Singh", "Nikhil Jain", "Sahil Kumar",
        "Harsh Sharma", "Yash Gupta", "Akash Verma", "Deepak Singh",
        "Manish Kumar", "Abhishek Jain", "Sumit Sharma", "Varun Gupta",
        "Piyush Kumar", "Ravi Verma", "Aakash Singh", "Neeraj Sharma",
        "Vikas Kumar", "Saurabh Jain", "Rohit Verma", "Mohit Sharma",
        "Kunal Gupta", "Aditya Singh", "Ayush Kumar", "Himanshu Verma",
        "Pranav Sharma", "Rajat Gupta", "Shubham Singh", "Tarun Kumar",
        "Dev Sharma", "Mandeep Singh", "Navjot Kumar", "Gaurav Verma",
        "Simran Kaur", "Neha Sharma", "Priya Gupta", "Anjali Singh",
        "Pooja Verma", "Komal Sharma", "Riya Gupta", "Muskan Kumar",
        "Sakshi Jain", "Nisha Singh"
    ],

    "Class": [
        "M.Com", "M.Com", "MCA", "MCA", "M.Com",
        "MA", "MCA", "M.Com", "M.Com", "M.Com",
        "MA", "M.Com", "MCA", "MA", "MCA",
        "MCA", "MA", "MA", "MA", "MA",
        "MA", "MA", "M.Com", "M.Com", "MCA",
        "MA", "M.Com", "MA", "M.Com", "M.Com",
        "M.Com", "M.Com", "MA", "M.Com", "MCA",
        "MCA", "MA", "MCA", "M.Com", "M.Com",
        "M.Com", "MA", "M.Com", "MA", "M.Com",
        "MCA", "MA", "MCA", "MCA", "M.Com"
    ],

    "Section": [
        "A", "A", "C", "C", "C",
        "A", "A", "A", "C", "C",
        "B", "A", "B", "A", "A",
        "A", "C", "C", "A", "C",
        "C", "A", "A", "B", "A",
        "B", "A", "A", "C", "A",
        "A", "A", "B", "C", "B",
        "A", "B", "C", "A", "B",
        "A", "A", "C", "B", "B",
        "C", "A", "C", "B", "B"
    ],

    "Admission Date": [
        "2023-07-15", "2023-08-05", "2023-07-18", "2023-09-25",
        "2023-07-12", "2023-07-05", "2023-07-28", "2023-09-16",
        "2023-07-26", "2023-09-28", "2023-07-29", "2023-08-05",
        "2023-09-28", "2023-08-05", "2023-08-13", "2023-08-18",
        "2023-08-14", "2023-07-06", "2023-09-07", "2023-07-11",
        "2023-09-19", "2023-09-12", "2023-07-09", "2023-07-30",
        "2023-07-30", "2023-08-05", "2023-08-16", "2023-08-15",
        "2023-08-04", "2023-09-21", "2023-09-20", "2023-08-01",
        "2023-08-18", "2023-09-27", "2023-09-26", "2023-07-30",
        "2023-08-21", "2023-07-28", "2023-08-10", "2023-09-02",
        "2023-08-28", "2023-07-18", "2023-09-10", "2023-09-13",
        "2023-08-21", "2023-07-18", "2023-07-12", "2023-07-20",
        "2023-09-26", "2023-07-09"
    ],

    "Program": [
        "M.Com", "M.Com", "MCA", "MCA", "M.Com",
        "MA", "MCA", "M.Com", "M.Com", "M.Com",
        "MA", "M.Com", "MCA", "MA", "MCA",
        "MCA", "MA", "MA", "MA", "MA",
        "MA", "MA", "M.Com", "M.Com", "MCA",
        "MA", "M.Com", "MA", "M.Com", "M.Com",
        "M.Com", "M.Com", "MA", "M.Com", "MCA",
        "MCA", "MA", "MCA", "M.Com", "M.Com",
        "M.Com", "MA", "M.Com", "MA", "M.Com",
        "MCA", "MA", "MCA", "MCA", "M.Com"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Display DataFrame
print(df)

# Convert DataFrame to CSV
df.to_csv("student_mock_data.csv", index=False)

print("\nCSV file created successfully!")
print("File name: student_mock_data.csv")