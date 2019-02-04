# -*- coding: utf-8 -*-


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class age(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR
    label = "Âge de l'individu (en années)"


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