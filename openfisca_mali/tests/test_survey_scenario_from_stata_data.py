import logging
import os


from openfisca_mali.input_data_builder import (
    data_is_available,
    create_data_from_stata,
    )

from openfisca_mali.survey_scenarios import MaliSurveyScenario
from openfisca_mali.tests.data.fake_data_generator import data_directory


log = logging.getLogger(__file__)


def test_load_fake_stata_data():
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
    assert all(survey_scenario.calculate_variable('impot_traitement_salaire', period = year) == [5000, 0])


def test_survey_scenario(create_dataframes = True):
    circleci = 'CIRCLECI' in os.environ
    if circleci or not data_is_available:
        return

    year = 2014
    data = create_data_from_stata(create_dataframes = create_dataframes)
    survey_scenario = MaliSurveyScenario(
        data = data,
        year = year,
        )
    df_by_entity = survey_scenario.create_data_frame_by_entity(
        variables = ['age', 'salaire', 'impot_traitement_salaire']
        )

    for entity, df in df_by_entity.items():
        assert not df.empty, "{} dataframe is empty".format(entity)
        log.debug(df)


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)
    test_survey_scenario()
    test_load_fake_stata_data()
