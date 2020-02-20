from numpy import clip


from openfisca_core.model_api import *
from openfisca_mali.entities import *


class nombre_enfants_a_charge(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Nombre d'enfants à charge de la personne de référence et de son/sa conjointe dans le ménage"

    def formula(household, period, parameters):
        nombre_enfants_a_charge = household.nb_persons(Household.ENFANT)
        limite_nombre_enfants = parameters(period).reductions_pour_charge_de_famille.limite_nombre_enfants
        return min_(limite_nombre_enfants, nombre_enfants_a_charge)


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
        impot_brut = person('impot_brut', period)
        marie = person.household('marie', period)
        conjoint_a_des_revenus = person('conjoint_a_des_revenus', period)
        nombre_enfants_a_charge = person.household('nombre_enfants_a_charge', period)
        reductions_pour_charge_de_famille = parameters(period).reductions_pour_charge_de_famille

        taux = (
            not_(marie) * (reductions_pour_charge_de_famille.taux_seul + reductions_pour_charge_de_famille.taux_enfant_a_charge * nombre_enfants_a_charge)
            + marie * (reductions_pour_charge_de_famille.taux_couple + reductions_pour_charge_de_famille.taux_enfant_a_charge * nombre_enfants_a_charge)
            )
        reduction_sans_repartition = clip(impot_brut * taux, a_min = 0, a_max = impot_brut)

        repartition_parents = reductions_pour_charge_de_famille.repartition_parents
        eligible_repartition = marie * conjoint_a_des_revenus
        reduction_avec_repartition = reduction_sans_repartition * eligible_repartition * repartition_parents

        reduction_charge_famille = reduction_sans_repartition - reduction_avec_repartition
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
