from flask_wtf.file import FileRequired

from coredash.model.finance_upload import FinanceUpload
from coredash.security import ROLENAME_FINANCE_UPLOADER
from coredash.services.finance_uploads import finance_upload_save, finance_upload_search_query
from .. import blueprint
from flask import render_template, request, url_for
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from lbrc_flask.forms import FlashingForm, FileField
from lbrc_flask.response import refresh_response
from flask_security.decorators import roles_accepted


class UploadForm(FlashingForm):
    finance_file = FileField(
        'Finance File',
        accept=['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel.sheet.macroEnabled.12'],
        validators=[FileRequired()],
    )


@blueprint.route("/finance_upload/")
@roles_accepted(ROLENAME_FINANCE_UPLOADER)
def finance_upload_index():
    search_form = SearchForm(formdata=request.args, search_placeholder='Search upload filenames')

    q = finance_upload_search_query(search_form.data)
    q = q.order_by(FinanceUpload.created_date.desc())

    finance_uploads = db.paginate(select=q)

    return render_template(
        "ui/finance_uploads/index.html",
        finance_uploads=finance_uploads,
        search_form=search_form,
    )


@blueprint.route("/finance_upload/upload", methods=['GET', 'POST'])
@roles_accepted(ROLENAME_FINANCE_UPLOADER)
def finance_upload_upload(id=None):
    form = UploadForm()
    title = f"Upload Sample File"

    if form.validate_on_submit():
        finance_upload_save(form.data)
        return refresh_response()

    return render_template(
        "lbrc/form_modal.html",
        title=title,
        form=form,
        url=url_for('ui.finance_upload_upload', id=id),
    )
