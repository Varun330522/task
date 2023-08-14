from .constants import CONSTANTS


def calculate_IntperMonth():
    return CONSTANTS.INTEREST/CONSTANTS.YEAR


class Loan_Approval:
    @staticmethod
    def calculate_int_processing_fee(amount, tenure):
        interest_perMonth = calculate_IntperMonth()
        interest = (amount*interest_perMonth*tenure/100)
        pricipal_amount = interest/2
        return round(interest, 2), round(pricipal_amount, 2)
