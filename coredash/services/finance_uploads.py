from sqlalchemy import select
from lbrc_flask.database import db
from coredash.model.finance_upload import FinanceUpload, FinanceUploadMessage
from coredash.services.expenditure import expenditure_save
from coredash.services.external_fundings import external_funding_save
from coredash.services.projects import projects_save
from lbrc_flask.logging import log_exception


def finance_upload_search_query(search_data=None):
    q = select(FinanceUpload)

    search_data = search_data or []

    if x := search_data.get('search'):
        for word in x.split():
            q = q.where(FinanceUpload.filename.like(f"%{word}%"))

    return q


def finance_upload_save(data):
    u: FinanceUpload = FinanceUpload(filename=data['finance_file'].filename)

    u.local_filepath.parent.mkdir(parents=True, exist_ok=True)
    data['finance_file'].save(u.local_filepath)

    try:
        finance_upload_process(u)
    except Exception as e:
        log_exception(e)
        db.session.add(
            FinanceUploadMessage(
                finance_upload=u,
                type='Error',
                message='Unexpected error',
        ))
        u.status = FinanceUpload.STATUS__ERROR

    db.session.add(u)
    db.session.commit()


def finance_upload_process(finance_upload: FinanceUpload):
    finance_upload.validate()

    if not finance_upload.is_error:
        projects_save(finance_upload.project_data())
        external_funding_save(finance_upload.external_funding_data())
        expenditure_save(finance_upload.expenditure_data())
        finance_upload.status = FinanceUpload.STATUS__PROCESSED
