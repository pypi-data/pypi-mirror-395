import uuid
from sqlalchemy import Column, String, ForeignKey, JSON, Text, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass
from typing import Dict, Optional

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    storage_connections = relationship("StorageConnection", back_populates="user")

class StorageProviderConfig(Base):
    __tablename__ = "storage_provider_configs"
    id = Column(UUID(as_uuid=True), primary_key=True)
    encryptedCredentials = Column('encryptedCredentials', JSON, nullable=False, default={})
    scanRootPath = Column('scanRootPath', String)
    configuration = Column('configuration', JSON, nullable=False, default={})

class StorageConnection(Base):
    __tablename__ = "storage_connections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column('providerType', String)
    user_id = Column('userId', UUID(as_uuid=True), ForeignKey("users.id"))
    storage_provider_config_id = Column('storageProviderConfigId', UUID(as_uuid=True), ForeignKey("storage_provider_configs.id"))
    # host and port are now stored in encryptedCredentials JSON
    encrypted_credentials = Column('encryptedCredentials', Text)
    
    user = relationship("User", back_populates="storage_connections")
    config = relationship("StorageProviderConfig")

class Model(Base):
    __tablename__ = 'models'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    file_size = Column('fileSize', BigInteger, nullable=True)
    file_type = Column('fileType', String, nullable=True)  # Single file type
    file_name = Column('fileName', String, nullable=True)  # Original filename
    source_path = Column('sourcePath', String, nullable=True)  # Path in storage
    owner_id = Column('ownerId', UUID(as_uuid=True), nullable=True)  # Owner reference
    library_id = Column('libraryId', UUID(as_uuid=True), nullable=True)  # Library reference

    storage_items = relationship("StorageItem", back_populates="platform_model")

class StorageItem(Base):
    __tablename__ = 'storage_items'
    id = Column(UUID(as_uuid=True), primary_key=True)
    provider_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    connection_id = Column(UUID(as_uuid=True), ForeignKey('storage_connections.id'))
    platform_model_id = Column(UUID(as_uuid=True), ForeignKey('models.id'), nullable=True)
    size = Column(BigInteger)
    last_modified = Column('last_modified', DateTime)
    
    platform_model = relationship("Model", back_populates="storage_items")
    metamodel_storage_items = relationship("MetamodelStorageItem", back_populates="storage_item")


class Metamodel(Base):
    __tablename__ = 'metamodels'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    library_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String, nullable=False)
    confidence_score = Column('confidence_score', String, nullable=True)
    
    metamodel_storage_items = relationship("MetamodelStorageItem", back_populates="metamodel")


class MetamodelStorageItem(Base):
    __tablename__ = 'metamodel_storage_items'
    metamodel_id = Column(UUID(as_uuid=True), ForeignKey('metamodels.id'), primary_key=True)
    storage_item_id = Column(UUID(as_uuid=True), ForeignKey('storage_items.id'), primary_key=True)
    
    metamodel = relationship("Metamodel", back_populates="metamodel_storage_items")
    storage_item = relationship("StorageItem", back_populates="metamodel_storage_items")


# Dataclasses for job data remain useful
@dataclass
class FilePath:
    value: str


@dataclass
class DownloadJobData:
    """
    Job data for file download requests.
    Supports both new format (storageLocation) and legacy format (storageConnectionId + filePath).
    """
    modelId: str
    originalJobName: str = ""
    # New format fields
    storageLocation: Optional[Dict] = None  # New: {storageConnectionId, path}
    ownerId: Optional[str] = None  # Optional - retrieved from StorageConnection if not provided
    # Legacy format fields  
    storageConnectionId: Optional[str] = None  # Legacy: top-level storage connection ID
    filePath: Optional[Dict] = None  # Legacy: {props: {value: "path"}}