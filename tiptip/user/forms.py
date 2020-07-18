# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from tiptip.user.models import Customer, Merchant


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = Customer.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = Customer.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class MerchantRegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Company Name", validators=[DataRequired(), Length(min=3, max=45)]
    )
    email = StringField(
        "Contact Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(MerchantRegisterForm, self).__init__(*args, **kwargs)
        self.merchant = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(MerchantRegisterForm, self).validate()
        if not initial_validation:
            return False
        merchant = Merchant.query.filter_by(username=self.username.data).first()
        if merchant:
            self.username.errors.append("Merchant already registered")
            return False
        merchant = Merchant.query.filter_by(email=self.email.data).first()
        if merchant:
            self.email.errors.append("Email already registered")
            return False
        return True
