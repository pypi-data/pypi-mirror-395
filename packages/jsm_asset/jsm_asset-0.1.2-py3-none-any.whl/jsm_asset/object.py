from __future__ import annotations
from typing import Self
from .util import logger


class AssetObject:
    """Representation of a single Asset Object instance.

    This class wraps a single object (record) in an Asset schema. The
    instance exposes lazy-access to attributes and helpers to stage/commit
    changes.
    """

    def __init__(self, parent, type_id, object_id=None, object_data=None) -> Self:
        """Initialize an AssetObject wrapper.

        Args:
            parent (AssetSchema): Parent schema instance that defines the
                object's type.
            type_id (int): The id of the object type within the schema.
            object_id (int|str, optional): The id of the object instance. If
                not provided, object_data must be supplied or an API fetch
                will be attempted.
            object_data (dict, optional): Raw object JSON as returned by the
                Assets API. When provided the object will not be fetched.
        """
        # parent is an AssetSchema instance
        self.schema = parent
        self.session = parent.session
        self.id = object_id
        self.type = parent.object_types[type_id]
        self.object_data = object_data
        # At object creation it's possible we won't have the object data, so we need to pull it from the API
        if object_data is None:
            response = self.session.api_request(method='get', path=f'/object/{object_id}')
            if response.status_code == 200:
                self.object_data = response.json()
            else:
                logger.error('Failed to retrieve data for AssetObject %s', object_id)
                self.object_data = {}
        self.name = self.object_data.get('label')
        self.id = self.object_data.get('id', None)
        self.url = f'{self.session.jira_site_url}/jira/assets/object/{self.id}'

        # Lazy-evaluated properties
        self._attributes = None
        # staged updates
        self.updates = []

    @property
    def attributes(self):
        """Return a mapping of attribute id -> attribute wrapper for the object.

        The mapping is lazily constructed on first access. Attribute wrapper
        classes are chosen based on the attribute type defined on the
        object's type.

        Returns:
            dict: Mapping of attribute id to attribute wrapper instances.
        """
        attribute_types = None
        # lazy import attribute wrapper classes to avoid cycles
        from .schema import (
            AssetObjectTypeDefaultAttribute,
            AssetObjectTypeObjectAttribute,
            AssetObjectTypeUserAttribute,
            AssetObjectTypeGroupAttribute,
            AssetObjectTypeStatusAttribute,
        )
        attribute_types = {
            0: AssetObjectTypeDefaultAttribute,
            1: AssetObjectTypeObjectAttribute,
            2: AssetObjectTypeUserAttribute,
            4: AssetObjectTypeGroupAttribute,
            7: AssetObjectTypeStatusAttribute,
        }
        if self._attributes is None:
            object_attribute_data = {x['objectTypeAttributeId']: x for x in self.object_data.get('attributes', [])}
            logger.info('Processing attributes for AssetObject %s, found values: %s', self.id, object_attribute_data.keys())
            self._attributes = {}
            # Populate the object attribute dict with the object type's defined attributes
            for k, v in self.type.attributes.items():
                logger.info('Processing attribute %s of type %s', k, type(v))
                attribute_data = v.raw_data
                if k in object_attribute_data.keys():
                    attribute_data = v.raw_data | object_attribute_data[k]
                self._attributes[k] = attribute_types[attribute_data['type']](self, attribute_data)
        return self._attributes

    def __str__(self):
        return (self.name or '')

    def __repr__(self):
        return f'<AssetObject: {self.schema.name}/{self.type}/{self.name} id: {self.id}>'

    def stage_attr_change(self, attribute_id, values):
        """Stage an attribute change to be committed by :meth:`update`.

        Args:
            attribute_id (int): The id of the attribute to change.
            values (list): A list of attribute value payloads in API format.
        """
        self.updates.append({'objectTypeId': attribute_id, 'attributes': values})

    def pending_changes(self):
        """Return the currently staged changes for this object.

        Returns:
            list: A list of staged update payloads.
        """
        return self.updates

    def update(self):
        """Commit staged changes to the Assets API.

        The refactor left update logic as a placeholder. Callers should either
        implement this method or perform API updates via the session helper
        functions.

        Raises:
            NotImplementedError: Always, until an implementation is provided.
        """
        # Placeholder - user said they handled update logic elsewhere
        raise NotImplementedError('update() not implemented in refactor placeholder')

    def delete(self):
        """Delete the Asset Object from the JSM instance.

        Returns:
            bool: True if the deletion succeeded, False otherwise.
        """
        if self.id:
            response = self.session.api_request('delete', f'/object/{self.id}')
            if response.status_code == 200:
                logger.info('Successfully deleted AssetObject %s', self.id)
                return True
            else:
                logger.error('Attempt to delete AssetObject %s failed.', self.id)
                return False
        else:
            logger.error('Attempt to delete an uncommitted AssetObject failed.')
            return False


class AssetAttributeValue(object):
    """Represents a single attribute value for an :class:`AssetObject`.

    This is the base class for specialized attribute value types (object,
    user, etc.).
    """
    def __init__(self, parent, value_data):
        """Initialize an attribute value wrapper.

        Args:
            parent: The attribute or object that owns this value.
            value_data (dict): Raw API payload for the attribute value.
        """
        self.parent = parent
        self.value_data = value_data
        self.type = 'Default'
        self.display_value = value_data.get('displayValue', None)
        self.search_value = value_data.get('searchValue', None)
        self.referenced_type = value_data.get('referencedType', None)

    def __str__(self):
        return f'{self.display_value}'

    def __repr__(self):
        return f'<AssetAttributeValue: {self.display_value}>'


class AssetAttributeObjectValue(AssetAttributeValue):
    """Attribute value representing a reference to another AssetObject."""
    def __init__(self, parent, value_data):
        """Create an object-valued attribute wrapper.

        Adds object-specific convenience attributes such as ``id`` and
        ``label``.
        """
        super().__init__(parent, value_data)
        self.type = 'Object'
        self.id = value_data.get('id', None)
        self.label = value_data.get('label', None)
        self.object_type_id = value_data.get('objectTypeId', None)
        self.object_schema_id = value_data.get('objectSchemaId', None)


class AssetAttributeUserValue(AssetAttributeValue):
    """Attribute value representing a user reference."""
    def __init__(self, parent, value_data):
        """Create a user-valued attribute wrapper.

        Exposes common user fields such as account id and display name.
        """
        super().__init__(parent, value_data)
        self.type = 'User'
        self.account_id = value_data.get('accountId', None)
        self.email = value_data.get('email', None)
        self.display_name = value_data.get('displayName', None)
        self.active = value_data.get('active', None)
