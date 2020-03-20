from openfisca_core.model_api import *
from openfisca_mali.entities import *


class accidents_du_travail(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale accidents du travail et maladies professionnelles (employeur)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        accidents_du_travail = parameters(period).prelevements_obligatoires.prelevements_sociaux.accidents_du_travail
        taux_minimal = accidents_du_travail.taux_minimal
        return taux_minimal.calc(salaire_brut_annuel)


class anpe(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale ANPE (employeur)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        anpe = parameters(period).prelevements_obligatoires.prelevements_sociaux.anpe
        return 12 * anpe.calc(salaire_brut_annuel / 12)


class cotisations_employeur(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale employeur"

    def formula(person, period):
        return (
            person('anpe', period)
            + person('accidents_du_travail', period)
            + person('famille', period)
            + person('sante_employeur', period)
            + person('retraite_employeur', period)
            )


class cotisations_salariales(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale salariales"

    def formula(person, period):
        return person('retraite_salarie', period) + person('maladie_salarie', period)


class famille(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale prestations familiales et indemnités journalières de maternité (employeur)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        famille = parameters(period).prelevements_obligatoires.prelevements_sociaux.prestations_familiales
        return 12 * famille.calc(salaire_brut_annuel / 12)


class sante_employeur(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation assurance maladie oblogatoire (employeur)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        maladie = parameters(period).prelevements_obligatoires.prelevements_sociaux.maladie
        return 12 * maladie.employeur.calc(salaire_brut_annuel / 12)


class maladie_salarie(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation assurance maladie oblogatoire (salarie)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        maladie = parameters(period).prelevements_obligatoires.prelevements_sociaux.maladie
        return 12 * maladie.salarie.calc(salaire_brut_annuel / 12)


class retraite_employeur(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale de vieillesse invalidité, survivants (employeur)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        retraite = parameters(period).prelevements_obligatoires.prelevements_sociaux.retraite
        return 12 * retraite.employeur.calc(salaire_brut_annuel / 12)


class retraite_salarie(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Cotisation sociale  de vieillesse invalidité, survivants (salarié)"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        retraite = parameters(period).prelevements_obligatoires.prelevements_sociaux.retraite
        return 12 * retraite.salarie.calc(salaire_brut_annuel / 12)


class salaire_imposable(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Salaire imposable"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        cotisations_salariales = person('cotisations_salariales', period)
        return salaire_brut_annuel - cotisations_salariales


class salaire_super_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Salaire super brut"

    def formula(person, period, parameters):
        salaire_brut_annuel = person('salaire_brut', period)
        cotisations_employeur = person('cotisations_employeur', period)
        return salaire_brut_annuel + cotisations_employeur

