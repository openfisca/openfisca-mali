# -*- coding: utf-8 -*-

from openfisca_mali import CountryTaxBenefitSystem as MaliTaxBenefitSystem

from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_survey_manager.utils import stata_files_to_data_frames


class MaliSurveyScenario(AbstractSurveyScenario):

    def __init__(self, tax_benefit_system = None, baseline_tax_benefit_system = None,
            data = None, year = None):
        super(MaliSurveyScenario, self).__init__()
        if tax_benefit_system is None:
            tax_benefit_system = MaliTaxBenefitSystem()
        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            )

        assert year is not None
        self.year = year

        if data is None:
            return

        variables_from_stata_files = stata_files_to_data_frames(data, period = year)
        self.used_as_input_variables = list(
            set(tax_benefit_system.variables.keys()).intersection(
                set(variables_from_stata_files)
                )
            )
        self.init_from_data(data = data)
