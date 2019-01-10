# -*- coding: utf-8 -*-


import os
import pandas as pd
import pkg_resources


data_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_mali').location,
    'openfisca_mali',
    'tests',
    'data',
    )


def generate_mali_fake_stata_data():
    assert os.path.exists(data_directory), "{} is not a valid path".format(data_directory)
    person = pd.DataFrame()
    person['revenu_net_imposable'] = [430000]
    person['id'] = [0]
    person['household_id'] = [0]
    person['household_role'] = [0]
    person['household_legacy_role'] = [0]

    household = pd.DataFrame()
    household['household_id'] = [0]

    person.to_stata(os.path.join(data_directory, 'person.dta'))
    household.to_stata(os.path.join(data_directory, 'household.dta'))


if __name__ == '__main__':
    generate_mali_fake_stata_data()
