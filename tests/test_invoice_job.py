import logging
import time

import stripe
import pytest

import os
from tiptip.app import create_app
from tiptip.invoice_job import run
from tiptip.user.models import Customer, Merchant

stripe.api_key = os.getenv("STRIPE_API_KEY")
logging.getLogger().setLevel(logging.INFO)


@pytest.fixture()
def clean_tables():
    yield
    Customer.query.session.rollback()
    Customer.query.delete()
    Customer.query.session.commit()
    Merchant.query.session.rollback()
    Merchant.query.delete()
    Merchant.query.session.commit()


def make_customer(name, amount_paid):
    # Create customer with stripe
    stripe_customer = stripe.Customer.create(
        name=name,
    )

    # Save user to DB with customer ID.
    return Customer.create(
        username=name,
        email=("{}@example.com".format(name)),
        password="{}pass".format(name),
        active=True,
        stripe_id=stripe_customer.id,
        amount_paid=amount_paid,
    )


def make_merchant(name, amount_earned):
    # Create customer with stripe
    email = "{}@example.com".format(name)
    stripe_merchant = stripe.Account.create(
        type="custom",
        country="US",
        email=email,
        business_type="company",
        company={"name": name},
        business_profile={"url": "josh.us"},
        tos_acceptance={"date": int(time.time()), "ip": "8.8.8.8"},
        external_account={
            "account_number": "000123456789",
            "routing_number": "110000000",
            "object": "bank_account",
            "country": "US",
            "currency": "usd",
        },
        capabilities={
            "transfers": {"requested": True},
        },
    )

    # Save user to DB with merchant ID.
    return Merchant.create(
        username=name,
        email=email,
        password="{}pass".format(name),
        stripe_id=stripe_merchant.id,
        amount_earned=amount_earned,
    )


@pytest.fixture()
def customer_zak():
    customer = make_customer("zak", 0.75)
    yield customer
    stripe.Customer.delete(customer.stripe_id)


@pytest.fixture()
def customer_sara():
    customer = make_customer("sara", 1.25)
    yield customer
    stripe.Customer.delete(customer.stripe_id)


@pytest.fixture()
def merchant_sears():
    merchant = make_merchant("sears2", 3.25)
    stripe_id = merchant.stripe_id
    yield merchant
    stripe.Account.delete(stripe_id)


@pytest.fixture()
def merchant_acme():
    merchant = make_merchant("acme3", 1.5)
    stripe_id = merchant.stripe_id
    yield merchant
    stripe.Account.delete(stripe_id)


def test_success(
    db, customer_zak, customer_sara, merchant_acme, merchant_sears, clean_tables
):
    stripe.Topup.create(
        amount=2000,
        currency="usd",
        description="testtopup",
        statement_descriptor="Top-up",
        source="btok_us_verified",
    )
    try:
        run(os.getenv("STRIPE_API_KEY"))

        # Assert correct amount for invoices due
        zak_invoices = stripe.Invoice.list(limit=2, customer=customer_zak.stripe_id)
        assert len(zak_invoices.data) == 1
        assert zak_invoices.data[0].amount_due == 75

        sara_invoices = stripe.Invoice.list(limit=2, customer=customer_sara.stripe_id)
        assert len(sara_invoices.data) == 1
        assert sara_invoices.data[0].amount_due == 125

        # List last payouts
        acme_payouts = stripe.Transfer.list(
            limit=2, destination=merchant_acme.stripe_id
        )
        assert len(acme_payouts.data) == 1
        assert acme_payouts.data[0].amount == 150

        sears_payouts = stripe.Transfer.list(
            limit=2, destination=merchant_sears.stripe_id
        )
        assert len(sears_payouts.data) == 1
        assert sears_payouts.data[0].amount == 325

    finally:
        for invoice in stripe.Invoice.list():
            stripe.Invoice.delete(invoice)
