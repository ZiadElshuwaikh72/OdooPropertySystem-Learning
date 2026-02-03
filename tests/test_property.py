from odoo.tests.common import TransactionCase
from odoo import fields

class TestProperty(TransactionCase):

    def setUp(self,*args,**kwargs):
        super(TestProperty,self).setUp()
        self.property_01_record=self.env['property'].create({
            'ref':'PTR 1000',
            'name': 'property 1000',
            'postcode':'101',
            'description':'description 1000',
            'date_availability':fields.Datetime.today(),
            'bedrooms':10,
            'expected_price':1000
        })

    def test_01_property_check_values(self):
        property_id=self.property_01_record
        self.assertRecordValues(property_id,[{
            'ref': 'PTR 1000',
            'name': 'property 1000',
            'postcode': '101',
            'description': 'description 1000',
            'date_availability': fields.Datetime.today(),
            'bedrooms': 10,
            'expected_price': 1000
        }])