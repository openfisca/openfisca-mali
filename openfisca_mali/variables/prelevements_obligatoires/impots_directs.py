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
        reductions_familiales = person('reductions_familiales', period)
        impot_traitement_salaire = impot_brut - reductions_familiales
        return impot_traitement_salaire


class reductions_familiales(Variable):
    value_type = float
    default_value = 0
    entity = Person
    definition_period = YEAR
    label = "Réduction pour charge de famille"

    def formula(person, period, parameters):
        #condition_pas_enfant = nombre_enfants_a_charge == 0
        taux_reductions_familiales = parameters(period).reductions_pour_charge_de_famille

        taux = (marie == 0) * (nombre_enfants_a_charge == 0) * taux_reductions_familiales.taux_1 + \
            (marie == 1) * (nombre_enfants_a_charge == 0) * taux_reductions_familiales.taux_2 + \
            (marie == 0) * (nombre_enfants_a_charge > 0) * taux_reductions_familiales.taux_1 + (taux_reductions_familiales.taux_3 * nombre_enfants_a_charge) + \
            (marie == 1) * (nombre_enfants_a_charge > 0) * taux_reductions_familiales.taux_2 + (taux_reductions_familiales.taux_3 * nombre_enfants_a_charge)

        reductions_familiales = impot_brut * taux
        return reductions_familiales


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
        revenu_net_imposable = salaire
        return revenu_net_imposable


class nombre_enfants_a_charge(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Nombre d'enfants à charge de la personne de référence et de son/sa conjointe dans le ménage"

    def formula(household, period):
        nombre_enfants_a_charge = household.nb_persons(Household.ENFANT)
        return min_(10, nombre_enfants_a_charge)
