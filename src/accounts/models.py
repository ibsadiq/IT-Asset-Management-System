from datetime import datetime

from flask_login import UserMixin 
from src import bcrypt, db
import re
from sqlalchemy import event, Enum


class User(UserMixin, db.Model): 
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User {self.email}>"
    


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    acronym = db.Column(db.String(10), nullable=False)

    def generate_acronym(self):
        words = re.findall(r'\b\w', self.name)
        self.acronym = ''.join(words).upper()

    def __repr__(self):
        return f"<Company {self.name} - {self.acronym}>"

@event.listens_for(Company.name, 'set', retval=True)
def generate_acronym_for_company(target, value, oldvalue, initiator):
    if value is not None:
        company = target
        company.generate_acronym()
        return value

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    company = db.relationship('Company', backref='locations')

    def __repr__(self):
        return self.site

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(250), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    company = db.relationship('Company', backref='departments')

    def __repr__(self):
        return self.department
    


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    serial_number = db.Column(db.String(50))
    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)
    status = db.Column(Enum('good', 'bad', name='asset_status'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    location = db.relationship('Location', backref='assets')
    department = db.relationship('Department', backref='assets')
    owner = db.relationship('Employee', backref='assets')

    def __repr__(self):
        return f"<Asset {self.name}>"
    


class AssignmentHistory(db.Model):
    __tablename__ = 'assignment_history'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    returned_date = db.Column(db.DateTime)
    return_reason = db.Column(Enum('exit', 'repair', name='assignment_status'), nullable=False)

    asset = db.relationship('Asset', backref='assignment_history')
    employee = db.relationship('Employee', backref='assignment_history')

    def __repr__(self):
        return f"<AssignmentHistory {self.id}>"
    

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    department = db.relationship('Department', backref='employees')

    def __repr__(self):
        return f"<Employee {self.name}>"
