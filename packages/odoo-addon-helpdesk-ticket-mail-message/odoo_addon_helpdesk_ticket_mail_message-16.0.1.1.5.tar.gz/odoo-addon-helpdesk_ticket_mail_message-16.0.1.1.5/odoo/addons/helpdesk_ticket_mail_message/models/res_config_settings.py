from odoo import models, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    helpdesk_reply_to_template_id = fields.Many2one(
        "mail.template",
        string=_("Helpdesk Reply-To Email Template"),
        related="company_id.helpdesk_reply_to_template_id",
        readonly=False,
    )
    helpdesk_forward_to_template_id = fields.Many2one(
        "mail.template",
        string=_("Helpdesk Forward-To Email Template"),
        related="company_id.helpdesk_forward_to_template_id",
        readonly=False,
    )
