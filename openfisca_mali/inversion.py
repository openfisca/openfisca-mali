import numpy as np


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class autres_revenus_du_capital_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Revenu des capitaux brut"

    def formula(individu, period, parameters):
        return individu('autres_revenus_du_capital', period)


class revenu_foncier_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Revenu locatif (foncier) brut"

    def formula(individu, period, parameters):
        return individu('revenu_locatif', period)


class revenu_non_salarie_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Revenu non salarie brut"

    def formula(individu, period, parameters):
        return individu('revenu_non_salarie', period)


class pension_retraite_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR

    def formula(individu, period, parameters):
        return individu('pension_retraite', period)


class salaire_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Salaire brut"

    def formula(person, period, parameters):
        salaire = person('salaire', period)
        marie = person.household('marie', period)
        nombre_enfants_a_charge = person.household('nombre_enfants_a_charge', period)
        reductions_pour_charge_de_famille = parameters(period).reductions_pour_charge_de_famille
        taux = (
            not_(marie) * (reductions_pour_charge_de_famille.taux_seul + reductions_pour_charge_de_famille.taux_enfant_a_charge * nombre_enfants_a_charge)
            + marie * (reductions_pour_charge_de_famille.taux_couple + reductions_pour_charge_de_famille.taux_enfant_a_charge * nombre_enfants_a_charge)
            )
        salaire_imposable = 0
        for taux_ in np.unique(taux):
            impot_traitement_salaire = parameters(period).prelevements_obligatoires.impots_directs.impot_traitement_salaire.copy()
            impot_traitement_salaire.multiply_rates((1 - taux_))
            salaire_imposable = (
                salaire_imposable
                + (taux_ == taux) * impot_traitement_salaire.inverse().calc(salaire)
                )

        retraite = parameters(period).prelevements_obligatoires.prelevements_sociaux.retraite.salarie.copy()
        sante = parameters(period).prelevements_obligatoires.prelevements_sociaux.maladie.salarie
        prelevements_sociaux = retraite.copy()
        prelevements_sociaux.add_tax_scale(sante)

        salaire_brut = 12 * prelevements_sociaux.inverse().calc(salaire_imposable / 12)

        return salaire_brut
