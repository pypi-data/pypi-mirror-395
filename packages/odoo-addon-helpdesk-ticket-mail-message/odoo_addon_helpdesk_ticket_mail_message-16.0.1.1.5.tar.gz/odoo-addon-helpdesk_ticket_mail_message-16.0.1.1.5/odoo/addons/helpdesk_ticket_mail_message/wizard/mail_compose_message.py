from odoo import models, fields, api, tools
from odoo.tools.translate import _
from odoo.exceptions import UserError


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    helpdesk_ticket_tag_ids = fields.Many2many(
        "helpdesk.ticket.tag",
    )
    available_mail_template_ids = fields.Many2many(
        "mail.template",
        compute="_compute_available_mail_template_ids",
    )
    lang = fields.Selection(string="Language", selection="_get_lang")
    scheduled_date = fields.Datetime(
        string=_("Scheduled Date"),
        help=_(
            "Send at the scheduled date (if in the past, it will be sent immediately)."
        ),
    )
    include_history_in_email = fields.Boolean(
        string=_("Include Message History in Email"),
        help=_(
            "Include the message history in the email body when sending emails from "
            "helpdesk tickets."
        ),
    )
    mail_message_id = fields.Many2one(
        "mail.message",
        string=_("Mail Message"),
        help=_("The mail message to which the email is a reply or forward."),
    )

    def _ensure_non_duplicates(self, partner_ids):
        """
        Remove duplicate emails from email_to and email_cc fields, ensuring that
        partner emails are not duplicated in the recipients and that each list
        contains unique emails.
        """
        partners = self.env["res.partner"].browse(partner_ids)
        partner_emails = {tools.email_normalize(p.email) for p in partners if p.email}

        email_to_set = set(tools.email_normalize_all(self.email_to))
        email_cc_set = set(tools.email_normalize_all(self.email_cc))

        # Remove partner emails from both sets
        email_to_set -= partner_emails
        email_cc_set -= partner_emails

        # Remove any emails in email_to from email_cc to avoid duplicates across fields
        email_cc_set -= email_to_set

        self.email_to = ",".join(sorted(email_to_set))
        self.email_cc = ",".join(sorted(email_cc_set))

    def _append_mail_message_body(self, body):
        """
        Append the body of an existing mail.message to the body of the composer.
        """
        if not self.mail_message_id.exists():
            return body

        original_body = self.mail_message_id._get_message_body_for_reply()
        return f"{body}<br/>{original_body}"

    @api.model
    def default_get(self, fields):
        result = super(MailComposeMessage, self).default_get(fields)

        ctx = self.env.context.copy()
        if result.get("model") == "helpdesk.ticket" and result.get("res_id"):
            ticket = self.env[result.get("model")].browse(result.get("res_id"))
            result["helpdesk_ticket_tag_ids"] = ticket.tag_ids.ids
            result["lang"] = (
                ticket.partner_id.lang
                if ticket.partner_id and ticket.partner_id.lang
                else self.env.user.lang
            )

            mail_message = self.env["mail.message"].browse(ctx.get("mail_message_id"))
            if mail_message.exists():
                result["mail_message_id"] = mail_message.id
                return result

            template_id = result.get("template_id") or ctx.get("default_template_id")
            if template_id:
                template = self.env["mail.template"].browse(template_id)
                result["include_history_in_email"] = template.include_history_in_email

        return result

    @api.onchange("template_id")
    def _onchange_template_id_wrapper(self):
        """
        Prevent onchange from messing with defaults when the template is set from
        the mass mailing wizard in the helpdesk ticket form view
        """
        if self._context and self._context.get("skip_onchange_template_id"):
            self.ensure_one()
            # try to apply the template values even if the composition mode
            # is mass_mailing.
            try:
                values = self.with_context(
                    lang=self.lang,
                    include_history_in_email=self.include_history_in_email,
                )._onchange_template_id(
                    self.template_id.id, "", self.model, self.res_id
                )["value"]
                for fname, value in values.items():
                    setattr(self, fname, value)
            except Exception:
                raise UserError(
                    "The selected template is not compatible with the current "
                    "context. Please select a different template."
                )
            return

        super(MailComposeMessage, self)._onchange_template_id_wrapper()

    @api.onchange("lang", "include_history_in_email")
    def _onchange_template_related_fields(self):
        """
        Update the email template fields when either the language or the
        include_history_in_email fields are changed.
        """
        if self.template_id:
            template_values = self.with_context(
                lang=self.lang,
                include_history_in_email=self.include_history_in_email,
            ).generate_email_for_composer(
                self.template_id.id, [self.res_id]
            )
            self.update(template_values[self.res_id])

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        """
        Override (for helpdesk tickets only) to avoid the email composer to suggest
        addresses based on ticket partners, since it was causing duplicates for gmail
        accounts. (See also helpdesk_automatic_stage_changes/models/helpdesk_ticket.py)
        """
        if fields is None:
            fields = [
                "subject",
                "body_html",
                "email_from",
                "email_to",
                "partner_to",
                "email_cc",
                "reply_to",
                "attachment_ids",
                "mail_server_id",
            ]

        # let's reproduce the original method's logic changing tpl_partners_only
        multi_mode = True
        if isinstance(res_ids, int):
            multi_mode = False
            res_ids = [res_ids]

        returned_fields = fields + ["partner_ids", "attachments"]
        values = dict.fromkeys(res_ids, False)

        template_values = (
            self.env["mail.template"]
            .with_context(tpl_partners_only=False)
            .browse(template_id)
            .generate_email(res_ids, fields)
        )
        for res_id in res_ids:
            res_id_values = dict(
                (field, template_values[res_id][field])
                for field in returned_fields
                if template_values[res_id].get(field)
            )
            res_id_values["body"] = res_id_values.pop("body_html", "")
            values[res_id] = res_id_values

        template_values = (
            multi_mode and values or values[res_ids[0]]
        )  # this would be the return value in the original method

        if self._context.get("active_model") == "helpdesk.ticket":
            for res_id in res_ids:
                self._ensure_non_duplicates(
                    template_values[res_id].get("partner_ids", [])
                )
                body = template_values[res_id].get("body", "") or ""
                template_values[res_id]["body"] = self._append_mail_message_body(body)

        return template_values

    @api.depends("helpdesk_ticket_tag_ids")
    def _compute_available_mail_template_ids(self):
        for record in self:
            available_templates = self.env["mail.template"].search(
                [("model", "=", record.model)]
            )
            if record.model == "helpdesk.ticket" and record.helpdesk_ticket_tag_ids:
                record_tag_ids = record.helpdesk_ticket_tag_ids.ids
                ticket_templates = available_templates.filtered(
                    lambda t: not t.helpdesk_ticket_tag_ids
                    or bool(set(t.helpdesk_ticket_tag_ids.ids) & set(record_tag_ids))
                )
                record.available_mail_template_ids = ticket_templates.ids
            else:
                record.available_mail_template_ids = available_templates.ids

    @api.model
    def _get_lang(self):
        return self.env["res.lang"].get_installed()

    def _action_send_mail(self, auto_commit=False):
        if self.model == "helpdesk.ticket":
            ctx = self._context.copy()
            ctx.update(
                {
                    "default_email_to": str(self.email_to).replace(";", ",") or "",
                    "default_email_cc": str(self.email_cc).replace(";", ",") or "",
                }
            )
            if self.lang:
                ctx["lang"] = self.lang
            ctx["include_history_in_email"] = self.include_history_in_email

            self = self.with_context(ctx)
        return super(MailComposeMessage, self)._action_send_mail(
            auto_commit=auto_commit
        )

    def get_mail_values(self, res_ids):
        results = super(MailComposeMessage, self).get_mail_values(res_ids)

        if self.model == "helpdesk.ticket" and self.scheduled_date:
            for res_id in results.keys():
                results[res_id]["scheduled_date"] = self.scheduled_date

        return results
