from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, MainFundingSource, Methodology, NihrPriorityArea, Project, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode
from lbrc_flask.pytest.faker import BaseProvider, LookupProvider, FakeCreator


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
        MainFundingSource,
        MainFundingCategory,
        MainFundingDhscNihrFunding,
        MainFundingIndustry,
    ]


class ProjectFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(Project)

    def get(self, lookups_in_db=True, **kwargs):
        self.faker.add_provider(CoreDashLookupProvider)

        result = self.cls(
            title = kwargs.get('title') or self.faker.sentence(),
            summary = kwargs.get('summary') or self.faker.paragraph(),
            comments = kwargs.get('comments') or self.faker.paragraph(),

            local_rec_number = kwargs.get('local_rec_number') or self.faker.pystr(min_chars=8, max_chars=8),
            iras_number = kwargs.get('iras_number') or self.faker.pyint(),

            start_date = kwargs.get('start_date') or self.faker.date_object(),
            end_date = kwargs.get('end_date') or self.faker.date_object(),
            participants_recruited_to_centre_fy = kwargs.get('participants_recruited_to_centre_fy') or self.faker.pyint(),

            brc_funding = kwargs.get('brc_funding') or self.faker.pyint(),
            main_funding_brc_funding = kwargs.get('main_funding_brc_funding') or self.faker.pyint(),
            total_external_funding_award = kwargs.get('total_external_funding_award') or self.faker.pyint(),

            sensitive = kwargs.get('sensitive') or self.faker.pybool(),
            first_in_human = kwargs.get('first_in_human') or self.faker.pybool(),
            link_to_nihr_transactional_research_collaboration = kwargs.get('link_to_nihr_transactional_research_collaboration') or self.faker.pybool(),
            crn_rdn_portfolio_study = kwargs.get('crn_rdn_portfolio_study') or self.faker.pybool(),
            rec_approval_required = kwargs.get('rec_approval_required') or self.faker.pybool(),
            randomised_trial = kwargs.get('randomised_trial') or self.faker.pybool(),

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
            main_funding_source =  self.faker.main_funding_source().get_value_or_get(kwargs, 'main_funding_source', lookups_in_db),
            main_funding_category =  self.faker.main_funding_category().get_value_or_get(kwargs, 'main_funding_category', lookups_in_db),
            main_funding_dhsc_nihr_funding =  self.faker.main_funding_dhsc_nihr_funding().get_value_or_get(kwargs, 'main_funding_dhsc_nihr_funding', lookups_in_db),
            main_funding_industry =  self.faker.main_funding_industry().get_value_or_get(kwargs, 'main_funding_industry', lookups_in_db),
        )

        return result


class ProjectProvider(BaseProvider):
    def project(self):
        return ProjectFakeCreator()
