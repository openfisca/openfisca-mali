from openfisca_core.model_api import *
from openfisca_mali.entities import *


class salaire(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Salaires et traitements"


class salaire_brut(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Salaires et traitements brut tirés d'une activitée formelle"


class conjoint_a_des_revenus(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
