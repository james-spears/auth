from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Membership

User = get_user_model()


class MembershipSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = [
            'team',
            'permissions'
        ]

    def get_team(self, obj):
        return obj.team.name

    def get_permissions(self, obj):
        # 'obj' is the instance of MyObject being serialized
        # You can access related objects, perform calculations, etc.
        # For example, if 'obj' has a related manager 'items':
        permissions = list(
            map(
                lambda x: x.codename,
                obj.permissions.all()))
        return permissions


class UserSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    memberships = MembershipSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'teams',
            'permissions',
            'memberships',
        ]

    def get_teams(self, obj):
        # 'obj' is the instance of MyObject being serialized
        # You can access related objects, perform calculations, etc.
        # For example, if 'obj' has a related manager 'items':
        teams = list(
            map(
                lambda x: x.name,
                obj.teams.all()))
        return teams

    def get_permissions(self, obj):
        # 'obj' is the instance of MyObject being serialized
        # You can access related objects, perform calculations, etc.
        # For example, if 'obj' has a related manager 'items':
        permissions = list(
            map(
                lambda x: x.codename,
                obj.get_all_permissions()))
        return permissions
