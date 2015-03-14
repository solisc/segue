from segue.core import db
from segue.errors import NotAuthorized

from factories import BuyerFactory, PurchaseFactory, PaymentFactory
from models import Purchase, Payment

from .pagseguro import PagSeguroPaymentService
import schema

class PurchaseFilterStrategies(object):
    def given(self, **criteria):
        result = []
        for key, value in criteria.items():
            method = getattr(self, "by_"+key)
            result.append(method(value))
        return result

    def by_customer_id(self, value):
        return Purchase.customer_id == value

class PurchaseService(object):
    def __init__(self, db_impl=None, payments=None, strategies=None):
        self.db = db_impl or db
        self.payments = payments or PaymentService()
        self.filter_strategies = strategies or PurchaseFilterStrategies()

    def query(self, by=None, **kw):
        kw['customer_id'] = by.id
        filter_list = self.filter_strategies.given(**kw)
        return Purchase.query.filter(*filter_list).all()

    def create(self, buyer_data, product, account):
        buyer    = BuyerFactory.from_json(buyer_data, schema.buyer)
        purchase = PurchaseFactory.create(buyer, product, account)
        self.db.session.add(purchase)
        self.db.session.commit()
        return purchase

    def get_one(self, purchase_id, by=None):
        purchase = Purchase.query.get(purchase_id)
        if not purchase: return None
        if not self.check_ownership(purchase, by): raise NotAuthorized()
        return purchase

    def check_ownership(self, purchase, alleged):
        return purchase and alleged and purchase.customer_id == alleged.id

    def create_payment(self, purchase_id, payment_method, payment_data, by=None):
        purchase = self.get_one(purchase_id, by=by)
        return self.payments.create(purchase, payment_method, payment_data)

class PaymentService(object):
    DEFAULT_PROCESSORS = dict(
        pagseguro=PagSeguroPaymentService()
    )

    def __init__(self, **processors_overrides):
        self.processors_overrides = processors_overrides

    def create(self, purchase, method, data):
        processor = self.processor_for(method)
        payment = processor.create(purchase, data)
        instructions = processor.process(payment)
        return instructions

    def get_one(self, purchase_id, payment_id):
        result = Payment.query.filter(Purchase.id == purchase_id, Payment.id == payment_id)
        return result.first()

    def notify(self, purchase_id, payment_id, notification_code):
        pass

    def processor_for(self, method):
        if method in self.processors_overrides:
            return self.processors_overrides[method]
        if method in self.DEFAULT_PROCESSORS:
            return self.DEFAULT_PROCESSORS[method]
        raise NotImplementedError(method+' is not a valid payment method')
