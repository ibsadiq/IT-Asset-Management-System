from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from accounts.models import Asset, Location, Department, Employee

class AssetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    description = TextAreaField('Description')
    serial_number = StringField('Serial Number')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d')
    warranty_expiry = DateField('Warranty Expiry', format='%Y-%m-%d')
    status = SelectField('Status', choices=[('good', 'Good'), ('bad', 'Bad')], validators=[DataRequired()])
    location = QuerySelectField('Location', query_factory=lambda: Location.query.all(), get_label='name', validators=[DataRequired()])
    department = QuerySelectField('Department', query_factory=lambda: Department.query.all(), get_label='name', validators=[DataRequired()])
    owner = QuerySelectField('Owner', query_factory=lambda: Employee.query.all(), get_label='name', allow_blank=True)
