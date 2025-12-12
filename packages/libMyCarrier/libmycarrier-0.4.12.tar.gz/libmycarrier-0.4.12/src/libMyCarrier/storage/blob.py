from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class Blob:
    """
    Class for interacting with Azure Blob Storage.

    Methods:
        - __init__(account_url):
            Initializes the Blob class instance.

            :param account_url: The account URL for the Azure Blob Storage.

        - download_blob(container_name, blob_name):
            Downloads a storage from Azure Blob Storage.

            :param container_name: The name of the container.
            :param blob_name: The name of the storage.
            :return: The downloaded storage.
    """

    def __init__(self, account_url):
        """
        Initializes the Blob class instance.
        Args:
            account_url: The account URL for the Azure Blob Storage.
        """
        default_credential = DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    def download_blob(self, container_name, blob_name):
        """
        Downloads a storage from Azure Blob Storage.

        Args:
            container_name: The name of the container.
            blob_name: The name of the storage.

        Returns: The downloaded storage.

        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            return blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
        except Exception as e:
            raise e

    def delete_blob(self, container_name, blob_name):
        """
        Deletes a storage from Azure Blob Storage.

        Args:
            container_name: The name of the container.
            blob_name: The name of the storage.

        Returns: None

        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            if blob_client.exists():
                blob_client.delete_blob()
                print(f"Blob {blob_name} deleted from container {container_name}.")
            else:
                print(f"Blob {blob_name} not found in container {container_name}, skipping deletion.")

        except Exception as e:
            raise e
