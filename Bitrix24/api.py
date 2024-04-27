import requests
import random
from tele_bot.config import BASE_URL

def create_lead(name, phone, email, query):
    url = BASE_URL + "crm.lead.add"
    data = {
        'fields': {
            "TITLE": query,
            "NAME": name,
            "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
            "EMAIL": [{"VALUE": email, "VALUE_TYPE": "WORK"}]
        },
        'params': {"REGISTER_SONET_EVENT": "Y"}
    }
    response = requests.post(url, json=data)
    print("API_RESPONSE", response.text)
    return response.json()

def get_employee_id(department_id=7):
    url = BASE_URL + "user.get"
    params = {
        "FILTER": {"ACTIVE": True, "UF_DEPARTMENT": department_id},
        "SELECT": ["ID", "NAME", "LAST_NAME", "WORK_POSITION"]
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        employees = response.json()
        print("Employees in Department:", employees)
        if employees.get('result'):
            employee = random.choice(employees['result'])
            print(f"Randomly selected employee: {employee['NAME']} {employee['LAST_NAME']} (ID: {employee['ID']})")
            return employee['ID']
        else:
            print("No employees found in the specified department.")
            return None
    else:
        print("Failed to fetch employees:", response.status_code, response.text)
        return None


def assign_lead_to_employee(lead_id, employee_id):
    url = BASE_URL + "crm.lead.update"
    data = {
        'id': lead_id,
        'fields': {
            "ASSIGNED_BY_ID": employee_id
        }
    }
    response = requests.post(url, json=data)
    print("Assignment Response:", response.text)
    return response.json()

def update_lead_stage(lead_id, stage_id):
    url = BASE_URL + "crm.lead.update"
    data = {
        'id': lead_id,
        'fields': {
            "STATUS_ID": stage_id
        }
    }
    response = requests.post(url, json=data)
    print("Update Lead Stage Response:", response.text)
    return response.json()
