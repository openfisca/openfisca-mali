# -*- coding: utf-8 -*-


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class impot_traitement_salaire(Variable):
    value_type = float
    entity = Person
    label = u"Impôt pour les traitements et les salaires"
    definition_period = YEAR

    def formula(person, period):
        impot_brut = person('impot_brut', period)
        impot_traitement_salaire = person('impot_brut', period) - person('reductions_familiales', period)
        return impot_traitement_salaire


class reductions_familiales(Variable):
    value_type = float
    default_value = 0
    entity = Person
    definition_period = YEAR
    label = "Réduction pour charge de famille"

    def formula(person, period, parameters):
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


class impot_brut(Variable):
    value_type = float
    entity = Person
    label = u"Impôt brut"
    definition_period = YEAR

    def formula(person, period, parameters):
        revenu_net_imposable = person('revenu_net_imposable', period)
        bareme = parameters(period).prelevements_obligatoires.impots_directs.impot_traitement_salaire
        impot_brut = bareme.calc(revenu_net_imposable)
        return impot_brut


class revenu_net_imposable(Variable):
    value_type = float
    entity = Person
    label = u"Revenu net imposable"
    definition_period = YEAR

    def formula(person, period):
        salaire = person('salaire', period)
        revenu_net_imposable = person('salaire', period)
        return revenu_net_imposable


class nombre_enfants_a_charge(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Nombre d'enfants à charge de la personne de référence et de son/sa conjointe dans le ménage"

    def formula(household, period):
        nombre_enfants_a_charge = household.nb_persons(Household.ENFANT)
        return min_(10, nombre_enfants_a_charge)
