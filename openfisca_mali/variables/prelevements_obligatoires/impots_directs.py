# -*- coding: utf-8 -*-


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class impot_traitement_salaire(Variable):
    value_type = float
    entity = Person
    label = u"Impôt pour les traitements et les salaires"
    definition_period = YEAR

    def formula(person, period, parameters):
        impot_brut = person('impot_brut', period)
        impot_traitement_salaire = impot_brut * person.household('reductions_familiales', period)
        return impot_traitement_salaire


class impot_brut(Variable):
    value_type = float
    entity = Person
    label = u"Impôt brut"
    definition_period = YEAR

    def formula(person, period, parameters):
        salaire = person('salaire', period)
        bareme = parameters(period).prelevements_obligatoires.impots_directs.impot_traitement_salaire
        impot_brut = bareme.calc(salaire)
        return impot_brut


class revenu_net_imposable(Variable):
    value_type = float
    entity = Person
    label = u"Revenu net imposable"
    definition_period = YEAR
