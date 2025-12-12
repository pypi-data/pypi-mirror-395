from markupsafe import Markup
from odoo import api, models, fields, tools, _


class Message(models.Model):
    _inherit = "mail.message"

    color_row = fields.Char(_("Color Row"), default="#000000")
    color_background_row = fields.Char(_("Color Background Row"), default="#FFFFFF")
    date_subject = fields.Text(_("Date/Subject"), compute="_compute_date_subject")
    message_type_mail = fields.Selection(
        selection=[
            ("email_sent", _("Mail sent")),
            ("email_received", _("Email received")),
            ("note", _("Note")),
        ],
        string="Message type",
    )
    scheduled_date = fields.Datetime(
        string=_("Scheduled Date"),
        compute="_compute_scheduled_date",
        help="Scheduled date for the activity linked to this message",
    )
    reschedule_date = fields.Datetime(
        string=_("Reschedule Date"),
        help="New scheduled date to reschedule the email",
    )

    @api.depends("mail_ids", "mail_ids.scheduled_date")
    def _compute_scheduled_date(self):
        for message in self:
            future_mails = message.mapped("mail_ids").filtered(
                lambda m: m.scheduled_date
            )
            if future_mails:
                scheduled_date = min(future_mails.mapped("scheduled_date"))
                if scheduled_date and scheduled_date > fields.Datetime.now():
                    message.scheduled_date = scheduled_date
                else:
                    message.scheduled_date = False
            else:
                message.scheduled_date = False

    @api.depends("date", "subject")
    def _compute_date_subject(self):
        for message in self:
            message.date_subject = (
                f" {message.date.strftime('%Y-%m-%d %H:%M:%S')} \n"
                f" {message.subject}"
            )

    @api.model
    def create(self, values):
        """
        When creating a new message, color it depending of its type
        (sent, recieved, note) and update its ticket if it is related to one
        """
        if values.get("model") == "helpdesk.ticket" and values.get("res_id"):
            ticket = self.env["helpdesk.ticket"].browse(values.get("res_id"))
            if not ticket:
                return super(Message, self).create(values)

            if values.get("message_type") == "email":
                values["color_row"] = "#FFFFFF"
                if self._context.get(
                    "default_message_type_mail"
                ) == "email_sent" or self.env.user.company_id.email == values.get(
                    "email_from"
                ):
                    values["message_type_mail"] = "email_sent"
                    values["color_background_row"] = "#FF0000"
                else:
                    values["message_type_mail"] = "email_received"
                    values["color_background_row"] = "#000000"
            elif values.get("message_type") == "comment":
                values["message_type_mail"] = "note"
                values["color_background_row"] = "#23FF00"

        return super(Message, self).create(values)

    def action_cancel_scheduled_email(self):
        """Cancel the scheduled email(s) linked to this message"""
        self.unlink()
        return True

    def mail_compose_action(self):
        if self.message_type == "email":
            return self.mail_compose_message_action()
        elif self.message_type == "comment":
            return self.mail_compose_message_action_note()
        else:
            return False

    def _prepare_action_mail_compose_with_context(
        self, composition_mode, is_resend=False
    ):
        """
        Prepare action mail_compose_message for tickets with context,
        depending on the composition_mode and other parameters
        """
        if not self.res_id or not self.model == "helpdesk.ticket":
            return {}
        ticket = self.env["helpdesk.ticket"].browse(self.res_id)

        sender_address = self._get_message_email_from_for_reply(ticket)

        company = self.env.user.company_id or self.env.company
        if ticket and ticket.company_id:
            company = ticket.company_id

        response_tmpl = company.helpdesk_forward_to_template_id if is_resend else company.helpdesk_reply_to_template_id

        ctx = self.env.context.copy() or {}
        ctx.update(
            {
                "default_composition_mode": composition_mode,
                "default_email_from": sender_address,
                "default_email_to": self.email_from,
                "default_no_atuto_thread": True,
                "default_reply_to": sender_address,
                "default_parent_id": self.id,
                "default_body": self._get_message_body_for_reply(),
                "default_template_id": response_tmpl.id if response_tmpl else False,
                "active_model": self.model,
                "active_id": self.res_id,
                "active_ids": [self.res_id],
                "default_subject": self._get_message_subject_for_reply(
                    is_resend, ticket.number
                ),
                "default_message_type_mail": "email_sent",
                "default_is_log": (composition_mode == "comment"),
                "mail_message_id": self.id,
                "skip_onchange_template_id": True,
            }
        )

        action = self.env.ref(
            "helpdesk_ticket_mail_message.action_mail_compose_message_wizard"
        ).read()[0]
        action.update(
            {
                "src_model": "helpdesk.ticket",
                "context": ctx,
            }
        )

        return action

    def mail_compose_message_action(self):
        """
        Open new communication to send mail
        """
        return self._prepare_action_mail_compose_with_context("mass_mail")

    def mail_compose_message_action_all(self):
        """
        Open new communication to send mail with CC
        """
        action = self._prepare_action_mail_compose_with_context("mass_mail")

        action["context"].update(
            {"default_email_cc": self._get_message_email_cc_for_reply_all(action)}
        )
        return action

    def mail_compose_message_action_resend(self):
        """
        Open new communication to reply
        """
        return self._prepare_action_mail_compose_with_context(
            "mass_mail", is_resend=True
        )

    def mail_compose_message_action_note(self):
        """
        Open new communication to create a note
        """
        res = self._prepare_action_mail_compose_with_context("comment")
        res["context"].update({"default_body": Markup("")})
        res["name"] = _("Create note")

        return res

    def mail_compose_message_action_readonly(self):
        """
        Open existing email message in a form view for reading
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message.helpdesk_mail_message_action_readonly"
        ).read()[0]
        action["res_id"] = self.id

        return action

    def mail_compose_message_action_reschedule(self):
        """
        Open new communication to reschedule email. This won't open a wizard
        but a form view of the mail.message to set the new reschedule date.
        """
        # Set the reschedule_date to the current scheduled_date value
        if self.scheduled_date:
            self.reschedule_date = self.scheduled_date

        action = self.env.ref(
            "helpdesk_ticket_mail_message.helpdesk_mail_message_reschedule_action"
        ).read()[0]
        action["res_id"] = self.id

        return action

    def save_rescheduled_email(self):
        """
        Save the rescheduled date to the linked mail.mail records
        """
        for message in self:
            for mail in message.mapped("mail_ids"):
                mail.write(
                    {
                        "scheduled_date": message.reschedule_date,
                        "body_html": message.body,
                        "email_cc": message.email_cc,
                        "email_to": message.email_to,
                        "subject": message.subject,
                    }
                )

        return {"type": "ir.actions.client", "tag": "reload"}

    def mail_compose_message_action_note_open(self):
        """
        Open existing note message in a form view for editing
        """
        action = self.env.ref(
            "helpdesk_ticket_mail_message.helpdesk_mail_message_note_open_action"
        ).read()[0]
        action["res_id"] = self.id

        return action

    def save_edited_note(self):
        """
        Save the edited note message
        """
        for message in self:
            message.write({"body": message.body})

        return {"type": "ir.actions.client", "tag": "reload"}

    def _get_message_body_for_reply(self):
        email_from = tools.email_normalize(self.email_from) or self.email_from
        email_to = ", ".join(set(tools.email_normalize_all(self.email_to)))
        email_cc = ", ".join(set(tools.email_normalize_all(self.email_cc)))

        return Markup(
            _(
                "<hr><blockquote>"
                "<p><b>From:</b> {email_from}</p>"
                "<p><b>Sent at:</b> {date}</p>"
                "<p><b>To:</b> {email_to}</p>"
                "<p><b>CC:</b> {email_cc}</p>"
                "<p><b>Subject:</b> {subject}</p>"
                "{body}"
                "</blockquote>"
            ).format(
                email_from=email_from,
                date=self.date,
                email_to=email_to or (self.email_to or ""),
                email_cc=email_cc or (self.email_cc or ""),
                subject=self.subject,
                body=self.body,
            )
        ).unescape()

    def _get_message_subject_for_reply(self, is_resend, ticket_number=None):
        if not self.subject:
            return ""

        refwd_suffix = _("Fwd:") if is_resend else _("Re:")
        ticket_number = f"[{ticket_number}]" if ticket_number else ""
        return (
            self.subject
            if refwd_suffix in self.subject
            else f"{refwd_suffix}{ticket_number} {self.subject}"
        )

    def _get_message_email_from_for_reply(self, ticket=None):
        """
        Get email_from for reply for ticket messages.
        The priority is:
        - Team default email_from
        - Team alias email
        - Ticket's company email
        - User's company email
        - User email
        """
        # Default fallback is the user's company email or user email
        fallback = (
            self.env.user.company_id.email_formatted
            or self.env.user.email_formatted
            or ""
        )
        if not ticket:
            return fallback

        # Ticket's company email is a preferred fallback
        if ticket.company_id:
            fallback = ticket.company_id.email_formatted or fallback

        # Try with team settings
        if not ticket.team_id:
            return fallback

        if ticket.team_id.default_team_from_value:
            return ticket.team_id.default_team_from_value

        team_alias_id = ticket.team_id.alias_id
        if team_alias_id and team_alias_id.alias_domain and team_alias_id.alias_name:
            return f"{team_alias_id.alias_name}@{team_alias_id.alias_domain}"

        return fallback

    def _get_message_email_cc_for_reply_all(self, action={}):
        """
        Get the email CC for the reply all message
        """
        ctx = action.get("context", {})

        ignore_addresses = set(
            tools.email_normalize_all(ctx.get("default_email_from", ""))
            + tools.email_normalize_all(self.email_from)
            + tools.email_normalize_all(self.delivered_to or "")
        )
        if self.model == "helpdesk.ticket" and self.res_id:
            ticket = self.env[self.model].browse(self.res_id)
            if ticket:
                ignore_addresses.update(
                    tools.email_normalize_all(ticket.original_email_to or "")
                )
                if ticket.team_id and ticket.team_id.alias_id:
                    team_alias = ticket.team_id.alias_id
                    if team_alias.alias_domain and team_alias.alias_name:
                        ignore_addresses.add(
                            tools.email_normalize(
                                f"{team_alias.alias_name}@{team_alias.alias_domain}"
                            )
                        )
                if ticket.team_id and ticket.team_id.default_team_from_value:
                    ignore_addresses.add(
                        tools.email_normalize(ticket.team_id.default_team_from_value)
                    )

        for server in self.env["fetchmail.server"].sudo().search([]):
            if server.user and "@" in str(server.user):
                ignore_addresses.add(tools.email_normalize(server.user))
            elif server.user and server.server:
                domain_split = server.server.split(".")
                if len(domain_split) > 2:
                    domain = ".".join(domain_split[1:])
                    ignore_addresses.add(
                        tools.email_normalize(f"{server.user}@{domain}")
                    )
                elif len(domain_split) == 2:
                    ignore_addresses.add(
                        tools.email_normalize(f"{server.user}@{server.server}")
                    )

        email_cc = set(
            tools.email_normalize_all(self.email_cc)
            + tools.email_normalize_all(self.email_to)
        )
        email_cc -= ignore_addresses

        return ",".join(sorted(email_cc)) if email_cc else ""
