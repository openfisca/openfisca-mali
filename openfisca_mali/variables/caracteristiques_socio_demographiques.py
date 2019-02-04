# -*- coding: utf-8 -*-


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)  # By default, if no value is set for a simulation,
    # we consider the people involved in a simulation to be born on the 1st of Jan 1970.
    entity = Person
    label = u"Date de naissance"
    definition_period = ETERNITY  # This variable cannot change over time.
    reference = u"https://en.wiktionary.org/wiki/birthdate"


class age(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = u"Âge de l'individu (en années)"

    # A person's age is computed according to its birth date.
    def formula(person, period, parameters):
        date_naissance = person('date_naissance', period)
        birth_year = date_naissance.astype('datetime64[Y]').astype(int) + 1970
        birth_month = date_naissance.astype('datetime64[M]').astype(int) % 12 + 1
        birth_day = (date_naissance - date_naissance.astype('datetime64[M]') + 1).astype(int)

        is_birthday_past = (
            (birth_month < period.start.month)
            + (birth_month == period.start.month) * (birth_day <= period.start.day)
            )
        # If the birthday is not passed this year, subtract one year
        return (period.start.year - birth_year) - where(is_birthday_past, 0, 1)


class marie(Variable):
    value_type = bool
    entity = Household
    definition_period = YEAR
    label = "Variable binaire indiquant si la personne de référence a un-e conjoint-e dans le ménage"

    def formula(household, period):
        marie = household.nb_persons(Household.CONJOINT)
        return marie


class nombre_enfants_a_charge(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Nombre d'enfants à charge de la personne de référence et de son/sa conjointe dans le ménage"

    def formula(household, period):
        nombre_enfants_a_charge = household.nb_persons(Household.ENFANT)
        if nombre_enfants_a_charge > 10:
            nombre_enfants_a_charge = 10
        return nombre_enfants_a_charge


class reductions_familiales(Variable):
    value_type = float
    default_value = 0
    entity = Household
    definition_period = YEAR
    label = "Réduction pour charge de famille en (%)"

    def formula(household, period):
        condition_pas_enfant = nombre_enfants_a_charge == 0
        return select(
            [
                not_(marie, 1) * condition_pas_enfant,
                marie * condition_pas_enfant,
                not_(marie, 1) * not_(condition_pas_enfant, 1),
                marie * not_(condition_pas_enfant, 1),
            ],

            [
                reductions_familiales,
                reductions_familiales + 0.1,
                reductions_familiales + (nombre_enfants_a_charge * 0.025),
                reductions_familiales + 0.1 + (nombre_enfants_a_charge * 0.025)
            ]
        )