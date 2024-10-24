from keycloak import KeycloakAdmin


class CustomKeycloakAdmin(KeycloakAdmin):
    __client_secret_key__ = 'client_secret_key'
    __client_id__ = 'client_id'

    def __init__(self, *args, **kwargs):
        kwargs['client_id'] = 'admin-cli'
        super().__init__(*args, **kwargs)
        self.client_secret_key = kwargs.get(
            self.__client_secret_key__, '')
        self.client_id = kwargs.get(
            self.__client_id__, '')

        self.roles = self.get_all_roles_with_attributes()
        self.groups = self.get_all_groups_with_attributes()

    def get_client_id_by_name(self):
        """Retrieve the client ID using the client's name."""

        clients = self.get_clients()
        for client in clients:
            if client['clientId'] == self.client_id:
                return client['id']
        raise Exception(f"Client '{self.client_id}' not found")

    def get_role_attributes(self, role_id: str):
        """Retrieve the attributes for a specific role in a client."""
        role_details = self.get_role_by_id(role_id)
        return role_details.get('attributes', {})

    def get_all_roles_with_attributes(self):
        """Retrieve all roles and their attributes for a client."""
        roles = self.get_client_roles(client_id=self.client_secret_key)

        roles_with_attributes = {}
        for role in roles:
            role_name = role['name']
            role_id = role['id']
            attributes = self.get_role_attributes(role_id)
            roles_with_attributes[role_name] = attributes

        return roles_with_attributes

    def get_all_groups_with_attributes(self):
        """Retrieve all groups and their attributes for a client."""
        groups = self.get_groups()

        group_with_attributes = {}
        for group in groups:
            group_path = group['path']
            properties = self.get_group_by_path(group_path)
            group_with_attributes[group_path] = properties.get(
                'attributes', {})

        return group_with_attributes

    def update_roles_and_groups(self):
        self.roles = self.get_all_roles_with_attributes()
        self.groups = self.get_all_groups_with_attributes()
