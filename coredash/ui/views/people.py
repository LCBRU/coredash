from coredash.model.people import JobTitle, ProfessionalBackground, ProfessionalBackgroundDetail
from coredash.model.project import UkcrcHealthCategory
from coredash.services.people import person_search_query
from .. import blueprint
from flask import render_template, request
from lbrc_flask.forms import SearchForm
from lbrc_flask.database import db
from lbrc_flask.lookups import LookupRepository
from wtforms import SelectField


class PersonSearchForm(SearchForm):
    job_title_id = SelectField('Job Title', coerce=int, render_kw={'class':' select2'})
    ukcrc_health_category_id = SelectField('UKCRC Health Category', coerce=int, render_kw={'class':' select2'})
    professional_background_id = SelectField('Professional Background', coerce=int, render_kw={'class':' select2'})
    professional_background_detail_id = SelectField('Professional Background Details', coerce=int, render_kw={'class':' select2'})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.job_title_id.choices = LookupRepository(JobTitle).get_select_choices()
        self.ukcrc_health_category_id.choices = LookupRepository(UkcrcHealthCategory).get_select_choices()
        self.professional_background_id.choices = LookupRepository(ProfessionalBackground).get_select_choices()
        self.professional_background_detail_id.choices = LookupRepository(ProfessionalBackgroundDetail).get_select_choices()


@blueprint.route("/people/")
def people_index():
    search_form = PersonSearchForm(formdata=request.args, search_placeholder='Search person details')

    q = person_search_query(search_form.data)

    return render_template(
        "ui/people/index.html",
        people=db.paginate(select=q),
        search_form=search_form,
    )
