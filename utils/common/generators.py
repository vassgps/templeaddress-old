# webapp/utils/common/generators.py
import string
import random
import logging

# from django.contrib.auth import get_user_model

logger = logging.getLogger("django")


# Function for generate Random codes
def generate_random_code():
    try:
        number = random.randint(10001, 99999)
        result = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + str(number)
        return result
    except Exception as ex:
        logger.error(ex)
        return None


# Choice filed generators
class ChoiceMenu:
    USER_SCOPES = [("1", "Super Admin"), ("2", "Portal Admin"),
                   ("3", "Portal Manager"), ("4", "Project Coordinator"),
                   ("5", "Premium User"), ("6", "Normal User"),
                   ("7", "Clubs"), ("8", "Customer"), ("9", "Other")]

    DESIGNATION = [("1", "Pujari or Priest"), ("2", "Archaka or Kazhakam"),
                   ("3", "Sthapati"), ("4", "Astrologer"),
                   ("5", "Administrative Staff"), ("6", "Tantric"),
                   ("7", "Artists"), ("8", "Cook"),
                   ("9", "Hereditary"), ("10", "Volunteers")]

    STATUS = [("1", "PENDING"), ("2", "HOLD"), ("3", "OTHER"),
              ("4", "REVERTED"), ("5", "REJECTED"), ("6", "DELETED"),
              ("7", "VERIFIED"), ("8", "APPROVED"), ("9", "DONE")]
    # agreement
    AGREEMENT = [("TOS", "Terms Of Service"), ("PRIVACY", "Privacy policy"), ("OTHER", "Other"),
                 ("DATA", "Data Policy"), ("BILLING", "Billing and Finance")]
    PORTAL_TYPE = [("1", "BLOG"), ("2", "LISTING"), ("3", "DATA"), ("4", "CRM"), ("5", "ERP"), ]

    VERSION = [("1", "2020"), ("2", "2021"), ("3", "2022"), ("4", "2023"), ("5", "2024"), ("6", "2025")]

    PACKAGES = [("1", "Basic"), ("2", "Advanced"), ("3", "Premium"), ("4", "Enterprise"), ("5", "Other"), ]

    TEMPLE_TYPES = [("1", "Temples"), ("2", "Kavu"), ("3", "Other")]

    TXN_TYPES = [("1", "Customer"), ("2", "System"), ("3", "User")]
    pass


def default_blank_fields():
    fields = []
    return fields
