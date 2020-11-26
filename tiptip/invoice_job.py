import logging
import stripe
from tiptip.user.models import Customer, Merchant

logger = logging.getLogger(__name__)


def run(api_key):
    stripe.api_key = api_key
    for customer in Customer.query:
        stripe.InvoiceItem.create(
            customer=customer.stripe_id,
            amount=int(100 * customer.amount_paid),
            currency="usd",
        )
        stripe.Invoice.create(customer=customer.stripe_id, auto_advance=True)

    for merchant in Merchant.query:
        stripe.Transfer.create(
            amount=int(100 * merchant.amount_earned),
            currency="usd",
            destination=merchant.stripe_id,
        )
