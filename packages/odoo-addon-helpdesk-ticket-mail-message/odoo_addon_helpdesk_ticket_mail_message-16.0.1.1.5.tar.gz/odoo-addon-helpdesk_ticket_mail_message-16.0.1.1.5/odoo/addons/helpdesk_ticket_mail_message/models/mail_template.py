from odoo import models, fields, _


class MailTemplate(models.Model):
    _inherit = "mail.template"

    helpdesk_ticket_tag_ids = fields.Many2many(
        "helpdesk.ticket.tag", help=_("Helpdesk Tags related to this template.")
    )
    include_history_in_email = fields.Boolean(
        string=_("Include Message History in Email"),
        help=_(
            "Include the message history in the email body when sending emails from "
            "helpdesk tickets."
        ),
    )

    def generate_email(self, res_ids, fields):
        """
        Generate email for the given record ids and fields override to force the language
        instead of relying on the ticket's partner language for helpdesk tickets.
        """
        model = self._context.get("active_model") or self._context.get(
            "params", {}
        ).get("model")
        if model != "helpdesk.ticket":
            return super().generate_email(res_ids, fields)

        lang = self._context.get("lang") or self.env.lang
        if lang:
            self = self.with_context(lang=lang)
            self.lang = lang

        template_values = super().generate_email(res_ids, fields)

        ticket = self.env["helpdesk.ticket"].browse(res_ids)
        if not ticket.exists():
            return template_values

        include_history = self.env.context.get(
            "include_history_in_email", self.include_history_in_email
        )
        if include_history and not self.env.context.get("mail_message_id"):
            for res_id in res_ids:
                if res_id not in template_values or "body_html" not in template_values[res_id]:
                    continue

                current_body = template_values[res_id]["body_html"] or ""
                history = ticket.get_message_body_with_history()
                template_values[res_id]["body_html"] = str(current_body) + str(
                    history
                )

        return template_values
