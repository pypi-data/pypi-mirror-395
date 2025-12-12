import base64
from markupsafe import Markup

from odoo import models, fields, api, tools, _
from odoo.tools.mimetypes import guess_mimetype


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    name = fields.Char(string="Title", required=True, size=100)
    message_emails_ids = fields.One2many(
        "mail.message", compute="_compute_emails", string="Messages"
    )
    color_row = fields.Char("Color Row", default="#000000")
    color_background_row = fields.Char("Color Background Row", default="#FFFFFF")
    partner_category_id = fields.Many2many(
        related="partner_id.category_id", string="Partner Category", readonly=True
    )
    partner_contact_phone = fields.Char(
        related="partner_id.phone",
        string=_("Partner Phone"),
        readonly=True,
    )
    last_email_sent_date = fields.Datetime(
        string=_("Last Email Sent Date"),
        compute="_compute_last_email_sent_date",
        store=True,
        readonly=True,
    )
    last_email_received_date = fields.Datetime(
        string=_("Last Email Received Date"),
        compute="_compute_last_email_received_date",
        store=True,
        readonly=True,
    )

    @api.depends("message_emails_ids")
    def _compute_last_email_sent_date(self):
        for ticket in self:
            last_sent_msg = ticket.message_emails_ids.filtered(
                lambda msg: msg.message_type == "email"
                and msg.message_type_mail == "email_sent"
            ).sorted("date", reverse=True)[:1]
            ticket.last_email_sent_date = last_sent_msg.date if last_sent_msg else False

    @api.depends("message_emails_ids")
    def _compute_last_email_received_date(self):
        for ticket in self:
            last_received_msg = ticket.message_emails_ids.filtered(
                lambda msg: msg.message_type == "email"
                and msg.message_type_mail == "email_received"
            ).sorted("date", reverse=True)[:1]
            ticket.last_email_received_date = (
                last_received_msg.date if last_received_msg else False
            )

    @api.model
    def message_new(self, msg, custom_values=None):
        """Override message_new from mail gateway so we can set correctly
        process attached images in the ticket description.
        """
        ticket = super().message_new(msg, custom_values)

        msg_body = msg.get("body", Markup(""))
        for attachment in msg.get("attachments", []):
            cid = attachment.info.get("cid")
            if not cid or f"cid:{cid}" not in msg_body:
                continue

            mimetype = guess_mimetype(attachment.content, attachment.fname)
            if not mimetype or not mimetype.startswith("image/"):
                continue

            b64_content = base64.b64encode(attachment.content)
            data_url = f"data:{mimetype};base64,{b64_content.decode('utf-8')}"

            msg_body = msg_body.replace(f"cid:{cid}", data_url)
            msg_body = msg_body.replace(
                f'data-mce-src="cid:{cid}"', f'data-mce-src="{data_url}"'
            )

        ticket.description = Markup(msg_body)

        return ticket

    @api.depends("message_ids")
    def _compute_emails(self):
        for record in self:
            emails_ids = [
                msg_id.id
                for msg_id in record.message_ids
                if msg_id.message_type in ("email", "comment") and msg_id.body
            ]
            record.message_emails_ids = [(6, 0, emails_ids)]

    def mail_compose_message_action(self):
        """
        Open new communication sales according to requirements
        """
        if not self.description:
            self.description = Markup("")

        action = self.env.ref(
            "helpdesk_ticket_mail_message." "action_mail_compose_message_wizard"
        ).read()[0]
        response_tmpl = self.env.ref(
            "helpdesk_ticket_mail_message.created_response_ticket_template",
            raise_if_not_found=False,
        )
        reply_to = response_tmpl.reply_to if response_tmpl else False
        if not reply_to:
            reply_to = self.env["mail.message"]._get_message_email_from_for_reply(
                ticket=self
            )

        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "mass_mail",
                "default_template_id": response_tmpl.id if response_tmpl else False,
                "default_email_to": self.partner_email,
                "default_reply_to": reply_to,
                "default_subject": _("The Ticket %s", self.number),
                "default_body": self.description,
                "default_message_type_mail": "email_sent",
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "skip_onchange_template_id": True,
            }
        )
        action["context"] = ctx
        return action

    def mail_compose_message_action_note(self):
        """
        Open new communication sales according to requirements
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message." "action_mail_compose_message_wizard"
        ).read()[0]
        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": "comment",
                "default_is_log": True,
                "active_model": self._name,
                "active_id": self.id,
                "active_ids": [self.id],
                "default_subject": self.name,
                "default_body": Markup(""),
            }
        )
        action["context"] = ctx
        action["name"] = _("Create note")
        return action

    def _message_get_default_recipients(self):
        """
        Override for helpdesk tickets (as in crm.lead) to avoid the email composer
        to suggest addresses based on ticket partners, since it was causing duplicates
        for gmail accounts.
        """
        return {
            r.id: {
                "partner_ids": [],
                "email_to": ",".join(tools.email_normalize_all(r.partner_email))
                or r.partner_email,
                "email_cc": False,
            }
            for r in self.sudo()
        }

    def get_message_body_with_history(self):
        """
        Get the message body with history to include it in email templates.
        """
        self.ensure_one()

        history_parts = []
        for msg in self.message_emails_ids.sorted("date", reverse=True):
            history_parts.append(str(msg._get_message_body_for_reply()))

        return Markup("<br/>".join(history_parts))

    def _notify_get_reply_to(self, default=None):
        """
        Compute the reply-to address for tickets.

        Prefer the template's reply_to if available, then the team's default_email_from,
        then the team's alias (name@domain), then the ticket's company formatted email,
        and finally the provided default.
        """
        res = super()._notify_get_reply_to(default=default)

        # Check if there's a template with a reply_to value that should take precedence
        template_id = self.env.context.get("default_template_id")
        template_reply_to = None
        if template_id:
            template = self.env["mail.template"].browse(template_id)
            if template.exists() and template.reply_to:
                # Render the template reply_to for each ticket
                template_reply_to = template._render_field("reply_to", self.ids)

        for ticket in self:
            # If template has a reply_to value, prioritize it
            if template_reply_to and template_reply_to.get(ticket.id):
                res[ticket.id] = template_reply_to[ticket.id]
                continue

            # Fall back to custom helpdesk logic
            company = (
                getattr(ticket, "company_id", ticket.env.user.company_id)
                or ticket.env.company
            )
            reply_to = company.email_formatted or default

            team = ticket.team_id
            if team:
                if team.default_team_from_value:
                    reply_to = team.default_team_from_value
                else:
                    alias = team.alias_id
                    if alias and alias.alias_name and alias.alias_domain:
                        reply_to = f"{alias.alias_name}@{alias.alias_domain}"

            res[ticket.id] = reply_to

        return res
