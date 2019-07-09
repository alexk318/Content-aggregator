from wtforms import Form, StringField, PasswordField


class RegistrationForms(Form):
    nameform = StringField('Name:')
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')


class LoginForms(Form):
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')


regforms = RegistrationForms()
logforms = LoginForms()
