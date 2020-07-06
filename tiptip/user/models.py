# -*- coding: utf-8 -*-
import decimal
import datetime as dt

from flask_login import UserMixin

from tiptip.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
)
from tiptip.extensions import bcrypt


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    type = Column(db.String(20))

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "user"}


class Customer(User):
    is_admin = Column(db.Boolean(), default=False)
    amount_paid = Column(db.Numeric(), default=0)

    def charge(self, amount):
        self.amount_paid += decimal.Decimal(amount)

    __mapper_args__ = {
        "polymorphic_identity": "customer",
    }


class Merchant(User):
    verified = Column(db.Boolean(), default=False)
    amount_earned = Column(db.Numeric(), default=0)

    def pay(self, amount):
        self.amount_earned += decimal.Decimal(amount)

    def verify(self):
        self.verified = True

    __mapper_args__ = {
        "polymorphic_identity": "merchant",
    }
