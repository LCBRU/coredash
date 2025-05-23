
from coredash.services.dashboard import get_frontpage
from .. import blueprint
from flask import render_template


@blueprint.route("/dashboard/frontpage/")
def dashboard_frontpage():
    return render_template(
        "ui/dashboard/frontpage.html",
        frontpage=get_frontpage(),
    )
