# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_mali.entities import *


class salaire(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Salaires et Traitements"


class conjoint_a_des_revenus(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
