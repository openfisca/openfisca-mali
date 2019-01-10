# -*- coding: utf-8 -*-


import os


from openfisca_mali.survey_scenarios import MaliSurveyScenario

from openfisca_mali.tests.data.fake_data_generator import data_directory


def test_load_stata_data():
    data = dict()
    data['stata_file_by_entity'] = dict(
        household = os.path.join(data_directory, 'household.dta'),
        person = os.path.join(data_directory, 'person.dta'),
        )
    year = 2017
    survey_scenario = MaliSurveyScenario(
        data = data,
        year = year,
        )
    assert survey_scenario.calculate_variable('impot_traitement_salaire', period = year) == [5000]


if __name__ == '__main__':
    test_load_stata_data()
