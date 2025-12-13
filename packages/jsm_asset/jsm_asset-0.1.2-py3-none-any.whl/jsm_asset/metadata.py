"""
Simple support libraries for use with jsm_asset
"""
from enum import Enum

class DefaultAttributeTypes(Enum):
    Text = 0
    Integer = 1
    Boolean = 2
    Double = 3
    Date = 4
    Time = 5
    DateTime = 6
    Url = 7
    Email = 8
    TextArea = 9
    Select = 10
    IPAddress = 11
       
class AttributeTypes(Enum):
    AssetObjectTypeDefaultAttribute = 0
    AssetObjectTypeObjectAttribute = 1
    AssetObjectTypeUserAttribute = 2
    AssetObjectTypeGroupAttribute = 4
    AssetObjectTypeStatusAttribute = 7