import numpy as np
import matplotlib.pyplot as plt

students = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]

year_2023 = [18000, 22000, 19000, 21000, 24000, 20000, 17000, 15000, 23000, 21000,
             18000, 16000, 25000, 22000, 19500, 17500, 24000, 21000, 18000, 16000,
             26000, 23000, 20000, 19000, 24500, 21500]

year_2024 = [22000, 26000, 21000, 19000, 23000, 24000, 18000, 17000, 25000, 22000,
             20000, 18500, 26000, 23000, 21000, 17500, 24500, 22000, 19500, 18000,
             27000, 24000, 21000, 20000, 23000, 25000]

year_2025 = [17000, 21000, 19000, 18000, 22000, 23000, 16000, 15000, 24000, 21000,
             20000, 17500, 25000, 22000, 20500, 18000, 23500, 21000, 19000, 17000,
             26000, 23500, 20500, 19500, 22500, 24000]

# Line chart
plt.figure(figsize=(12, 6))
plt.plot(students, year_2023, marker='o', label='2023')
plt.plot(students, year_2024, marker='s', label='2024')
plt.plot(students, year_2025, marker='^', label='2025')
plt.title('Student Income in Rupees')
plt.xlabel('Students')
plt.ylabel('Rupees (₹)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Bar chart
x = np.arange(len(students))
bar_width = 0.25

plt.figure(figsize=(12, 6))
plt.bar(x - bar_width, year_2023, width=bar_width, color='skyblue', label='2023')
plt.bar(x, year_2024, width=bar_width, color='lightgreen', label='2024')
plt.bar(x + bar_width, year_2025, width=bar_width, color='salmon', label='2025')
plt.title('Student Income in Rupees')
plt.xlabel('Students')
plt.ylabel('Rupees (₹)')
plt.xticks(x, students, rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Pie chart
plt.figure(figsize=(8, 8))
plt.pie(year_2023, labels=students, autopct='%1.1f%%', startangle=90)
plt.title('Student Income Distribution (2023)')
plt.show()

plt.figure(figsize=(8, 8))
plt.pie(year_2024, labels=students, autopct='%1.1f%%', startangle=90)
plt.title('Student Income Distribution (2024)')
plt.show()

plt.figure(figsize=(8, 8))
plt.pie(year_2025, labels=students, autopct='%1.1f%%', startangle=90)
plt.title('Student Income Distribution (2025)')
plt.show()