from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import Q
from accounts.models import *

# Setting External Models
content_types = []
for i in range(20):
    content_types.append(ContentType.objects.create(app_label="external", model=f"model{str(i).zfill(3)}"))

operations = ['create', 'read', 'update', 'delete']
for content_type in content_types:
    for operation in operations:
        Permission.objects.create(
            name=f"{operation} {content_type.model}",
            content_type=content_type,
            codename=f"{content_type.app_label}_{operation}_{content_type.model}"
        )

# Setup Groups
read_only = Group.objects.create(name="viewer")
read_only.permissions.set(Permission.objects.filter(name__startswith=operations[1]))

admin = Group.objects.create(name="admin")
admin.permissions.set(Permission.objects.filter(content_type__in=content_types))

manager = Group.objects.create(name="manager")
manager.permissions.set(Permission.objects.filter(Q(content_type__in=content_types) & ~Q(name__startswith="delete")))


# Setup Users
users = []
for i in range(10):
    users.append(User.objects.create(email=f"user_{str(i).zfill(3)}@example.com",
                 password=make_password(f"@Password_{str(i).zfill(3)}")))

for i in range(len(users)):
    team = Team.objects.create(name=f"Team {str(i).zfill(3)}", owner=users[i])
    for j in range(len(users)):
        if i != j:
            membership = Membership.objects.create(
                email=users[j].email, invited_by=users[i], team=team, holder=users[j])
            membership.permissions.set(read_only.permissions.all() if j % 2 == 0 else admin.permissions.all())
