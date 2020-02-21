import configparser
import logging
import os


from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_mali import entities


log = logging.getLogger(__name__)


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class CountryTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self, coicop = True):
        # We initialize our tax and benefit system with the general constructor
        super(CountryTaxBenefitSystem, self).__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        param_path = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_path)
        if coicop:
            try:
                from openfisca_ceq.tests.test_indirect_tax_variables_generator import add_coicop_item_to_tax_benefit_system
                add_coicop_item_to_tax_benefit_system(self, country = "mali")
            except (configparser.NoSectionError, ModuleNotFoundError) as e:
                log.info("No coicop consumption variable: \n")
                log.info(e)
                log.info("Passing")
