from datetime import datetime
from .base import Base
from cidc_api.models.types import ChecksumType, FileFormat


class File(Base):
    # The unique internal identifier for this File record
    file_id: int | None = None

    # The unique identifier for the associated trial
    trial_id: int | None = None

    # The version number of the trial dataset
    version: str | None = None

    # The unique internal identifier of the institution that created this file
    creator_id: int | None = None

    # A description of the file's purpose and contents
    description: str | None = None

    # A unique UUID to identify the file across systems
    uuid: str

    # The name of the file
    file_name: str

    # The url of the file object as found in cloud storage, a bucket, external system, etc.
    object_url: str

    # The timestamp of when CIDC received the file
    uploaded_timestamp: datetime

    # The size of the file's contents, in bytes
    file_size_bytes: int

    # The value of the checksum calculated for the file's contents
    checksum_value: str

    # The type of the checksum calculated for the file's contents
    checksum_type: ChecksumType

    # A description or abbreviation of the format of the file's contents, possibly different than the extension
    file_format: FileFormat
