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
        return nombre_enfants_a_charge