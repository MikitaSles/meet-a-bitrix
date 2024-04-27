# Bitrix/models.py
class Lead:
    def __init__(self, name, phone, email, query):
        self.name = name
        self.phone = phone
        self.email = email
        self.query = query

class Employee:
    def __init__(self, employee_id, name, last_name, work_position):
        self.employee_id = employee_id
        self.name = name
        self.last_name = last_name
        self.work_position = work_position
