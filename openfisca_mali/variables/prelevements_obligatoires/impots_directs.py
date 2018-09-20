# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/variables.html


# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_mali.entities import *

#On créé une variable pour le revenu net imposable
class revenu_net_imposable(Variable):
    value_type = float
    entity = Person
    label = u"Revenu net imposable pour une personne pour une année donnée"
    definition_period = YEAR


class impot_traitement_salaire(Variable):
    value_type = float
    entity = Person
    label = u"Barême de l'ITS"
    definition_period = YEAR

    def formula(person, period, parameters):
        revenu_net_imposable = person('revenu_net_imposable', period)
        bareme = parameters(period).prelevements_obligatoires.impots_directs.impot_traitement_salaire
        impot = bareme.calc(revenu_net_imposable)
        return impot