# Copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).
import binascii

from odoo import http, fields, SUPERUSER_ID, _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

class CustomerPortal(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>/shop/payment'], type='json', auth="public", website=True)
    def website_order_signature(self, order_id, access_token=None, name=None, signature=None, send_label=None):

        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            order_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}
        pdf = request.env.ref('sale.action_report_saleorder').with_user(SUPERUSER_ID)._render_qweb_pdf([order_sudo.id])[0]
        _message_post_helper(
            'sale.order', order_sudo.id, _('Order signed by %s') % (name,),
            attachments=[('%s.pdf' % order_sudo.name, pdf)],
            **({'token': access_token} if access_token else {}))
        redirect_url = request.httprequest.url_root
        ends_with_slash = redirect_url.endswith("/")
        if ends_with_slash:
            redirect_url = F"{redirect_url}shop/payment"
        else:
            redirect_url = F"{redirect_url}/shop/payment"
        return {
            'force_refresh': True,
            'redirect_url': redirect_url
        }