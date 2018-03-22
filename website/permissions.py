def is_administrator(user):
    if user and user.groups.filter(name='Administrator').count() == 1:
        return True
        