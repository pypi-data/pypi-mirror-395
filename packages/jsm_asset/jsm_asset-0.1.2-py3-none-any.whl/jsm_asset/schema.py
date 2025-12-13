"""Defines the AssetSchema and AssetObjectType classes for interaction with the JSM Assets API."""
from __future__ import annotations
from typing import Self
from datetime import datetime
from .util import logger


class AssetSchema:
    """Provides an interface for a JSM Asset Schema.

    An AssetSchema contains object types and objects. This wrapper exposes
    lazy accessors for object types and object enumerations and provides
    helpers to update or delete the schema.
    """
    def __init__(self, jsm_instance, schema_id: int, object_data: dict = None) -> Self:
        logger.debug(f'Instantiating an AssetSchema: id: {schema_id}, object_data: {object_data}')
        self.id = schema_id
        self.session = jsm_instance
        self.object_data = object_data
        if self.object_data is None:
            logger.debug(f'Object data for AssetSchema {schema_id} was None, pulling data from endpoint')
            response = self.session.api_request(method='get', path=f'/objectschema/{self.id}')
            if response.status_code == 200:
                self.object_data = response.json()
            else:
                logger.error(f'Failed to retrieve data for AssetSchema {schema_id}')
                self.object_data = {}
        self.name = self.object_data.get('name')
        self.object_schema_key = self.object_data.get('objectSchemaKey')
        self.object_count = self.object_data.get('objectCount', 0)
        self.description = self.object_data.get('description', '')
        created = self.object_data.get('created')
        updated = self.object_data.get('updated')
        if created:
            self.created = datetime.fromisoformat(created.replace("Z", "+00:00"))
        else:
            self.created = None
        if updated:
            self.updated = datetime.fromisoformat(updated.replace("Z", "+00:00"))
        else:
            self.updated = None

        # lazy values
        self._object_types = None
        self._objects = None
        # initialize backing store for object types
        self._object_types = {}

    @property
    def object_types(self):
        """Return a mapping of object type id -> :class:`AssetObjectType`.

        The mapping is lazily populated from the Assets API on first access.
        Returns an empty dict when the retrieval fails.
        """
        if self._object_types is None:
            response = self.session.api_request('get', f'/objectschema/{self.id}/objecttypes/flat')
            if response.status_code == 200:
                # instantiate the concrete AssetObjectType implementation
                self._object_types = {x['id']: AssetObjectType(self, x['id'], object_data=x) for x in response.json()}
            else:
                logger.error(f'Failed to retrieve object types for AssetSchema {self.id}')
        return self._object_types

    @property
    def objects(self):
        """Return an :class:`AQLQuery` that yields objects for this schema.

        The returned query will not include attribute values by default to
        reduce payload size; callers can override that behavior when needed.
        """
        from .aql import AQLQuery
        return AQLQuery(self.session, f'objectSchemaId = {self.id}', include_attributes=False)

    def __str__(self):
        return (self.name or '')

    def __repr__(self):
        return (f'<AssetSchema: {self.name}, id: {self.id}')

    def update(self):
        """Update the schema metadata on the Assets API.

        Returns:
            AssetSchema: The refreshed AssetSchema instance on success.
            None: On failure.
        """
        data = {
            'name': self.name,
            'objectSchemaKey': self.object_schema_key,
            'description': self.description,
        }
        response = self.session.api_request('put', f'/objectschema/{self.id}', data=data)
        if response.status_code == 200:
            self.session.schemas[self.id] = AssetSchema(self.session, self.id, object_data=response.json())
            return self
        else:
            logger.error(f'Attempt to update AssetSchema {self.id} failed.')

    def delete(self):
        """Delete this schema from the Assets instance.

        Returns:
            bool: True when deletion succeeds, False otherwise.
        """
        response = self.session.api_request('delete', f'/objectschema/{self.id}')
        if response.status_code == 200:
            del self.session.schemas[self.id]
            return True
        else:
            logger.error(f'Attempt to delete AssetSchema {self.id} failed.')
            return False


class AssetObjectType:
    """Represents an object type inside an AssetSchema.

    The class wraps metadata about the object type (attributes, icon,
    description) and provides access to the type's defined attributes.
    """
    def __init__(self, parent, id, object_data=None):
        """Initialize an AssetObjectType wrapper.

        Args:
            parent (AssetSchema): The schema that owns this object type.
            id (int): The id of the object type.
            object_data (dict, optional): Raw API payload for the object type.
        """
        self.schema = parent
        self.session = parent.session
        self.id = id
        self.object_data = object_data
        if self.object_data is None:
            response = self.session.api_request(method='get', path=f'/objecttype/{id}')
            if response.status_code == 200:
                self.object_data = response.json()
            else:
                logger.error(f'Failed to retrieve data for ObjectType {id}')
                self.object_data = {}
        self.global_id = self.object_data.get('globalId')
        self.name = self.object_data.get('name')
        self.description = self.object_data.get('description', '')
        self.icon = self.object_data.get('icon')
        self.position = self.object_data.get('position')
        self.created = self.object_data.get('created')
        self.updated = self.object_data.get('updated')
        self.object_count = self.object_data.get('objectCount')
        if self.object_data.get('parentObjectId', None) is not None:
            self.session_object_type = AssetObjectType(self.session, self.object_data['parentObjectId'])
        else:
            self.session_object_type = None
        self.inherited = self.object_data.get('inherited')
        self.abstract_object_type = self.object_data.get('abstractObjectType')
        self.url = f'{self.session.jira_site_url}/jira/assets/object-schema/{self.schema.id}?typeId={self.id}'

        # @property decorated values that are lazy-evaluated
        self._attributes = None
        # initialize backing store for attributes
        self._attributes = {}

    def __str__(self):
        return (self.name or '')

    def __repr__(self):
        return f'<AssetObjectType: {self.schema.name}/{self.name} id: {self.id}>'

    @property
    def attributes(self):
        """Return a mapping of attribute id -> attribute type wrapper.

        Attributes are lazily retrieved from the API and wrapped in the
        appropriate attribute-type classes.
        """
        attribute_types = {
            0: AssetObjectTypeDefaultAttribute,
            1: AssetObjectTypeObjectAttribute,
            2: AssetObjectTypeUserAttribute,
            4: AssetObjectTypeGroupAttribute,
            7: AssetObjectTypeStatusAttribute,
        }
        if self._attributes is None:
            self._attributes = {}
            response = self.session.api_request('get', f'/objecttype/{self.id}/attributes')
            if response.status_code == 200:
                for attribute in response.json():
                    logger.info('Creating attribute of type_id %s', attribute.get('type'))
                    self._attributes[attribute['id']] = attribute_types[attribute['type']](self, attribute)
        return self._attributes

    def update(self):
        """Update the object type metadata on the Assets API.

        Returns:
            AssetObjectType: self on success, None on failure.
        """
        data = {
            'name': self.name,
            'description': self.description,
            'iconId': self.icon['id'] if self.icon else 1,
            'inherited': self.inherited,
            'abstractObjectType': self.abstract_object_type,
        }
        response = self.session.api_request('put', f'/objecttype/{self.id}', data=data)
        if response.status_code == 200:
            return self
        else:
            logger.error('Attempt to update AssetObjectType %s failed.', self.id)
            return None

    def delete(self):
        """Delete this object type from its schema.

        Returns:
            bool: True on success, False otherwise.
        """
        response = self.session.api_request('delete', f'/objecttype/{self.id}')
        if response.status_code == 200:
            return True
        else:
            logger.error('Attempt to delete AssetObjectType %s failed.', self.id)
            return False

    def create_object(self, name):
        """Create a new object instance of this type.

        Args:
            name (str): The display name/label for the new object.

        Returns:
            AssetObject: The created object on success, None on failure.
        """
        data = {
            'objectTypeId': self.id,
            'label': name,
        }
        response = self.session.api_request('post', '/object/create', data=data)
        if response.status_code == 201:
            data = response.json()
            from .object import AssetObject
            return AssetObject(self.schema, data['objectTypeId'], object_data=data)
        else:
            logger.error('Attempt to create AssetObject %s failed.', name)
            return None


class AssetObjectTypeAttribute:
    """Represents an attribute type defined on an object type.

    Instances of this class describe attribute metadata (name, type,
    cardinality) and provide helpers to read/update/delete the attribute
    definition.
    """
    def __init__(self, parent, attribute_data):
        """Initialize an attribute-type wrapper.

        Args:
            parent (AssetObjectType|AssetObject): The owning object type or
                instance.
            attribute_data (dict): Raw attribute metadata from the API.
        """
        self.parent = parent
        self.id: int = attribute_data.get('id')
        if isinstance(self.parent, AssetObjectType):
            self.object_type = self.parent
            self.attribute_data = attribute_data
        else:
            # parent is AssetObject
            self.object_type = self.parent.type
            self.attribute_data = self.parent.type.attributes[self.id].raw_data | attribute_data
        self.name: str = attribute_data.get('name', None)
        self.label: bool = attribute_data.get('label', False)
        self.description: str = attribute_data.get('description', '')
        self.type_id: int = attribute_data.get('type', 0)
        self.cardinality: tuple = (attribute_data.get('minimumCardinality', 0), attribute_data.get('maximumCardinality', 1))
        self.include_child_object_types: bool = attribute_data.get('includeChildObjectTypes', False)
        self.hidden: bool = attribute_data.get('hidden', False)
        self.updates: dict = {}
        self.raw_data = attribute_data
        self._values: list = None

    def __str__(self):
        return (self.name or '')

    def __repr__(self):
        string = f'<{self.__class__.__name__}'
        if hasattr(self, 'default_type'):
            string += f'[{getattr(self, "default_type")}] '
        else:
            string += ' '
        string += self.name
        if isinstance(self.parent, AssetObjectType):
            return string + '>'
        value_string = str([val['displayValue'] for val in self.values])
        return f'{string} -> {value_string}>'

    @property
    def values(self):
        """Return attribute values for an attribute instance.

        For attribute definitions (when parent is :class:`AssetObjectType`) no
        instance values exist. For attribute instances (parent is
        :class:`AssetObject`) the method returns a list of values taken from the
        object's data.
        """
        if isinstance(self.parent, AssetObjectType):
            logger.info('Not setting values for Attribute on ObjectType %s', self.id)
        else:
            self._values = []
            for value in self.attribute_data.get('objectAttributeValues', []):
                self._values.append(value)
                #self._values_in_api_format = [val['searchValue'] for val in self._values]
            return self._values

    def update(self):
        """Update the attribute type definition on the Assets API.

        This method is a no-op for attribute instances on objects; only
        attribute-type definitions can be updated here.
        """
        updates = {
            'name': getattr(self, 'name'),
            'label': getattr(self, 'label'),
            'description': getattr(self, 'description'),
            'type': getattr(self, 'type_id'),
            'minimumCardinality': getattr(self, 'cardinality')[0],
            'maximumCardinality': getattr(self, 'cardinality')[1],
            'hidden': getattr(self, 'hidden'),
        }
        if isinstance(self.parent, AssetObject):
            logger.info('Skipping attempt to update attributetype on instance of AssetObject')
            return
        response = self.parent.session.api_request('PUT', f'/objecttypeattribute/{self.parent.type_id}/{self.id}', data=updates)
        if response.status_code == 200:
            self.updates = {}
            logger.info('Succesful update of attribute %s on object attribute type %s', self.id, self.parent.id)

    def delete(self):
        """Delete this attribute definition from its parent type.

        Returns:
            None
        """
        response = self.parent.session.api_request('DELETE', f'/objecttypeattribute/{self.id}')
        if response.status_code == 200:
            del self.parent.attributes[self.id]


# Specializations

class AssetObjectTypeDefaultAttribute(AssetObjectTypeAttribute):
    """Default attribute type (text, numeric, date, etc.)."""
    def __init__(self, parent, attribute_data):
        super().__init__(parent, attribute_data)
        if attribute_data.get('defaultType'):
            self.default_type_id = attribute_data.get('defaultType').get('id', None)
            self.default_type = attribute_data.get('defaultType').get('name', None)
        if getattr(self, 'default_type_id', None) == 7:
            self.additional_value = attribute_data.get('additionalValue', '')
        if getattr(self, 'default_type_id', None) in [1, 3]:
            self.suffix = attribute_data.get('suffix', None)
            self.summable = attribute_data.get('summable', False)
        if getattr(self, 'default_type_id', None) in [0, 8]:
            self.regex_validation = attribute_data.get('regexValidation')
        if getattr(self, 'default_type_id', None) == 10:
            self.options = attribute_data.get('options', [])

    def update(self):
        pass


class AssetObjectTypeObjectAttribute(AssetObjectTypeAttribute):
    def __init__(self, parent, attribute_data):
        super().__init__(parent, attribute_data)


class AssetObjectTypeUserAttribute(AssetObjectTypeAttribute):
    def __init__(self, parent, attribute_data):
        super().__init__(parent, attribute_data)


class AssetObjectTypeGroupAttribute(AssetObjectTypeAttribute):
    def __init__(self, parent, attribute_data):
        super().__init__(parent, attribute_data)


class AssetObjectTypeStatusAttribute(AssetObjectTypeAttribute):
    def __init__(self, parent, attribute_data):
        super().__init__(parent, attribute_data)
