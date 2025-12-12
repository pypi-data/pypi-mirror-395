from faker import Faker
import random
import pandas as pd
fake = Faker()

USER_TEMPLATE = {
    "full_name": lambda: fake.name(),
    "username": lambda: fake.user_name(),
    "email": lambda: fake.email(),
    "phone_number": lambda: fake.phone_number(),
    "gender": lambda: random.choice(["male", "female", "other"]),
    "date_of_birth": lambda: fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat()
}

EMPLOYEE_TEMPLATE = {
    "full_name": lambda: fake.name(),
    "employee_id": lambda: fake.uuid4()[:8],
    "email": lambda: fake.company_email(),
    "department": lambda: random.choice(["HR","Engineering","Sales"]),
    "salary": lambda: round(random.uniform(30000,120000),2)
}

STUDENT_TEMPLATE = {
    "full_name": lambda: fake.name(),
    "student_id": lambda: str(random.randint(10000,99999)),
    "gpa": lambda: round(random.uniform(2.0,4.0),2),
    "year": lambda: random.randint(1,4)
}

PRODUCT_TEMPLATE = {
    "product_name": lambda: fake.word().capitalize(),
    "price": lambda: round(random.uniform(100,5000),2),
    "stock_quantity": lambda: random.randint(0,1000)
}

BANK_ACCOUNT_TEMPLATE = {
    "account_number": lambda: str(random.randint(10000000,99999999)),
    "account_holder": lambda: fake.name(),
    "balance": lambda: round(random.uniform(0,1000000),2)
}

HEALTH_PATIENT_TEMPLATE = {
    "full_name": lambda: fake.name(),
    "patient_id": lambda: fake.uuid4()[:8],
    "height_cm": lambda: round(random.uniform(50,200),1),
    "weight_kg": lambda: round(random.uniform(3,150),1)
}

TEMPLATE_MENU = {
    1: USER_TEMPLATE,
    2: EMPLOYEE_TEMPLATE,
    3: STUDENT_TEMPLATE,
    4: PRODUCT_TEMPLATE,
    5: BANK_ACCOUNT_TEMPLATE,
    6: HEALTH_PATIENT_TEMPLATE
}

TEMPLATE_NAMES = {
    1: "User",
    2: "Employee",
    3: "Student",
    4: "Product",
    5: "Bank Account",
    6: "Patient"
}

def generate_data(template_number, n_rows=1, seed=None):
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)
    
    template = TEMPLATE_MENU[template_number]
    data = []
    for _ in range(n_rows):
        row = {key: func() for key, func in template.items()}
        data.append(row)
    return data

__version__ = "0.1.0"
