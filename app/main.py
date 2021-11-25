"""Invoice creator app."""
import datetime
import logging
import os
from typing import Any, Dict, Optional

import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape

from app.config.service import Config
from app.jira.service import JiraService
from app.tools.date import working_days_percent

_LOG = logging.getLogger(__name__)

env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())


class Runner:
    """Main app runner."""

    INVOICE_TEMPLATE = "invoice.html.j2"
    OUTPUT_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "invoices"
    )

    def __init__(self, config_file: str) -> None:
        """
        :param config_file: path to JSON config
        """
        self._config = Config.from_file(config_file)
        self._render_params: Optional[Dict[str, Any]] = None

    def run(self) -> None:
        """Create PDf invoice."""
        html = self._render_invoice(self.render_params)
        saved_file = self._save_pdf(html)
        _LOG.info("Saved to %s" % saved_file)

    def _render_invoice(self, params: Dict[str, Any]) -> str:
        """Get invoice HTML.

        :param params: substitutes for template
        :returns: HTML text
        """
        template = env.get_template(self.INVOICE_TEMPLATE)
        html = template.render(**params)
        return html

    def _save_pdf(self, html_text: str) -> str:
        """Save PDF to invoices dir.

        :param html_text: HTML string
        :returns: path to saved file
        """
        if not os.path.exists(self.OUTPUT_DIR):
            os.mkdir(self.OUTPUT_DIR)
        f_date = datetime.date.today().strftime("%Y-%m-%d")
        f_name = self.render_params["from"]["name"]
        f_invoice = self.render_params["invoice"]["number"]
        filename = os.path.join(
            self.OUTPUT_DIR, "%s - %s - %s.pdf" % (f_date, f_name, f_invoice)
        )
        pdfkit.from_string(html_text, filename)
        with open("%s.html" % filename, "w") as f:
            f.write(html_text)
        return filename

    @property
    def render_params(self) -> Dict[str, Any]:
        """Build render params from config"""
        if self._render_params is not None:
            return self._render_params
        render_params: Dict[str, Any] = {}
        render_params["from"] = self._config.me
        render_params["to"] = self._config.company
        render_params["agreement"] = self._config.agreement
        render_params["currency"] = self._config.pay.currency
        render_params["totals"] = {
            "sub": self._config.pay.total
            * 1.0
            * working_days_percent(
                start=datetime.datetime.strptime(
                    self._config.start_date, "%b %d %Y"
                ).date()
            )
            / 100
        }
        render_params["totals"]["tax"] = self._config.pay.tax * 100
        render_params["totals"]["total"] = render_params["totals"]["sub"] * (
            1 - self._config.pay.tax
        )
        # Get tasks.
        jira = JiraService(self._config.jira.url, self._config.jira.token)
        success, tasks = jira.find(self._config.jira.user, period="month")
        if not success:
            raise ValueError("Not all tasks were taken")
        # Save tasks.
        render_params["tasks"] = [{"description": task, "amount": 0} for task in tasks]
        amounts = [round(render_params["totals"]["sub"] / len(tasks), 2)] * len(tasks)
        amounts[0] += round(render_params["totals"]["sub"] - sum(amounts), 2)
        for i, item in enumerate(render_params["tasks"]):
            item["amount"] = amounts[i]
        # Get invoice info.
        today = datetime.date.today()
        render_params["invoice"] = {}
        render_params["invoice"]["date"] = today.strftime("%d %b %Y")
        render_params["invoice"]["period"] = today.strftime("%B %Y")
        render_params["invoice"]["number"] = "INV%s" % today.strftime("%Y%m")
        # Return params.
        self._render_params = render_params
        return self._render_params
