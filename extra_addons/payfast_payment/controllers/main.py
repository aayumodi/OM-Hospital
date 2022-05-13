from odoo import http
from odoo.http import request
from werkzeug.urls import url_parse

import logging
import werkzeug
import pprint
import socket
import requests
import hashlib
import urllib.parse

_logger = logging.getLogger(__name__)

class PayfastController(http.Controller):
    _notify_url = '/payment/payfast/notify_url/'
    _return_url = '/payment/payfast/return_url/'
    _cancel_url = '/payment/payfast/cancel_url/'



    def get_payfast_data(self, post):
        payfast =  request.env['payment.acquirer'].sudo().search([('provider', '=', 'payfast')])
        environment = 'prod' if payfast.state == 'enabled' else 'test'
        pfHost = 'sandbox.payfast.co.za' if environment == 'test' else 'www.payfast.co.za'
        # Get posted variables from ITN and convert to a string
        pfData = post
        pfParamString = " "
        for key in pfData:
        # Get all the data from PayFast and prepare parameter string
            if key != 'signature':
                pfParamString += key + "=" + urllib.parse.quote_plus(pfData[key].replace("+", " ")) + "&"
        # After looping through, cut the last & or append your passphrase
        # payload += "passphrase=SecretPassphrase123"
        pfParamString = pfParamString[:-1]
        return pfData, pfParamString


    def pfValidSignature(self,pfData, pfParamString):
        # import pdb; pdb.set_trace()
        signature = hashlib.md5(pfParamString.encode()).hexdigest()
        print(signature)
        return (pfData.get('signature') == signature)


    def pfValidIP(self):
        valid_hosts = [
        'www.payfast.co.za',
        'sandbox.payfast.co.za',
        'w1w.payfast.co.za',
        'w2w.payfast.co.za',
        ]
        valid_ips = []

        for item in valid_hosts:
            ips = socket.gethostbyname_ex(item)
            if ips:
                for ip in ips:
                    if ip:
                        valid_ips.append(ip)
        # Remove duplicates from array
        clean_valid_ips = []
        for item in valid_ips:
            # Iterate through each variable to create one list
            if isinstance(item, list):
                for prop in item:
                    if prop not in clean_valid_ips:
                        clean_valid_ips.append(prop)
            else:
                if item not in clean_valid_ips:
                    clean_valid_ips.append(item)

        # Security Step 3, check if referrer is valid
        if url_parse(request.headers.get("Referer")).host not in clean_valid_ips:
            return False
        else:
            return True 

    def pfValidPaymentData(cartTotal, pfData):
        return not (abs(float(cartTotal)) - float(pfData.get('amount'))) > 0.01 

    def pfValidServerConfirmation(pfParamString, pfHost = 'sandbox.payfast.co.za'):
        url = f"https://{pfHost}/eng/query/validate"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        response = requests.post(url, data=pfParamString, headers=headers)
        return response.text == 'VALID' 


    def payfast_validate_data(self,post):

        payfast = request.env['payment.acquirer'].search([('provider', '=', 'payfast')], limit=1)
        pfData,pfParamString = self.get_payfast_data(post)
        import pdb; pdb.set_trace()

        check1 = self.pfValidSignature(pfData, pfParamString)
        print(check1)
        check2 = self.pfValidIP()
        check3 = self.pfValidPaymentData(cartTotal, pfData)
        check4 = self.pfValidServerConfirmation(pfParamString, pfHost);


        if(check1 and check2 and check3 and check4):

            return werkzeug.utils.redirect('/payment/payfast/notify_url')
        else:
            return werkzeug.utils.redirect('/payment/process')

        return werkzeug.utils.redirect('/payment/process')


    @http.route('/payment/payfast/notify_url/', type='http', auth='public', website=True, csrf=False)
    def payfast_notify(self, **post):
        import pdb; pdb.set_trace()
        _logger.info('Beginning Payfast nitify form_feedback with post data %s', pprint.pformat(post))  # debug
        if not post:
            _logger.warning('Payfast: received empty notification; skip.')
        else:
            self.payfast_validate_data(post)
        return ''

    @http.route('/payment/payfast/return_url/', type='http', auth="public", csrf=False)
    def payfast_return(self, **post):
        # import pdb; pdb.set_trace()
        try:
            _logger.info('Beginning Payfast form_feedback with post data %s', pprint.pformat(post))  # debug
        except:
            pass
        return werkzeug.utils.redirect('/payment/process')
