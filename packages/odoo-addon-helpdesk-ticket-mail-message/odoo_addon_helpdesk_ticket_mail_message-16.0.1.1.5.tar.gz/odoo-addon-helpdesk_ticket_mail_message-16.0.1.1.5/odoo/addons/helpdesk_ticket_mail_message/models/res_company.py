from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = "res.company"

    def _default_helpdesk_reply_to_template_id(self):
        return self.env.ref(
            "helpdesk_ticket_mail_message.replying_to_email_ticket_template",
            raise_if_not_found=False,
        )

    def _default_helpdesk_forward_to_template_id(self):
        return self.env.ref(
            "helpdesk_ticket_mail_message.resending_email_ticket_template",
            raise_if_not_found=False,
        )

    helpdesk_reply_to_template_id = fields.Many2one(
        "mail.template",
        string=_("Helpdesk Reply-To Email Template"),
        domain="[('model', '=', 'helpdesk.ticket')]",
        default=_default_helpdesk_reply_to_template_id,
        help=_(
            "Email template used to set the Reply-To field when sending emails "
            "from helpdesk tickets."
        ),
    )
    helpdesk_forward_to_template_id = fields.Many2one(
        "mail.template",
        string=_("Helpdesk Forward-To Email Template"),
        domain="[('model', '=', 'helpdesk.ticket')]",
        default=_default_helpdesk_forward_to_template_id,
        help=_(
            "Email template used to set the Forward-To field when sending emails "
            "from helpdesk tickets."
        ),
    )
