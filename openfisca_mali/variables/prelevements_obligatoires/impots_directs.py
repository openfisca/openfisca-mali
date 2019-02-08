# -*- coding: utf-8 -*-


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class nombre_enfants_a_charge(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Nombre d'enfants à charge de la personne de référence et de son/sa conjointe dans le ménage"

    def formula(household, period):
        nombre_enfants_a_charge = household.nb_persons(Household.ENFANT)
        return min_(10, nombre_enfants_a_charge)


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


class impot_traitement_salaire(Variable):
    value_type = float
    entity = Person
    label = u"Impôt pour les traitements et les salaires"
    definition_period = YEAR

    def formula(person, period):
        impot_brut = person('impot_brut', period)
        reduction_charge_famille = person('reduction_charge_famille', period)
        impot_traitement_salaire = impot_brut - reduction_charge_famille
        return impot_traitement_salaire


class reduction_charge_famille(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Réduction pour charge de famille"

    def formula(person, period, parameters):
        marie = person.household('marie', period)
        nombre_enfants_a_charge = person.household('nombre_enfants_a_charge', period)
        reductions_pour_charge_de_famille = parameters(period).reductions_pour_charge_de_famille
        taux = (
            not_(marie) * reductions_pour_charge_de_famille.taux_seul
            + marie * reductions_pour_charge_de_famille.taux_couple
            + reductions_pour_charge_de_famille.taux_enfant_a_charge * nombre_enfants_a_charge
            )
        reduction_charge_famille = person('impot_brut', period) * taux
        return reduction_charge_famille


class revenu_net_imposable(Variable):
    value_type = float
    entity = Person
    label = u"Revenu net imposable"
    definition_period = YEAR

    def formula(person, period):
        salaire = person('salaire', period)
        revenu_net_imposable = salaire
        return revenu_net_imposable
