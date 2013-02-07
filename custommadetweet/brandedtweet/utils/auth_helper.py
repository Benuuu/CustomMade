from django.contrib.auth.models import Group, User

def is_editor(user):
    if user:
        return user.groups.filter(name='Editors') != 0
    return False
    
def is_staff(user):
    if user:
        return user.groups.filter(name='Staff') != 0
    return False
