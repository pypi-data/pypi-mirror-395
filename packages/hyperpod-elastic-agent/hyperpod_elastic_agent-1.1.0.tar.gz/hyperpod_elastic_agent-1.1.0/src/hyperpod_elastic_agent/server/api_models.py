from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator


class UpdateRequest(BaseModel):
    """
    Pydantic model for the /update API request.
    
    This model provides automatic validation and type conversion for the request data.
    It ensures all required fields are present and have the correct types.
    """
    # Required fields
    rank: int = Field(..., description="Global rank of this node in the job")
    nnodes: int = Field(..., description="Total number of nodes in the job")
    faultCount: int = Field(..., description="Number of faults encountered in the job")
    master_addr: str = Field(..., description="Address of the master node")
    master_port: Union[int, str] = Field(..., description="Port of the master node")
    
    # Optional fields
    log_monitoring_configuration: Optional[List[Dict[str, Any]]] = Field(
        None, description="Configuration for log monitoring"
    )
    ipVersion: Optional[str] = Field(
        None, description="IP version to use (IPv4 or IPv6)"
    )
    rankIps: Optional[List[Dict[str, Union[str, int]]]] = Field(
        None, description="List of IP addresses for each rank"
    )
    worker_data: Optional[Any] = Field(
        None, description="Additional data for workers"
    )
    spare: Union[bool, int] = Field(
        False, description="Whether this node is a spare node"
    )
    
    # Validators to handle type conversions
    @field_validator('master_addr')
    @classmethod
    def validate_master_addr(cls, v):
        if not v:
            raise ValueError("Empty master_addr received from operator")
        return v
    
    @field_validator('master_port')
    @classmethod
    def validate_master_port(cls, v):
        if isinstance(v, str):
            if not v:  # Handle empty string
                return 0  # Default value, will be overridden if master_addr is valid
            return int(v)
        return v
    
    @field_validator('spare')
    @classmethod
    def validate_spare(cls, v):
        if isinstance(v, int):
            return bool(v)
        return v


class StopRequest(BaseModel):
    """
    Pydantic model for the /stop API request.
    
    This model provides automatic validation for the request data.
    """
    restart_mode: Optional[str] = Field(default="ipr", description="Mode for restarting the agent")
    is_graceful: Optional[bool] = Field(default=None, description="Whether to use graceful shutdown (SIGUSR1) or immediate termination")
    timeout: Optional[int] = Field(default=None, description="Timeout in seconds before escalating to SIGKILL")


class StartRequest(BaseModel):
    """
    Pydantic model for the /start API request.
    
    This model provides automatic validation and type conversion for the request data.
    It ensures all required fields are present and have the correct types.
    """
    # Required fields
    rank: int = Field(..., description="Global rank of this node in the job")
    nnodes: int = Field(..., description="Total number of nodes in the job")
    faultCount: int = Field(..., description="Total number of restarts encountered in the job")
    master_addr: str = Field(..., description="Address of the master node")
    master_port: Union[int, str] = Field(..., description="Port of the master node")
    
    log_monitoring_configuration: Optional[List[Dict[str, Any]]] = Field(
        None, description="Configuration for log monitoring"
    )
    ipVersion: Optional[str] = Field(
        None, description="version for update requests"
    )
    rankIps: Optional[List[Dict[str, Union[str, int]]]] = Field(
        None, description="List of IP addresses for each rank"
    )
    worker_data: Optional[Any] = Field(
        None, description="Aggregatd data from workers"
    )
    spare: Union[bool, int] = Field(
        False, description="Whether this node is a spare node"
    )
    progress: Dict[str, Any] = Field(
        default_factory=dict, description="Progress information"
    )
    
    # Validators to handle type conversions
    @field_validator('master_addr')
    @classmethod
    def validate_master_addr(cls, v):
        if not v:
            raise ValueError("Empty master_addr received from operator")
        return v
    
    @field_validator('master_port')
    @classmethod
    def validate_master_port(cls, v):
        if isinstance(v, str):
            if not v:  # Handle empty string
                return 0  # Default value, will be overridden if master_addr is valid
            return int(v)
        return v
    
    @field_validator('spare')
    @classmethod
    def validate_spare(cls, v):
        if isinstance(v, int):
            return bool(v)
        return v
