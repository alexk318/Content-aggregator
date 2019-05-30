from wtforms import Form, StringField, PasswordField, BooleanField


class RegistrationForms(Form):
    nameform = StringField('Name:')
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')


class LoginForms(Form):
    emailform = StringField('Email:')
    passwordform = PasswordField('Password:')
    checkbox = BooleanField('Remember me:')


regforms = RegistrationForms()
logforms = LoginForms()
