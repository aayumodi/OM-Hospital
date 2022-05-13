from odoo import api, fields, models, _
from werkzeug import urls
from odoo.addons.payfast_payment.controllers.main import PayfastController
from hashlib import md5

import hashlib
import urllib.parse


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('payfast', 'Payfast')],  ondelete={'payfast': 'set default'})
    payfast_key_id = fields.Char(string='Key ID', groups='base.group_user')
    payfast_key_secret = fields.Char(string='Key Secret', groups='base.group_user')


    @api.model
    def _get_payfast_urls(self, environment):
        """ Payfast URLS """
        if environment == 'prod':
            return {
                'payfast_form_url': 'https://www.payfast.co.za/eng/process',
            }
        else:
            return {
                'payfast_form_url': 'https://sandbox.payfast.co.za/eng/process',
            }

    

    # def _payfast_generate_sign(self, inout, values):
    #     if inout not in ('in', 'out'):
    #         raise Exception("Type must be 'in' or 'out'")

    #     if inout == 'in':
    #         data_string = ('~').join((self.payfast_key_secret, self.payfast_key_id, values['reference'],
    #                                       str(values['amount']), values['currency_code']))
    #     else:
    #         rounded_amount = decimal.Decimal(values.get('TX_VALUE')).quantize(decimal.Decimal('0.1'), decimal.ROUND_HALF_EVEN)
    #         data_string = ('~').join((self.payfast_key_secret, self.payfast_key_id, values['reference'],
    #                                       str(rounded_amount), values['currency_code'], values.get('transactionState')))
    #     shasign = md5(data_string.encode('utf-8'))
    #     return shasign.hexdigest()
        # return md5(data_string.encode('utf-8')).hexdigest()


    def payfast_form_generate_values(self, values):
        base_url = self.get_base_url()

        payfast_tx_values = dict(values)
        payfast_tx_values.update({
            'merchant_id': int(self.payfast_key_id),
            'merchant_key': self.payfast_key_secret,
            'm_payment_id':values['reference'],
            'cmd': '_xclick',
            'business': 'test',
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'item_number': values['reference'],
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
            'notify_url': urls.url_join(base_url, PayfastController._notify_url),
            'return_url': urls.url_join(base_url, PayfastController._return_url),
            'cancel_url': urls.url_join(base_url, PayfastController._cancel_url),
        })
        # payfast_tx_values['signature'] = self._payfast_generate_sign("in", payfast_tx_values)
        return payfast_tx_values



    def payfast_get_form_action_url(self):
        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        return self._get_payfast_urls(environment)['payfast_form_url']


# mobile_number =27875510569
# sa_id = 0590794029
# mail = neyil45351@azteen.com