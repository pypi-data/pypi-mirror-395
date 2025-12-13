from pydantic import BaseModel, Field, model_validator
from typing import Optional
from enum import IntEnum


class ConfigParameter(BaseModel):
    """
    Model representing a parameter in the process configuration.
    """
    parameterId: Optional[int] = Field(...,
                                       description="Id number of the parameter")
    displayName: str = Field(
        ..., description="Display name for the parameter")
    operator: Optional[str] = Field(
        None, description="Operator for the parameter")
    operatorContent: Optional[str] = Field(
        None, description="Content for the operator")
    optional: bool = Field(
        False, description="Whether the parameter is optional")
    test: str = Field(
        ..., description="Test for the parameter, if applicable")


class Parameter(BaseModel):
    """
    Input model for creating a parameter in the process configuration.
    """
    name: str = Field(..., description="Name of the parameter")
    qualifier: str = Field(
        ..., description="Qualifier for the parameter")
    fileType: Optional[str] = Field(
        None, description="File type for the parameter")

    @model_validator(mode="after")
    def conditional_required(cls, model):
        if model.qualifier != "val" and model.fileType is None:
            raise ValueError(
                "Field 'fileType' is required when type is not 'val'")
        return model


class ServerParameterResponse(BaseModel):
    """
    Output model for a parameter in the process configuration.
    """
    id: int = Field(
        ..., description="Unique identifier for the parameter")
    name: str = Field(..., description="Name of the parameter")
    qualifier: str = Field(
        ..., description="Qualifier for the parameter")
    fileType: Optional[str] = Field(
        None, description="File type for the parameter")

    @model_validator(mode="after")
    def conditional_required(cls, model):
        if model.qualifier != "val" and model.fileType is None:
            raise ValueError(
                "Field 'fileType' is required when type is not 'val'")
        return model


class ViewPermissionsEnum(IntEnum):
    """
    Enum representing view permissions for a process.
    """
    UserOwned = 3,
    GroupShared = 15,
    Public = 63


class PermissionSettings(BaseModel):
    """
    Model representing permission settings for a process.
    """
    viewPermissions: ViewPermissionsEnum = Field(
        ..., description="View permissions for the process")
    sharedGroupId: Optional[int] = Field(
        None,
        description="The id of the group to share with",
    )
    writeGroupIds: list[int] = Field(
        default_factory=list,
        description="A list of groups to allow process editing",
    )


class CreateProcessConfigInput(BaseModel):
    """
    Input model for creating a process configuration.
    """
    name: str = Field(..., description="Name of the process")
    menu_group_name: str = Field(..., description="Name of the menu group")
    summary: Optional[str] = Field(..., description="Summary of the process")
    inputParameters: list[ConfigParameter] = Field(
        ...,
        description="List of input parameters for the process",
    )
    outputParameters: list[ConfigParameter] = Field(
        ...,
        description="List of output parameters for the process",
    )
    script_body: Optional[str] = Field(
        ...,
        description="Script body for the process",
    )
    script_language: Optional[str] = Field(
        description="Programming language of the script",
        default="bash"
    )
    script_header: Optional[str] = Field(
        None,
        description="Header for the script, if applicable",
    )
    script_footer: Optional[str] = Field(
        None,
        description="Footer for the script, if applicable",
    )
    permission_settings: Optional[PermissionSettings] = Field(
        None,
        description="Permission settings for the process",
    )
    revision_comment: Optional[str] = Field(
        description="Comment for the revision of the process",
        default="Initial revision"
    )


class ProcessScript(BaseModel):
    """
    Model representing the script for a process.
    """
    body: str = Field(..., description="Body of the script")
    header: str = Field(
        None, description="Header of the script, if applicable")
    footer: str = Field(
        None, description="Footer of the script, if applicable")
    language: str = Field(
        ..., description="Programming language of the script")


class ProcessConfig(BaseModel):
    """
    Output model for creating a process configuration.
    """
    name: str = Field(..., description="Name of the process")
    summary: str = Field(
        ...,
        description="Summary of the process",
    )
    menuGroupId: int = Field(
        ...,
        description="Id of the menu group for the process",
    )

    inputParameters: list[ConfigParameter] = Field(
        ...,
        description="List of input parameters for the process",
    )
    outputParameters: list[ConfigParameter] = Field(
        ...,
        description="List of output parameters for the process",
    )
    revisionComment: str = Field(
        ...,
        description="Comment for the revision of the process",)
    script: ProcessScript = Field(
        ...,
        description="Script for the process",
    )
    permissionSettings: PermissionSettings = Field(
        ...,
        description="Permission settings for the process",
    )


class ParameterResponse(BaseModel):
    """
    Model representing a parameter in a process.
    FIXME: Have this model inherit from ConfigParameter when parameter names are made consistent."""
    parameter_id: int = Field(
        ...,
        description="Unique identifier for the parameter",
    )
    sname: str = Field(
        ...,
        description="Short name of the parameter",
    )
    id: int = Field(
        ...,
        description="Unique identifier for the process",
    )
    operator: Optional[str] = Field(
        None,
        description="Operator for the parameter, if applicable",
    )
    closure: Optional[str] = Field(
        None,
        description="Closure for the parameter, if applicable",
    )
    reg_ex: Optional[str] = Field(
        None,
        description="Regular expression for the parameter, if applicable",
    )
    optional: Optional[str] = Field(
        None,
        description="Indicates if the parameter is optional",
    )
    name: str = Field(
        ...,
        description="Name of the process",
    )
    file_type: str = Field(
        ...,
        description="File type associated with the process",
    )
    qualifier: str = Field(
        ...,
        description="Qualifier for the process",
    )


class ListParametersResponse(BaseModel):
    """
    Model representing a list of processes.
    """
    data: list[ParameterResponse] = Field(
        ...,
        description="List of processes",
    )


class ProcessResponse(BaseModel):
    """
    Model representing a process.
    FIXME: Have this model inherit from ProcessConfig when parameter names are made consistent.
    """
    id: int = Field(
        ...,
        description="Unique identifier for the process",
    )
    inputs: Optional[list[ParameterResponse]] = Field(
        None,
        description="List of input parameters for the process",
    )
    outputs: Optional[list[ParameterResponse]] = Field(
        None,
        description="List of output parameters for the process",
    )
    process_group_id: Optional[int] = Field(
        ...,
        description="Id of the process group",
    )
    name: str = Field(
        ...,
        description="Name of the process",
    )
    summary: Optional[str] = Field(
        None,
        description="Summary of the process",
    )
    script: Optional[str] = Field(
        None,
        description="Script associated with the process",
    )
    script_mode: Optional[str] = Field(
        None,
        description="Mode of the script",
    )
    script_header: Optional[str] = Field(
        None,
        description="Header of the script",
    )
    script_footer: Optional[str] = Field(
        None,
        description="Footer of the script",
    )
    script_mode_header: Optional[str] = Field(
        None,
        description="Header for the script mode",
    )
    run_pid: Optional[int] = Field(
        None,
        description="Process ID for the running process",
    )
    run_uuid: Optional[str] = Field(
        None,
        description="UUID for the running process",
    )
    run_status: Optional[str] = Field(
        None,
        description="Status of the running process",
    )
    script_test_mode: Optional[str] = Field(
        None,
        description="Test mode for the script",
    )
    script_test: Optional[str] = Field(
        None,
        description="Test script",
    )
    singu_options: Optional[str] = Field(
        None,
        description="Singularity options for the process",
    )
    singu_img: Optional[str] = Field(
        None,
        description="Singularity image for the process",
    )
    docker_opt: Optional[str] = Field(
        None,
        description="Docker options for the process",
    )
    docker_img: Optional[str] = Field(
        None,
        description="Docker image for the process",
    )
    singu_check: Optional[int] = Field(
        None,
        description="Check for Singularity",
    )
    docker_check: Optional[int] = Field(
        None,
        description="Check for Docker",
    )
    test_work_dir: Optional[str] = Field(
        None,
        description="Test working directory for the process",
    )
    test_env: Optional[str] = Field(
        None,
        description="Test environment for the process",
    )
    publish: Optional[int] = Field(
        None,
        description="Publish status of the process",
    )
    publicly_searchable: Optional[str] = Field(
        None,
        description="Whether the process is publicly searchable",
    )
    owner_id: Optional[int] = Field(
        None,
        description="Owner ID of the process",
    )
    group_id: Optional[int] = Field(
        None,
        description="Group ID of the process",
    )
    write_group_id: Optional[str] = Field(
        None,
        description="Write group ID for the process",
    )
    perms: Optional[int] = Field(
        None,
        description="Permissions for the process",
    )
    deleted: Optional[int] = Field(
        None,
        description="Deletion status of the process",
    )
    date_created: Optional[str] = Field(
        None,
        description="Creation date of the process",
    )
    date_modified: Optional[str] = Field(
        None,
        description="Last modified date of the process",
    )
    last_modified_user: Optional[str] = Field(
        None,
        description="User who last modified the process",
    )
    rev_id: Optional[int] = Field(
        None,
        description="Revision ID of the process",
    )
    rev_comment: Optional[str] = Field(
        None,
        description="Comment for the revision of the process",
    )
    process_gid: Optional[int] = Field(
        None,
        description="Group ID of the process",
    )
    process_rev_uuid: Optional[str] = Field(
        None,
        description="Revision UUID of the process",
    )
    process_uuid: Optional[str] = Field(
        None,
        description="UUID of the process",
    )


class ProcessSummaryResponse(BaseModel):
    """
    Model representing a summary of a process.
    """
    id: int = Field(
        ...,
        description="Unique identifier for the process",
    )
    name: str = Field(
        ...,
        description="Name of the process",
    )
    summary: Optional[str] = Field(
        None,
        description="Summary of the process",
    )
