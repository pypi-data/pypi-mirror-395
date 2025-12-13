import pydantic

from classiq.interface.backend.provider_config.provider_config import ProviderConfig


class BraketConfig(ProviderConfig):
    """
    Configuration specific to Amazon Braket.

    Attributes:
        braket_access_key_id (str | None):
            The access key id of user with full braket access

        braket_secret_access_key (str | None):
            The secret key assigned to the access key id for the user with full braket access.

        s3_bucket_name (str | None):
            The name of the S3 bucket where results and other related data will be stored.
            This field should contain a valid S3 bucket name under your AWS account.

        s3_folder (pydantic_backend.PydanticS3BucketKey | None):
            The folder path within the specified S3 bucket. This allows for organizing
            results and data under a specific directory within the S3 bucket.
    """

    braket_access_key_id: str | None = pydantic.Field(
        default=None,
        description="Key id assigned to user with credentials to access Braket service",
    )
    braket_secret_access_key: str | None = pydantic.Field(
        default=None,
        description="Secret access key assigned to user with credentials to access Braket service",
    )
    s3_bucket_name: str | None = pydantic.Field(
        default=None, description="S3 Bucket Name"
    )
    s3_folder: str | None = pydantic.Field(
        default=None, description="S3 Folder Path Within The S3 Bucket"
    )
