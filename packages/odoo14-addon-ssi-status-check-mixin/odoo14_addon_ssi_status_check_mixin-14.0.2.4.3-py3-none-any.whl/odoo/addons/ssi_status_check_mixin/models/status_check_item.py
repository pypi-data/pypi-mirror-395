# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class StatusCheckItem(models.Model):
    _name = "status.check.item"
    _description = "Status Check Item"
    _order = "id"

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void."""

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        ondelete="cascade",
        index=True,
        required=False,
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
    resolution_instruction = fields.Html(
        string="Resolution Instruction",
    )
    status_check_method = fields.Selection(
        string="Status Check Method",
        selection=[
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default=DEFAULT_PYTHON_CODE
        + "\n#  - result: Return result, the value is boolean.",
        copy=True,
    )
