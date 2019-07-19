from ..data_template import DataTemplate
from faker.providers import bank
from faker.providers import credit_card


class CreditCardTemplate(DataTemplate):

    def generate(self):

        self.faker.add_provider(bank)
        self.faker.add_provider(credit_card)

        if self.format == "delimited":
            return self.faker.name() + self.delimiter + self.faker.iban() + self.delimiter + \
                   self.faker.credit_card_number() + self.delimiter + self.faker.credit_card_provider()
        elif self.format == "json":
            json_obj = dict()
            json_obj["owner_name"] = self.faker.name()
            json_obj["iban"] = self.faker.iban()
            json_obj["credit_card_number"] = self.faker.credit_card_number()
            json_obj["credit_card_provider"] = self.faker.credit_card_provider()
            return json_obj
        else:
            "WRONG FORMAT"
