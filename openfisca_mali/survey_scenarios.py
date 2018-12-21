# -*- coding: utf-8 -*-


import os
import pandas as pd

from openfisca_core import periods

from openfisca_mali import CountryTaxBenefitSystem as MaliTaxBenefitSystem

from openfisca_survey_manager.scenarios import AbstractSurveyScenario


class MaliSurveyScenario(AbstractSurveyScenario):
    id_variable_by_entity_key = dict(
        famille = 'id_famille',
        )
    role_variable_by_entity_key = dict(
        famille = 'role_famille',
        )

    def __init__(self, tax_benefit_system = None, baseline_tax_benefit_system = None
            data = None, year = None):
        super(MaliSurveyScenario, self).__init__()
        if tax_benefit_system is None:
            tax_benefit_system = MaliTaxBenefitSystem()
        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            )

        if data is None:
            return

        stata_file_by_entity = data.get('stata_file_by_entity')

        if stata_file_by_entity is None:
            self.init_from_data(data = data)
            return

        assert year is not None
        variables_from_stata_files = []
        input_data_frame_by_entity_by_period = dict()
        input_data_frame_by_entity_by_period[periods.period(period)] = input_data_frame_by_entity = dict()
        for entity, file_path in stata_file_by_entity.items():
            assert os.path.exists(file_path)
            input_data_frame_by_entity[entity] = entity_data_frame = pd.read_stata(file_path)
            variables_from_stata_files.append(list(entity_data_frame.columns))

        self.used_as_input_variables = list(
            set(tax_benefit_system.variables.keys()).intersection(
                set(variables_from_stata_files)
                ))
        data = dict(input_data_frame_by_entity_by_period = input_data_frame_by_entity_by_period)
        self.init_from_data(data = data)
