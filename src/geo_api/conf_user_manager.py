import json

from peewee import DoesNotExist

from .keycloak_admin import CustomKeycloakAdmin
from .models import UserConf
from datetime import datetime, timedelta

class ConfUserManager:
    __additional__conf__ = [
        'user_image'
    ]

    def __init__(self, keycloak_admin: CustomKeycloakAdmin):
        self.keycloak_admin = keycloak_admin

    def get_user_roles_and_groups(self, token: dict):
        """Retrieve the roles and groups attributes for a specific user."""
        client_ = self.keycloak_admin.client_id
        # Fetch roles and groups from Keycloak
        user_roles = token.get('resource_access', {}).get(
            client_, {}).get('roles', [])
        user_groups = token.get('groups', [])

        # Combine roles and groups attributes into a dictionary
        roles_with_attributes = {
            role: role_data
            for role, role_data in self.keycloak_admin.roles.items()
            if role in user_roles
        }

        groups_with_attributes = {
            group: group_data
            for group, group_data in self.keycloak_admin.groups.items()
            if group in user_groups
        }

        additional_info = {
            ad_: token.get(ad_, '')
            for ad_ in self.__additional__conf__
        }

        # Create a dictionary with roles and groups attributes
        user_conf = {
            'roles': roles_with_attributes,
            'groups': groups_with_attributes,
            **additional_info
        }

        return user_conf

    def save_user_conf(self, user_id: str, user_conf: dict) -> None:
        """Save the user configuration (roles and groups) in the database."""
        user_conf_json = json.dumps(user_conf)

        try:
            user_conf_record = UserConf.get(UserConf.user_id == user_id)

            if user_conf_record.json != user_conf_json:
                user_conf_record.json = user_conf_json
                user_conf_record.save()

        except DoesNotExist:
            UserConf.create(UserId=user_id, json=user_conf_json)

        return None

    def update_user_conf_if_needed(self, token: dict):
        """
        Update the user configuration only if roles or groups have changed."""
        user_id = token['sub']  # Assume 'sub' contains the user ID

        # Fetch current configuration from the database
        last_update = None
        try:
            user_conf_record = UserConf.get(UserConf.user_id == user_id)
            current_conf = json.loads(user_conf_record.json)
            last_update = user_conf_record.last_update
        except DoesNotExist:
            current_conf = {}

        if last_update and (datetime.now() - last_update) < timedelta(minutes=5):
            return current_conf

        new_conf = self.get_user_roles_and_groups(token)

        if new_conf != current_conf:
            self.save_user_conf(user_id, new_conf)

        return new_conf
