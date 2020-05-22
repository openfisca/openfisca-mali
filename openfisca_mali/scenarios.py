import logging


log = logging.getLogger(__name__)


def init_single_entity(scenario, axes = None, enfants = None, household = None, parent1 = None, parent2 = None, period = None):
    if enfants is None:
        enfants = []
    assert parent1 is not None

    households = {}
    persons = {}

    count_so_far = 0
    for nth in range(0, 1):
        household_nth = household.copy() if household is not None else {}
        group = [parent1, parent2] + (enfants or [])
        for index, person in enumerate(group):
            if person is None:
                continue
            id = person.get('id')
            if id is None:
                person = person.copy()
                id = 'ind{}'.format(index + count_so_far)
            persons[id] = person
            if index <= 1:
                if index == 0:
                    household_nth['personne_de_reference'] = id
                else:
                    household_nth['conjoint'] = id
            else:
                household_nth.setdefault('enfants', []).append(id)

        count_so_far += len(group)
        households["m{}".format(nth)] = household_nth

    test_data = {
        'period': period,
        'households': households,
        'persons': persons
        }
    if axes:
        test_data['axes'] = axes
    scenario.init_from_dict(test_data)
    return scenario
