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
