from random import choice
from typing import Optional
from coredash.model.external_funding import ExternalFunding
from coredash.model.finance_upload import WORKSHEET_NAME_EXTERNAL_FUNDING, WORKSHEET_NAME_PROJECT_LIST, FinanceUpload, FinanceUpload_ExternalFunding_ColumnDefinition, FinanceUpload_ProjectList_ColumnDefinition
from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, Methodology, NihrPriorityArea, Project, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode
from lbrc_flask.pytest.faker import BaseProvider, LookupProvider, FakeCreator, FakeXlsxWorksheet, FakeXlsxFile
from tests import convert_external_funding_to_spreadsheet_data, convert_projects_to_spreadsheet_data


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


class ExternalFundingFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(ExternalFunding)

    def get(self, lookups_in_db=True, **kwargs):
        research_council = kwargs.get('research_council') or self.faker.pydecimal(right_digits=2, min_value=1_000, max_value=10_000_000)
        research_charity = kwargs.get('research_charity') or self.faker.pydecimal(right_digits=2, min_value=1_000, max_value=10_000_000)
        dhsc_nihr = kwargs.get('dhsc_nihr') or self.faker.pydecimal(right_digits=2, min_value=1_000, max_value=10_000_000)
        industry_collaborative = kwargs.get('industry_collaborative') or self.faker.pydecimal(right_digits=2, min_value=1_000, max_value=10_000_000)
        industry_contract = kwargs.get('industry_contract') or self.faker.pydecimal(right_digits=2, min_value=1_000, max_value=10_000_000)
        other_non_commercial = kwargs.get('other_non_commercial') or self.faker.pydecimal(right_digits=2, min_value=1_000, max_value=10_000_000)
        total = kwargs.get('total') or (research_council + research_charity + dhsc_nihr + industry_collaborative + industry_contract + other_non_commercial)

        result = self.cls(
            research_council=research_council,
            research_charity=research_charity,
            dhsc_nihr=dhsc_nihr,
            industry_collaborative=industry_collaborative,
            industry_contract=industry_contract,
            other_non_commercial=other_non_commercial,
            total=total,
        )

        return result


class CoreDashProvider(BaseProvider):
    def project(self):
        return ProjectFakeCreator()

    def external_data(self):
        return ExternalFundingFakeCreator()


class FinanceUploadFakeCreator(FakeCreator):
    def __init__(self):
        super().__init__(FinanceUpload)

    def get(self, **kwargs):
        return self.cls(
            filename = kwargs.get('filename') or self.faker.unique.file_name(extension='xslx'),
            status = kwargs.get('status') or choice(FinanceUpload.STATUS_NAMES),
        )

class FakeFinanceUpload():
    def __init__(self, filename: Optional[str] = None):
        self.filename: str = filename or 'test.xlsx'

        self.project_list_name: str = WORKSHEET_NAME_PROJECT_LIST
        self.project_list_headers: list[str] = FinanceUpload_ProjectList_ColumnDefinition().column_names
        self.project_list_header_row: int = 4
        self.project_list_data: list = []

        self.external_funding_name: str = WORKSHEET_NAME_EXTERNAL_FUNDING
        self.external_funding_headers: list[str] = FinanceUpload_ExternalFunding_ColumnDefinition().column_names
        self.external_funding_header_row: int = 4
        self.external_funding_data: list = []

    def get_project_list_worksheet(self):
        return FakeXlsxWorksheet(
            name=self.project_list_name,
            headers=self.project_list_headers,
            data=self.project_list_data,
            headers_on_row=self.project_list_header_row,
        )

    def get_external_funding_worksheet(self):
        return FakeXlsxWorksheet(
            name=self.external_funding_name,
            headers=self.external_funding_headers,
            data=self.external_funding_data,
            headers_on_row=self.external_funding_header_row,
        )

    def get_worksheets(self):
        return [
            self.get_project_list_worksheet(),
            self.get_external_funding_worksheet(),
        ]

    def get_workbook(self):
        return FakeXlsxFile(
            filename=self.filename,
            worksheets=self.get_worksheets(),
        )


class FinanceUploadProvider(BaseProvider):
    def finance_upload(self):
        return FinanceUploadFakeCreator()

    def finance_spreadsheet_project_data(self, rows=10):
        result = []

        for _ in range(rows):
            result.append(self.generator.project().get())
        
        return convert_projects_to_spreadsheet_data(result)

    def finance_spreadsheet_external_funding_data(self, rows=1):
        result = []

        for _ in range(rows):
            result.append(self.generator.external_data().get())
        
        return convert_external_funding_to_spreadsheet_data(result)

    def finance_spreadsheet(self, project_count: int = 10, external_funding_count: int = 1):
        file = FakeFinanceUpload()
        file.project_list_data = self.finance_spreadsheet_project_data(rows=project_count)
        file.external_funding_data = self.finance_spreadsheet_external_funding_data(rows=external_funding_count)

        return file
