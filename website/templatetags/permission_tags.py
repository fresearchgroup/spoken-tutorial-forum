from django import template

from website.views import is_administrator

register = template.Library()

def can_edit(user, obj):
    if user.id == obj.uid or is_administrator(user):
        return True
    return False

def isadministrator(user):
    return is_administrator(user)

register.filter(can_edit)
register.filter(isadministrator)
