# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=W0622,W0707,R1715,W0212,C0209
from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class StatusCheck(models.Model):
    _name = "status.check"
    _description = "Status Check"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    template_id = fields.Many2one(
        string="# Template",
        comodel_name="status.check.template",
    )
    template_detail_id = fields.Many2one(
        string="# Template Detail",
        comodel_name="status.check.template_detail",
    )
    status_check_method = fields.Selection(
        related="template_detail_id.status_check_item_id.status_check_method",
        readonly=True,
    )
    status_check_item_id = fields.Many2one(
        related="template_detail_id.status_check_item_id",
        readonly=True,
    )
    resolution_instruction = fields.Html(
        related="status_check_item_id.resolution_instruction",
    )

    # Bypass
    allowed_bypass_user_ids = fields.Many2many(
        string="Users Allowed To Bypass",
        comodel_name="res.users",
        compute="_compute_allowed_bypass_user_ids",
        store=False,
        compute_sudo=True,
    )
    date = fields.Datetime(
        string="Date",
        readonly=True,
    )
    bypass_ok = fields.Boolean(
        string="can Bypass?",
        compute="_compute_bypass_ok",
        compute_sudo=True,
    )
    bypass_user_id = fields.Many2one(
        string="Bypassed By",
        comodel_name="res.users",
        readonly=True,
    )

    def _compute_status_ok(self):
        for document in self:
            document.status_ok = False
            if document.bypass_user_id:
                document.status_ok = True
            else:
                result = document._evaluate_status_check()
                if result:
                    document.status_ok = result

    status_ok = fields.Boolean(
        string="Passed?",
        compute="_compute_status_ok",
        compute_sudo=True,
    )

    @api.depends(
        "template_detail_id",
    )
    def _compute_allowed_bypass_user_ids(self):
        for rec in self:
            list_user = []
            if rec.template_detail_id:
                selection_method = rec.template_detail_id.bypass_method
                user_ids = rec.template_detail_id.bypass_user_ids
                if user_ids:
                    list_user += user_ids.ids

                group_ids = rec.template_detail_id.bypass_group_ids
                if group_ids:
                    for group in group_ids:
                        list_user += group.users.ids

                if selection_method == "use_python":
                    python_code = rec.template_detail_id.python_code
                    result = rec._evaluate_python_code(python_code)
                    if result:
                        if "user" in result:
                            list_user += result["user"]
                        else:
                            msg_err = "No User defines on python code"
                            raise UserError(_(msg_err))
                rec.allowed_bypass_user_ids = list(set(list_user))

    @api.depends(
        "template_detail_id",
    )
    def _compute_bypass_ok(self):
        for record in self.sudo():
            result = False
            if (
                record.allowed_bypass_user_ids
                and record.env.user.id in record.allowed_bypass_user_ids.ids
            ):
                result = True
            record.bypass_ok = result

    def action_bypass_status_check(self):
        self.ensure_one()
        for record in self.sudo():
            record._bypass_status_check()

    def _bypass_status_check(self):
        self.ensure_one()
        if self.env.user.id in self.allowed_bypass_user_ids.ids:
            self.write(
                {
                    "date": fields.Datetime.now(),
                    "bypass_user_id": self.env.user.id,
                }
            )

    def action_reverse_bypass_status_check(self):
        for record in self.sudo():
            record._reverse_bypass_status_check()

    def _reverse_bypass_status_check(self):
        self.ensure_one()
        if self.env.user.id in self.allowed_bypass_user_ids.ids:
            self.write(
                {
                    "date": False,
                    "bypass_user_id": False,
                }
            )
            try:
                record = self._get_document()
                record.message_post(
                    body=_("The bypass has been reversed."),
                    message_type="comment",
                    subtype_id=self.env.ref("mail.mt_note").id,
                )
            except Exception as e:
                self.env["ir.logging"].create(
                    {
                        "name": "Error message_post",
                        "type": "server",
                        "dbname": self._cr.dbname,
                        "level": "ERROR",
                        "message": str(e),
                        "path": __name__,
                        "line": "0",
                        "func": "action_reverse_bypass_status_check",
                    }
                )

    def _get_document(self):
        document_id = self.res_id
        document_model = self.model

        object = self.env[document_model].browse([document_id])[0]
        return object

    def _get_localdict(self):
        return {
            "document": self._get_document(),
            "env": self.env,
            "time": tools.safe_eval.time,
            "datetime": tools.safe_eval.datetime,
            "dateutil": tools.safe_eval.dateutil,
        }

    def _evaluate_status_check(self):
        self.ensure_one()
        if not self.template_detail_id:
            return False
        try:
            method_name = "_evaluate_status_check_" + self.status_check_method
            result = getattr(self, method_name)()
        except Exception:
            record = self.env[self.model].browse(self.res_id)
            error_message = """
                Document: %s
                Context: Evaluating status check item
                Database ID: %s
                Problem: Python code error
                Solution: Check status check item ID %s
                """ % (
                record._description.lower(),
                record and record.id or "New Record",
                self.status_check_item_id.id,
            )
            raise UserError(_(error_message))
        return result

    def _evaluate_status_check_use_python(self):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(
                self.status_check_item_id.python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res
