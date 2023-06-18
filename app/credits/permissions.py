from rest_framework.permissions import BasePermission

from app.credits.models import Organization


class IsOrganizerUser(BasePermission):
    """
    Allows access only to organizer users.
    """

    def has_permission(self, request, view):
        try:
            Organization.objects.get(user=request.user)
        except:
            return False
        return True
