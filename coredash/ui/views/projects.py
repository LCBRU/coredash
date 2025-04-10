from coredash.model.project import Project
from .. import blueprint
from flask import render_template, request
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from sqlalchemy import select
from lbrc_flask.security import User


@blueprint.route("/")
def index():
    search_form = SearchForm(formdata=request.args, search_placeholder='Search project details')

    q = select(Project)

    if search_form.search.data:
        q = q.filter(User.email.like(f'%{search_form.search.data}%'))

    projects = db.paginate(
        select=q,
        page=search_form.page.data,
        per_page=5,
        error_out=False,
    )

    return render_template(
        "ui/projects/index.html",
        projects=projects,
        search_form=search_form,
    )
