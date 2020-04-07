from openfisca_core.model_api import *
from openfisca_mali.entities import *


class accidents_du_travail(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale accidents du travail et maladies professionnelles (employeur)"

    def formula(person, period, parameters):
        salaire_annuel = person('salaire', period)
        accidents_du_travail = parameters(period).prelevements_obligatoires.prelevements_sociaux.accidents_du_travail
        taux_minimal = accidents_du_travail.taux_minimal
        return taux_minimal * salaire_annuel


class famille(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale prestations familiales et indemnités journalières de maternité (employeur)"

    def formula(person, period, parameters):
        salaire_annuel = person('salaire', period)
        famille = parameters(period).prelevements_obligatoires.prelevements_sociaux.prestations_familiales
        return 12 * famille.calc(salaire_annuel / 12)


class retraite_employeur(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale de vieillesse invalidité, survivants (employeur)"

    def formula(person, period, parameters):
        salaire_annuel = person('salaire', period)
        retraite = parameters(period).prelevements_obligatoires.prelevements_sociaux.retraite
        return 12 * retraite.employeur.calc(salaire_annuel / 12)


class retraite_salarie(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale  de vieillesse invalidité, survivants (salarié)"

    def formula(person, period, parameters):
        salaire_annuel = person('salaire', period)
        retraite = parameters(period).prelevements_obligatoires.prelevements_sociaux.retraite
        return 12 * retraite.salarie.calc(salaire_annuel / 12)
