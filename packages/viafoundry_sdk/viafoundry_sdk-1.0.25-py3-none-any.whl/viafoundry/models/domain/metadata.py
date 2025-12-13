from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Literal, Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import re


class FieldType(str, Enum):
    """Enumeration for field types in metadata."""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    SELECT = "select"
    MULTISELECT = "multiselect"
    FILE = "file"
    REFERENCE = "reference"


class EveryoneEntry(BaseModel):
    type: Literal["everyone"]
    read: bool
    write: bool


class UserEntry(BaseModel):
    type: Literal["user"]
    email: EmailStr
    read: bool
    write: bool


class GroupEntry(BaseModel):
    type: Literal["group"]
    groupId: str = Field(..., pattern="^[0-9a-fA-F]{24}$")
    read: bool
    write: bool

    @field_validator('groupId')
    def validate_object_id(cls, v):
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError('Must be a valid 24-character hex ObjectId')
        return v


PermEntry = Union[EveryoneEntry, UserEntry, GroupEntry]


class OwnerModel(BaseModel):
    """
    Model representing an owner entity.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id",
                    description="Unique identifier for the owner")
    username: Optional[str] = Field(None, description="Username of the owner")
    name: Optional[str] = Field(None, description="Full name of the owner")
    email: Optional[str] = Field(
        None, description="Email address of the owner")
    affiliation: Optional[str] = Field(
        None, description="Affiliation of the owner")


class CanvasCreate(BaseModel):
    """
    Model for creating a new metadata canvas.
    """
    id: Optional[str] = Field(None, alias="_id",
                              description="Unique identifier for the canvas")
    name: str = Field(..., description="Name of the vmeta canvas")
    label: str = Field(..., description="Label of the vmeta canvas")
    perms: Optional[List[PermEntry]] = Field(
        None, description="Permissions for the canvas")
    dataPerms: Optional[List[PermEntry]] = Field(
        None, description="Data permissions for the canvas")
    active: Optional[bool] = Field(
        True, description="Is the canvas active? Defaults to True")
    createDefaultCollections: Optional[bool] = Field(
        True, description="Create default collections for the canvas? Defaults to True")

    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """Validate id is a valid MongoDB ObjectId (24 hex characters)."""
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError(
                "id must be a valid MongoDB ObjectId (24 hexadecimal characters)")
        return v


class CanvasUpdate(BaseModel):
    """
    Model for updating an existing metadata canvas.
    """
    name: Optional[str] = Field(..., description="Name of the canvas")
    label: Optional[str] = Field(..., description="Label of the canvas")


class CollectionCreate(BaseModel):
    """
    Model for creating a new metadata collection.
    """
    id: Optional[str] = Field(None, alias="_id",
                              description="Unique identifier for the collection")
    name: str = Field(..., description="Name of the collection")
    label: str = Field(..., description="Label of the collection")
    version: Optional[int] = Field(None,
                                   description="Version of the collection")
    canvasID: str = Field(...,
                           description="ID of the canvas this collection belongs to")
    dataPerms: Optional[List[PermEntry]] = Field(
        None, description="Data permissions for the collection")
    perms: Optional[List[PermEntry]] = Field(
        None, description="Permissions for the collection")
    dataDeleteProtected: Optional[bool] = Field(
        None, description="Protect Data Deletion?")

    @field_validator('canvasID', 'id')
    @classmethod
    def validate_canvas_id(cls, v):
        """Validate canvasID is a valid MongoDB ObjectId (24 hex characters)."""
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError(
                "canvasID must be a valid MongoDB ObjectId (24 hexadecimal characters)")
        return v


class CollectionUpdate(BaseModel):
    """
    Model for updating an existing metadata collection.
    """
    name: Optional[str] = Field(None, description="Name of the collection")
    label: Optional[str] = Field(None, description="Label of the collection")
    version: Optional[int] = Field(None,
                                   description="Version of the collection")
    canvasID: Optional[str] = Field(None,
                                     description="ID of the canvas this collection belongs to")
    dataPerms: Optional[List[PermEntry]] = Field(
        None, description="Permissions for the collection")
    perms: Optional[List[PermEntry]] = Field(
        None, description="Permissions for the collection")
    dataDeleteProtected: Optional[bool] = Field(
        None, description="Protect Data Deletion?")

    @field_validator('canvasID')
    @classmethod
    def validate_canvas_id(cls, v):
        """Validate canvasID is a valid MongoDB ObjectId (24 hex characters)."""
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError(
                "canvasID must be a valid MongoDB ObjectId (24 hexadecimal characters)")
        return v


class FieldOption(BaseModel):
    """
    Model representing an option for select/multiselect fields.
    """
    label: str = Field(..., description="Display label for the option")
    value: str = Field(..., description="Value of the option")


class VmetaFieldType(str, Enum):
    STRING = "String"
    NUMBER = "Number"
    BOOLEAN = "Boolean"
    ARRAY = "Array"
    DATE = "Date"
    MIXED = "Mixed"
    OBJECT_ID = "mongoose.Schema.ObjectId"


class FieldCreate(BaseModel):
    """
    Model for creating a new metadata field.
    """
    id: Optional[str] = Field(None, alias="_id",
                              description="Unique identifier for the field")
    name: str = Field(..., description="The name of the vmeta field",
                      example="New Field")
    label: str = Field(..., description="A label for easy identification of the field",
                       example="New Field")
    type: VmetaFieldType = Field(
        ..., description="The type of the vmeta field", example=VmetaFieldType.STRING)
    collectionID: str = Field(..., description="The collection ID that the field belongs to",
                              example="65c21d6a593f32e0103daf25")
    description: Optional[str] = Field(
        None, description="A description of the vmeta field", example="This is a new field")
    unit: Optional[str] = Field(
        None, description="The unit of the vmeta field", example="cm")
    namingPattern: Optional[str] = Field(
        None, description="The naming pattern for the vmeta field")
    barcode: Optional[str] = Field(
        None, description="The barcode for the vmeta field", example="1234567890")
    barcode_prefix: Optional[str] = Field(
        None, description="The prefix for the barcode", example="PREFIX_")
    unique: bool = Field(
        False, description="Whether the field value must be unique", example=True)
    hidden: bool = Field(
        False, description="Whether the field is hidden", example=False)
    deprecated: bool = Field(
        False, description="Whether the field is deprecated", example=False)
    required: bool = Field(
        False, description="Whether the field is required", example=True)
    checkvalid: Optional[Any] = Field(
        None, description="Validation function for the field")
    ontology: Optional[Any] = Field(
        None, description="Ontology information for the field")
    order: Optional[int] = Field(
        None, description="The order of the field in the collection", example=1)
    default: Optional[str] = Field(
        None, description="Default value for the field", example="Default Value")
    ref: Optional[str] = Field(
        None, description="Reference to another field or collection", example="65c21d6a593f32e0103daf25")
    enum: Optional[List[str]] = Field(None, description="Enumeration values for the field", example=[
                                      "Option 1", "Option 2", "Option 3"])
    min: Optional[Any] = Field(
        None, description="Minimum value for the field", example=0)
    max: Optional[Any] = Field(
        None, description="Maximum value for the field", example=100)
    lowercase: bool = Field(
        False, description="Whether to convert the field value to lowercase", example=True)
    uppercase: bool = Field(
        False, description="Whether to convert the field value to uppercase", example=False)
    trim: bool = Field(
        False, description="Whether to trim whitespace from the field value", example=True)
    header: bool = Field(
        False, description="Whether the field is a header", example=False)
    identifier: bool = Field(
        False, description="Whether the field is an identifier", example=True)
    descriptive: bool = Field(
        False, description="Whether the field is descriptive", example=False)
    grouped: Optional[str] = Field(
        None, description="Grouping information for the field", example="Group A")
    minlength: Optional[int] = Field(
        None, description="Minimum length of the field value", example=3)
    maxlength: Optional[int] = Field(
        None, description="Maximum length of the field value", example=255)
    various: Optional[Any] = Field(None, description="Mixed type field")
    perms: Optional[List[PermEntry]] = Field(
        None, description="Permissions associated with the field")

    @field_validator('collectionID', 'id')
    @classmethod
    def validate_collection_id(cls, v):
        """Validate collectionID is a valid MongoDB ObjectId (24 hex characters)."""
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError(
                "collectionID must be a valid MongoDB ObjectId (24 hexadecimal characters)")
        return v


class FieldUpdate(BaseModel):
    """
    Model for updating an existing metadata field.
    """
    name: Optional[str] = Field(None, description="The name of the vmeta field",
                                example="New Field")
    label: Optional[str] = Field(None, description="A label for easy identification of the field",
                                 example="New Field")
    type: Optional[VmetaFieldType] = Field(
        None, description="The type of the vmeta field", example=VmetaFieldType.STRING)
    collectionID: Optional[str] = Field(None, description="The collection ID that the field belongs to",
                                        example="65c21d6a593f32e0103daf25")
    description: Optional[str] = Field(
        None, description="A description of the vmeta field", example="This is a new field")
    unit: Optional[str] = Field(
        None, description="The unit of the vmeta field", example="cm")
    namingPattern: Optional[str] = Field(
        None, description="The naming pattern for the vmeta field")
    barcode: Optional[str] = Field(
        None, description="The barcode for the vmeta field", example="1234567890")
    barcode_prefix: Optional[str] = Field(
        None, description="The prefix for the barcode", example="PREFIX_")
    unique: bool = Field(
        False, description="Whether the field value must be unique", example=True)
    hidden: bool = Field(
        False, description="Whether the field is hidden", example=False)
    deprecated: bool = Field(
        False, description="Whether the field is deprecated", example=False)
    required: bool = Field(
        False, description="Whether the field is required", example=True)
    checkvalid: Optional[Any] = Field(
        None, description="Validation function for the field")
    ontology: Optional[Any] = Field(
        None, description="Ontology information for the field")
    order: Optional[int] = Field(
        None, description="The order of the field in the collection", example=1)
    default: Optional[str] = Field(
        None, description="Default value for the field", example="Default Value")
    ref: Optional[str] = Field(
        None, description="Reference to another field or collection", example="65c21d6a593f32e0103daf25")
    enum: Optional[List[str]] = Field(None, description="Enumeration values for the field", example=[
                                      "Option 1", "Option 2", "Option 3"])
    min: Optional[Any] = Field(
        None, description="Minimum value for the field", example=0)
    max: Optional[Any] = Field(
        None, description="Maximum value for the field", example=100)
    lowercase: bool = Field(
        False, description="Whether to convert the field value to lowercase", example=True)
    uppercase: bool = Field(
        False, description="Whether to convert the field value to uppercase", example=False)
    trim: bool = Field(
        False, description="Whether to trim whitespace from the field value", example=True)
    header: bool = Field(
        False, description="Whether the field is a header", example=False)
    identifier: bool = Field(
        False, description="Whether the field is an identifier", example=True)
    descriptive: bool = Field(
        False, description="Whether the field is descriptive", example=False)
    grouped: Optional[str] = Field(
        None, description="Grouping information for the field", example="Group A")
    minlength: Optional[int] = Field(
        None, description="Minimum length of the field value", example=3)
    maxlength: Optional[int] = Field(
        None, description="Maximum length of the field value", example=255)
    various: Optional[Any] = Field(None, description="Mixed type field")
    perms: Optional[List[PermEntry]] = Field(
        None, description="Permissions associated with the field")


class DatasetFileInfo(BaseModel):
    """
    Model representing file information in a dataset.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(
        None, alias="_id", description="Unique identifier for the file")
    name: str = Field(..., description="Name of the file")
    path: str = Field(..., description="Path to the file")
    size: Optional[int] = Field(None, description="Size of the file in bytes")
    mimeType: Optional[str] = Field(None, description="MIME type of the file")
    checksum: Optional[str] = Field(None, description="Checksum of the file")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata for the file")


class DatasetResponse(BaseModel):
    """
    Model representing a dataset response.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id",
                    description="Unique identifier for the dataset")
    name: str = Field(..., description="Name of the dataset")
    description: Optional[str] = Field(
        None, description="Description of the dataset")
    canvasID: str = Field(...,
                           description="ID of the canvas this dataset belongs to")
    files: Optional[List[DatasetFileInfo]] = Field(
        default_factory=list, description="Files in the dataset")
    owner: Optional[OwnerModel] = Field(
        None, description="Owner of the dataset")
    lastUpdatedUser: Optional[str] = Field(
        None, description="ID of the user who last updated the dataset")
    createdAt: Optional[datetime] = Field(
        None, description="Creation timestamp")
    updatedAt: Optional[datetime] = Field(
        None, description="Last update timestamp")


RESERVED_KEYS = {"_id", "active", "creationDate",
                 "lastUpdateDate", "owner", "lastUpdatedUser"}


class DataEntryUpdate(BaseModel):
    """
    Schema for updating vmeta data.
    Allows arbitrary extra fields but forbids reserved system fields.
    """
    perms: Optional[Optional[List[PermEntry]]] = None

    class Config:
        extra = "allow"  # equivalent to Joi's .unknown()

    @field_validator('*', mode='before')
    @classmethod
    def forbid_reserved_fields(cls, v, info):
        """Prevent modification of reserved system fields"""
        if info.field_name in RESERVED_KEYS:
            raise ValueError(
                f"Field '{info.field_name}' is forbidden and cannot be modified")
        return v

    def dict(self, **kwargs) -> Dict[str, Any]:
        """Override dict to ensure reserved fields are never included"""
        data = super().model_dump(**kwargs)
        return {k: v for k, v in data.items() if k not in RESERVED_KEYS}


ALLOWED_OPERATORS = {"ne", "gt", "gte", "lt", "lte", "in",
                     "nin", "regex", "not", "exists", "or", "and", "eq"}


class SortOrder(str, Enum):
    """Enum for sort order values"""
    DESC = "desc"
    ASC = "asc"


# Type for filter operator values
FilterOperatorValue = Union[str, int, float, bool, List[Any]]

# Type for filter operators object
FilterOperators = Dict[str, FilterOperatorValue]

# Type for filter values (can be primitive or operator object)
FilterValue = Union[str, int, float, bool,
                    datetime, List[Any], FilterOperators]


class DynamicFilter(BaseModel):
    """
    Dynamic filter model that matches the Joi dynamicFilterSchema pattern.
    Allows arbitrary field names with flexible value types including operators.
    """

    class Config:
        extra = "allow"  # Allow arbitrary field names

    # Changed from @validator('*', pre=True)
    @field_validator('*', mode='before')
    @classmethod
    def validate_filter_field(cls, v, field):
        """Validate each filter field value"""
        if v is None:
            return v

        # Handle operator objects
        if isinstance(v, dict):
            validated_operators = {}
            for op_key, op_value in v.items():
                # Validate operator key is allowed
                if op_key not in ALLOWED_OPERATORS:
                    raise ValueError(
                        f"Invalid operator '{op_key}'. Allowed operators: {ALLOWED_OPERATORS}")

                # Validate operator value types
                if not isinstance(op_value, (str, int, float, bool, list)):
                    raise ValueError(
                        f"Invalid operator value type for '{op_key}'")

                # Allow empty strings
                if isinstance(op_value, str):
                    validated_operators[op_key] = op_value
                elif isinstance(op_value, list):
                    validated_operators[op_key] = op_value
                else:
                    validated_operators[op_key] = op_value

            return validated_operators

        # Handle primitive values
        if isinstance(v, (str, int, float, bool, list)):
            return v

        # Handle datetime objects
        if isinstance(v, datetime):
            return v

        raise ValueError(f"Invalid filter value type: {type(v)}")


class SearchParams(BaseModel):
    """
    Schema for searching vmeta data with filtering, sorting, and pagination.
    """
    filter: Optional[DynamicFilter] = Field(
        None,
        description="Dynamic filter object supporting MongoDB-style operators",
        example={
            "name": "test",
            "owner.username": "test",
            "creationDate": {"gte": "2024-01-01", "lt": "2024-12-31"},
            "active": True
        }
    )

    sort: Optional[str] = Field(
        None,
        pattern=r"^[,\w]+$",
        description="Comma-separated list of fields to sort by",
        example="name,creationDate"
    )

    order: Optional[SortOrder] = Field(
        None,
        description="Sort order direction",
        example="asc"
    )

    fields: Optional[str] = Field(
        None,
        pattern=r"^[,\w]+$",
        description="Comma-separated list of fields to return",
        example="name,description"
    )

    take: Optional[int] = Field(
        None,
        ge=0,
        description="Number of items to return (limit)",
        example=10
    )

    skip: Optional[int] = Field(
        None,
        ge=0,
        description="Number of items to skip (offset)",
        example=0
    )

    class Config:
        json_schema_extra = {
            "example": {
                "filter": {
                    "name": "test",
                    "owner.username": "test",
                    "creationDate": {"gte": "2024-01-01"},
                    "active": True
                },
                "sort": "name",
                "order": "asc",
                "fields": "name,description",
                "take": 10,
                "skip": 0
            }
        }


class SearchResponse(BaseModel):
    """
    Model representing a search response.
    """
    data: List[Any] = Field(..., description="List of search results")
    total: Optional[int] = Field(
        None, description="Total number of matching documents")
    limit: Optional[int] = Field(
        None, description="Limit applied to the query")
    skip: Optional[int] = Field(
        None, description="Number of documents skipped")


class FileAddRequest(BaseModel):
    """
    Model for adding files to a dataset.
    """
    canvasID: str = Field(..., description="The ID of the study tracker canvas",
                           example="66269972dc000cff1c8a54b0")
    file: Dict[str, Any] = Field(...,
                                 description="File Object associated with the dataset")

    @field_validator('canvasID')
    @classmethod
    def validate_canvas_id(cls, v):
        """Validate canvasId is a valid MongoDB ObjectId (24 hex characters)."""
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError(
                "canvasId must be a valid MongoDB ObjectId (24 hexadecimal characters)")
        return v
