from random import choice
from coredash.model.finance_upload import FinanceUpload
from coredash.model.lookups import Theme
from coredash.model.people import JobTitle, Person, ProfessionalBackground, ProfessionalBackgroundDetail
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, Methodology, NihrPriorityArea, Project, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode
from lbrc_flask.pytest.faker import BaseProvider, LookupProvider, FakeCreator
from tests import convert_projects_to_spreadsheet_data


class CoreDashLookupProvider(LookupProvider):
    LOOKUPS = [
        Theme,
        ProjectStatus,
        UkcrcHealthCategory,
        NihrPriorityArea,
        UkcrcResearchActivityCode,
        RacsSubCategory,
        ResearchType,
        Methodology,
        ExpectedImpact,
        TrialPhase,
        MainFundingCategory,
        MainFundingDhscNihrFunding,
        MainFundingIndustry,
        JobTitle,
        ProfessionalBackground,
        ProfessionalBackgroundDetail,
    ]


class ProjectFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(Project)
        self.previous_iras_number = set()

    def get(self, lookups_in_db=True, **kwargs):
        self.faker.add_provider(CoreDashLookupProvider)

        sensitive = kwargs.get('sensitive')
        if sensitive is None:
            sensitive = self.faker.pybool()
        
        first_in_human = kwargs.get('first_in_human')
        if first_in_human is None:
            first_in_human = self.faker.pybool()
        
        link_to_nihr_transactional_research_collaboration = kwargs.get('link_to_nihr_transactional_research_collaboration')
        if link_to_nihr_transactional_research_collaboration is None:
            link_to_nihr_transactional_research_collaboration = self.faker.pybool()
        
        crn_rdn_portfolio_study = kwargs.get('crn_rdn_portfolio_study')
        if crn_rdn_portfolio_study is None:
            crn_rdn_portfolio_study = self.faker.pybool()
        
        rec_approval_required = kwargs.get('rec_approval_required')
        if rec_approval_required is None:
            rec_approval_required = self.faker.pybool()
        
        randomised_trial = kwargs.get('randomised_trial')
        if randomised_trial is None:
            randomised_trial = self.faker.pybool()
        
        result = self.cls(
            title = kwargs.get('title') or self.faker.sentence(),
            summary = kwargs.get('summary') or self.faker.paragraph(),
            comments = kwargs.get('comments') or self.faker.paragraph(),

            local_rec_number = kwargs.get('local_rec_number') or self.faker.unique.pystr(min_chars=8, max_chars=8),
            iras_number = kwargs.get('iras_number') or self.faker.unique.pystr(min_chars=8, max_chars=8),
            cpms_id = kwargs.get('cpms_id') or self.faker.unique.pystr(min_chars=8, max_chars=8),
            main_funding_source = kwargs.get('main_funding_source') or self.faker.unique.pystr(min_chars=50, max_chars=50),

            start_date = kwargs.get('start_date') or self.faker.date_object(),
            end_date = kwargs.get('end_date') or self.faker.date_object(),
            participants_recruited_to_centre_fy = kwargs.get('participants_recruited_to_centre_fy') or self.faker.pyint(),

            brc_funding = kwargs.get('brc_funding') or self.faker.pyint(),
            main_funding_brc_funding = kwargs.get('main_funding_brc_funding') or self.faker.pyint(),
            total_external_funding_award = kwargs.get('total_external_funding_award') or self.faker.pyint(),

            sensitive = sensitive,
            first_in_human = first_in_human,
            link_to_nihr_transactional_research_collaboration = link_to_nihr_transactional_research_collaboration,
            crn_rdn_portfolio_study = crn_rdn_portfolio_study,
            rec_approval_required = rec_approval_required,
            randomised_trial = randomised_trial,

            project_status =  self.faker.project_status().get_value_or_get(kwargs, 'project_status', lookups_in_db),
            theme =  self.faker.theme().get_value_or_get(kwargs, 'theme', lookups_in_db),
            ukcrc_health_category =  self.faker.ukcrc_health_category().get_value_or_get(kwargs, 'ukcrc_health_category', lookups_in_db),
            nihr_priority_area =  self.faker.nihr_priority_area().get_value_or_get(kwargs, 'nihr_priority_area', lookups_in_db),
            ukcrc_research_activity_code =  self.faker.ukcrc_research_activity_code().get_value_or_get(kwargs, 'ukcrc_research_activity_code', lookups_in_db),
            racs_sub_category =  self.faker.racs_sub_category().get_value_or_get(kwargs, 'racs_sub_category', lookups_in_db),
            research_type =  self.faker.research_type().get_value_or_get(kwargs, 'research_type', lookups_in_db),
            methodology =  self.faker.methodology().get_value_or_get(kwargs, 'methodology', lookups_in_db),
            expected_impact =  self.faker.expected_impact().get_value_or_get(kwargs, 'expected_impact', lookups_in_db),
            trial_phase =  self.faker.trial_phase().get_value_or_get(kwargs, 'trial_phase', lookups_in_db),
            main_funding_category =  self.faker.main_funding_category().get_value_or_get(kwargs, 'main_funding_category', lookups_in_db),
            main_funding_dhsc_nihr_funding =  self.faker.main_funding_dhsc_nihr_funding().get_value_or_get(kwargs, 'main_funding_dhsc_nihr_funding', lookups_in_db),
            main_funding_industry =  self.faker.main_funding_industry().get_value_or_get(kwargs, 'main_funding_industry', lookups_in_db),
        )

        return result


class ProjectProvider(BaseProvider):
    def project(self):
        return ProjectFakeCreator()


class PersonFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(Person)
        self.previous_iras_number = set()

    def get(self, lookups_in_db=True, **kwargs):
        self.faker.add_provider(CoreDashLookupProvider)

        result = self.cls(
            first_name = kwargs.get('first_name') or self.faker.first_name(),
            last_name = kwargs.get('last_name') or self.faker.last_name(),
            comments = kwargs.get('comments') or self.faker.paragraph(),

            orcid = kwargs.get('orcid') or self.faker.unique.orcid(),

            full_time_equivalent = kwargs.get('full_time_equivalent') or choice([0.2, 0.4, 0.4, 0.5, 0.6, 0.8, 1.0]),

            job_title =  self.faker.job_title().get_value_or_get(kwargs, 'job_title', lookups_in_db),
            ukcrc_health_category =  self.faker.ukcrc_health_category().get_value_or_get(kwargs, 'ukcrc_health_category', lookups_in_db),
            professional_background =  self.faker.professional_background().get_value_or_get(kwargs, 'professional_background', lookups_in_db),
            professional_background_detail = self.faker.professional_background_detail().get_value_or_get(kwargs, 'professional_background_detail', lookups_in_db),
        )

        return result


class PersonProvider(BaseProvider):
    def person(self):
        return PersonFakeCreator()


class FinanceUploadFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(FinanceUpload)

    def get(self, **kwargs):
        return self.cls(
            filename = kwargs.get('filename') or self.faker.unique.file_name(extension='xslx'),
            status = kwargs.get('status') or choice(FinanceUpload.STATUS_NAMES),
        )


class FinanceUploadProvider(BaseProvider):
    def finance_upload(self):
        return FinanceUploadFakeCreator()

    def finance_spreadsheet_data(self, rows=10):
        result = []

        for _ in range(rows):
            result.append(self.generator.project().get())
        
        return convert_projects_to_spreadsheet_data(result)


