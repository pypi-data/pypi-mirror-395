# 🎲 OJT Data Generator

A powerful and easy-to-use Python package for generating realistic fake data for testing, development, and prototyping. Built with Python's Faker library and Pandas, OJT Data Generator provides an interactive command-line interface and programmatic API to quickly generate structured datasets for various use cases.

## 🎯 Why OJT Data Generator?

Whether you're building a new application, testing database schemas, creating demos, or learning data analysis, you need realistic sample data. OJT Data Generator makes this process effortless by providing:

- **Pre-built Templates**: 6 ready-to-use data templates covering common use cases
- **Interactive CLI**: User-friendly command-line interface requiring no coding
- **Programmatic API**: Import and use in your Python scripts for automation
- **Reproducible Data**: Set seeds to generate consistent datasets
- **Export Ready**: Save generated data directly to CSV files
- **Pandas Integration**: Data returned as pandas DataFrames for easy manipulation

## ✨ Features

Generate realistic fake data with 6 pre-built templates:

- 👤 **User Data** - Full name, username, email, phone number, gender, date of birth
- 💼 **Employee Data** - Full name, employee ID, company email, department, salary
- 🎓 **Student Data** - Full name, student ID, GPA, academic year
- 📦 **Product Data** - Product name, price, stock quantity
- 🏦 **Bank Account Data** - Account number, account holder, balance
- 🏥 **Patient Data** - Full name, patient ID, height (cm), weight (kg)

## 📦 Installation

```bash
pip install ojt-data-generator
```

## 🚀 Quick Start

After installation, simply run the interactive CLI:

```bash
ojt
```

The tool will guide you through:
1. Selecting a data template
2. Choosing the number of rows to generate
3. Optionally setting a seed for reproducible data
4. Viewing the generated data
5. Saving to CSV if needed

## 💡 Example Usage

```bash
$ ojt
Select a template:
1. User
2. Employee
3. Student
4. Product
5. Bank Account
6. Patient
Enter template number: 1
Number of rows (default 1): 5
Seed (optional): 42

# Generated data will be displayed as a pandas DataFrame
# Option to save as CSV file
```

## 🔧 Use as a Library

You can also import and use OJT in your Python scripts for automation:

```python
from ojt import generate_data, TEMPLATE_NAMES
import pandas as pd

# Generate 10 user records with a seed for reproducibility
data = generate_data(template_number=1, n_rows=10, seed=42)
df = pd.DataFrame(data)
print(df)

# Save to CSV
df.to_csv('users.csv', index=False)

# Generate employee data
employee_data = generate_data(template_number=2, n_rows=50)
employees_df = pd.DataFrame(employee_data)

# Generate student data for testing
student_data = generate_data(template_number=3, n_rows=100, seed=123)
students_df = pd.DataFrame(student_data)
```

## 📊 Template Details

### 1. User Template
Perfect for user registration, authentication systems, and social platforms.
- Full Name
- Username
- Email Address
- Phone Number
- Gender (male/female/other)
- Date of Birth (ISO format)

### 2. Employee Template
Ideal for HR systems, payroll applications, and organizational databases.
- Full Name
- Employee ID (8-character UUID)
- Company Email
- Department (HR/Engineering/Sales)
- Salary ($30,000 - $120,000)

### 3. Student Template
Great for educational platforms, learning management systems, and academic tools.
- Full Name
- Student ID (5-digit number)
- GPA (2.0 - 4.0)
- Academic Year (1-4)

### 4. Product Template
Useful for e-commerce platforms, inventory systems, and retail applications.
- Product Name
- Price ($100 - $5,000)
- Stock Quantity (0-1,000 units)

### 5. Bank Account Template
Perfect for financial applications, banking systems, and payment platforms.
- Account Number (8-digit)
- Account Holder Name
- Balance ($0 - $1,000,000)

### 6. Patient Template
Designed for healthcare applications, medical records, and health tracking systems.
- Full Name
- Patient ID (8-character UUID)
- Height (50-200 cm)
- Weight (3-150 kg)

## 🎓 Use Cases

- **Software Testing**: Generate test data for unit tests, integration tests, and QA
- **Database Seeding**: Populate development and staging databases
- **Demos & Presentations**: Create realistic demo data for product showcases
- **Learning & Training**: Practice data analysis, SQL queries, and data visualization
- **Prototyping**: Quickly mock up applications with realistic data
- **API Testing**: Generate payloads for API endpoint testing

## 📋 Requirements

- Python >= 3.7
- faker >= 18.0.0
- pandas >= 1.3.0

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Kushal Kotiny

## 🔗 Links

- PyPI: https://pypi.org/project/ojt-data-generator/
- GitHub: https://github.com/kushalkotiny/ojt
