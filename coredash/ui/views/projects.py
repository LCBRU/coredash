from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, Methodology, NihrPriorityArea, Project, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode
from coredash.security import ROLENAME_PROJECT_EDITOR
from coredash.services.projects import project_populate, project_search_query
from .. import blueprint
from flask import render_template, request, url_for
from lbrc_flask.forms import SearchForm, YesNoSelectField, FlashingForm
from lbrc_flask.database import db
from lbrc_flask.lookups import LookupRepository
from lbrc_flask.response import refresh_response
from wtforms import BooleanField, DateField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import Length, DataRequired
from flask_security.decorators import roles_accepted


class ProjectSearchForm(SearchForm):
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    sensitive = YesNoSelectField('Sensitive Data')
    first_in_human = YesNoSelectField('First in Human')
    link_to_nihr_transactional_research_collaboration = YesNoSelectField('Link to NIHR Translational Research Collaboration')
    crn_rdn_portfolio_study = YesNoSelectField('CRN/RDN Portfolio Study')
    rec_approval_required = YesNoSelectField('REC Approval Required')
    randomised_trial = YesNoSelectField('Randomised Trial')
    project_status_id = SelectField('Status', coerce=int, render_kw={'class':' select2'})
    theme_id = SelectField('Theme', coerce=int, render_kw={'class':' select2'})
    ukcrc_health_category_id = SelectField('UKCRC Health Category', coerce=int, render_kw={'class':' select2'})
    nihr_priority_area_id = SelectField('NIHR priority Area', coerce=int, render_kw={'class':' select2'})
    ukcrc_research_activity_code_id = SelectField('UKCRC Research Activity Code', coerce=int, render_kw={'class':' select2'})
    racs_sub_category_id = SelectField('RACS sub-categories', coerce=int, render_kw={'class':' select2'})
    research_type_id = SelectField('Research Type', coerce=int, render_kw={'class':' select2'})
    methodology_id = SelectField('Methodology', coerce=int, render_kw={'class':' select2'})
    expected_impact_id = SelectField('Expected Impact', coerce=int, render_kw={'class':' select2'})
    trial_phase_id = SelectField('Trial Phase', coerce=int, render_kw={'class':' select2'})
    main_funding_category_id = SelectField('Main Funding Category', coerce=int, render_kw={'class':' select2'})
    main_funding_dhsc_nihr_funding_id = SelectField('Main Funding - DHSC/NIHR Funding', coerce=int, render_kw={'class':' select2'})
    main_funding_industry_id = SelectField('Main Funding - Industry Collaborative or Industry Contract Funding', coerce=int, render_kw={'class':' select2'})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.project_status_id.choices = LookupRepository(ProjectStatus).get_select_choices()
        self.theme_id.choices = LookupRepository(Theme).get_select_choices()
        self.ukcrc_health_category_id.choices = LookupRepository(UkcrcHealthCategory).get_select_choices()
        self.nihr_priority_area_id.choices = LookupRepository(NihrPriorityArea).get_select_choices()
        self.ukcrc_research_activity_code_id.choices = LookupRepository(UkcrcResearchActivityCode).get_select_choices()
        self.racs_sub_category_id.choices = LookupRepository(RacsSubCategory).get_select_choices()
        self.research_type_id.choices = LookupRepository(ResearchType).get_select_choices()
        self.methodology_id.choices = LookupRepository(Methodology).get_select_choices()
        self.expected_impact_id.choices = LookupRepository(ExpectedImpact).get_select_choices()
        self.trial_phase_id.choices = LookupRepository(TrialPhase).get_select_choices()
        self.main_funding_category_id.choices = LookupRepository(MainFundingCategory).get_select_choices()
        self.main_funding_dhsc_nihr_funding_id.choices = LookupRepository(MainFundingDhscNihrFunding).get_select_choices()
        self.main_funding_industry_id.choices = LookupRepository(MainFundingIndustry).get_select_choices()


class EditProjectForm(FlashingForm):
    title = StringField('Title', validators=[Length(max=500), DataRequired()])
    local_rec_number = StringField('Local REC Number', validators=[Length(max=50), DataRequired()])
    sensitive = BooleanField('Is this project sensitive?')
    summary = TextAreaField('Summary', validators=[DataRequired()])
    iras_number = StringField('IRAS Number', validators=[Length(max=50), DataRequired()])
    start_date = DateField('Actual Start Date', validators=[DataRequired()])
    end_date = DateField('End Date')
    crn_rdn_portfolio_study = BooleanField('CRN/RDN Portfolio study')
    cpms_id = StringField('CRN/RDN CPMS ID', validators=[Length(max=50), DataRequired()])
    main_funding_source = StringField('Main Funding Source', validators=[Length(max=500), DataRequired()])
    project_status_id = SelectField('Status', coerce=int, render_kw={'class':' select2'})
    theme_id = SelectField('Theme', coerce=int, render_kw={'class':' select2'})
    ukcrc_health_category_id = SelectField('UKCRC Health Category', coerce=int, render_kw={'class':' select2'})
    nihr_priority_area_id = SelectField('NIHR priority Areas / Fields of Research', coerce=int, render_kw={'class':' select2'})
    rec_approval_required = BooleanField('REC Approval Required')
    ukcrc_research_activity_code_id = SelectField('UKCRC Research Activity Code', coerce=int, render_kw={'class':' select2'})
    racs_sub_category_id = SelectField('RACS Sub-Categories', coerce=int, render_kw={'class':' select2'})
    research_type_id = SelectField('Research Type', coerce=int, render_kw={'class':' select2'})
    methodology_id = SelectField('Methodology', coerce=int, render_kw={'class':' select2'})
    expected_impact_id = SelectField('Expected Impact', coerce=int, render_kw={'class':' select2'})
    randomised_trial = BooleanField('Randomised Trial')
    trial_phase_id = SelectField('Trial Phase', coerce=int, render_kw={'class':' select2'})
    participants_recruited_to_centre_fy = IntegerField('Participants Recruited to Centre FY', validators=[DataRequired()])
    brc_funding = IntegerField('BRC funding', validators=[DataRequired()])
    main_funding_category_id = SelectField('Main Funding Category', coerce=int, render_kw={'class':' select2'})
    main_funding_brc_funding = IntegerField('Main Funding - BRC Funding', validators=[DataRequired()])
    main_funding_dhsc_nihr_funding_id = SelectField('Main Funding - DHSC/NIHR Funding', coerce=int, render_kw={'class':' select2'})
    main_funding_industry_id = SelectField('Main Funding - Industry Collaborative or Industry Contract Funding', coerce=int, render_kw={'class':' select2'})
    total_external_funding_award = IntegerField('Total External Funding Awarded', validators=[DataRequired()])
    first_in_human = BooleanField('First in Human Project')
    link_to_nihr_transactional_research_collaboration = BooleanField('Link to NIHR Translational Research Collaboration')
    comments = TextAreaField('Comments')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.project_status_id.choices = LookupRepository(ProjectStatus).get_select_choices()
        self.theme_id.choices = LookupRepository(Theme).get_select_choices()
        self.ukcrc_health_category_id.choices = LookupRepository(UkcrcHealthCategory).get_select_choices()
        self.nihr_priority_area_id.choices = LookupRepository(NihrPriorityArea).get_select_choices()
        self.ukcrc_research_activity_code_id.choices = LookupRepository(UkcrcResearchActivityCode).get_select_choices()
        self.racs_sub_category_id.choices = LookupRepository(RacsSubCategory).get_select_choices()
        self.research_type_id.choices = LookupRepository(ResearchType).get_select_choices()
        self.methodology_id.choices = LookupRepository(Methodology).get_select_choices()
        self.expected_impact_id.choices = LookupRepository(ExpectedImpact).get_select_choices()
        self.trial_phase_id.choices = LookupRepository(TrialPhase).get_select_choices()
        self.main_funding_category_id.choices = LookupRepository(MainFundingCategory).get_select_choices()
        self.main_funding_dhsc_nihr_funding_id.choices = LookupRepository(MainFundingDhscNihrFunding).get_select_choices()
        self.main_funding_industry_id.choices = LookupRepository(MainFundingIndustry).get_select_choices()


@blueprint.route("/")
def index():
    search_form = ProjectSearchForm(formdata=request.args, search_placeholder='Search project details')

    q = project_search_query(search_form.data)

    projects = db.paginate(select=q)

    return render_template(
        "ui/projects/index.html",
        projects=projects,
        search_form=search_form,
    )


@blueprint.route("/project/add/", methods=['GET', 'POST'])
@blueprint.route("/project/edit/<int:id>", methods=['GET', 'POST'])
@roles_accepted(ROLENAME_PROJECT_EDITOR)
def project_add(id=None):
    if id:
        object = db.get_or_404(Project, id)
        form = EditProjectForm(obj=object)
        title = f"Edit Project #{object.title}"
    else:
        object = Project()
        form = EditProjectForm()
        title = f"Add Project"

    if form.validate_on_submit():
        project_populate(object, form.data)
        db.session.add(object)
        db.session.commit()
        return refresh_response()

    return render_template(
        "lbrc/form_modal.html",
        title=title,
        form=form,
        url=url_for('ui.project_add', id=id),
    )


