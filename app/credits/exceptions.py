from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class OneTimeIncreasedBalanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("You have used your one-time chance to charge your account.")
    default_code = "increased_balance_failed"


class NotEnoughCreditsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The sender balance is lower than amount.")
    default_code = "not_enough_credits_exception"


class TransferDestinationNotValid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("You cannot transfer money to yourself.")
    default_code = "transfer_destination_not_valid"


class TransferDestinationNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("There is no organization with provided phone number.")
    default_code = "transfer_destination_not_found"
