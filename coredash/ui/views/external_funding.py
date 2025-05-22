
from coredash.services.external_fundings import get_external_funding
from coredash.model.external_funding import ExternalFunding
from .. import blueprint
from flask import render_template


@blueprint.route("/external_funding")
def external_funding_index():
    return render_template(
        "ui/external_funding/index.html",
        external_funding=get_external_funding(),
    )
