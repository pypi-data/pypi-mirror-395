from copy import deepcopy
from typing import Optional, Union
from .models.domain.metadata import (
    CanvasCreate,
    CanvasUpdate,
    CollectionCreate,
    CollectionUpdate,
    FieldCreate,
    FieldUpdate,
    DataEntryUpdate,
    SearchParams,
    FileAddRequest,
)


class Metadata:
    """
    A class for managing metadata in the ViaFoundry API.

    Attributes:
        client (ViaFoundryClient): The client instance to interact with the API.
    """

    def __init__(self, client) -> None:
        """
        Initializes the Metadata class.

        Args:
            client (ViaFoundryClient): The client instance to interact with.
        """
        self.client = client

    # --- Canvas Methods ---
    def search_canvas(self, search_params: Optional[Union[dict, SearchParams]] = None) -> dict:
        """
        Searches for the canvas using the metadata API.

        Args:
            search_params (dict or SearchParams, optional): Search parameters for the canvas search. Defaults to None.

        Returns:
            dict: The search results for the canvas.

        Raises:
            Exception: If the search fails.
        """
        try:
            endpoint = "/api/v1/vmeta/canvas/search"
            if isinstance(search_params, SearchParams):
                data = search_params.model_dump(exclude_none=True)
            else:
                data = search_params if search_params is not None else {}
            return self.client.call("POST", endpoint, data=data)
        except Exception as e:
            raise Exception(
                f"Error 2001: Failed to search canvas: {e}") from e

    def create_canvas(self, canvas_data: Union[dict, CanvasCreate]) -> dict:
        """
        Creates a new metadata canvas.

        Args:
            canvas_data (dict or CanvasCreate): Data required to create the canvas.

        Returns:
            dict: The created canvas.

        Raises:
            Exception: If the creation fails.
        """
        try:
            if isinstance(canvas_data, CanvasCreate):
                data = canvas_data.model_dump(exclude_none=True)
            else:
                data = canvas_data
            return self.client.call("POST", "/api/v1/vmeta/canvas/create", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2002: Failed to create canvas: {e}") from e

    def get_canvas(self, canvas_id: str) -> dict:
        """
        Retrieves a canvas by its ID.

        Args:
            canvas_id (str): The ID of the canvas.

        Returns:
            dict: The canvas details.

        Raises:
            Exception: If retrieval fails.
        """
        try:
            return self.client.call("GET", f"/api/v1/vmeta/canvas/{canvas_id}")
        except Exception as e:
            raise Exception(
                f"Error 2003: Failed to get canvas {canvas_id}: {e}") from e

    def update_canvas(self, canvas_id: str, update_data: Union[dict, CanvasUpdate]) -> dict:
        """
        Updates an existing canvas.

        Args:
            canvas_id (str): The ID of the canvas to update.
            update_data (dict or CanvasUpdate): The data to update in the canvas.

        Returns:
            dict: The updated canvas.

        Raises:
            Exception: If update fails.
        """
        try:
            if isinstance(update_data, CanvasUpdate):
                data = update_data.model_dump(exclude_none=True)
            else:
                data = update_data
            return self.client.call("PATCH", f"/api/v1/vmeta/canvas/{canvas_id}", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2004: Failed to update canvas {canvas_id}: {e}") from e

    def delete_canvas(self, canvas_id: str) -> dict:
        """
        Deletes a canvas by its ID.

        Args:
            canvas_id (str): The ID of the canvas to delete.

        Returns:
            dict: The deletion result.

        Raises:
            Exception: If deletion fails.
        """
        try:
            return self.client.call("DELETE", f"/api/v1/vmeta/canvas/{canvas_id}")
        except Exception as e:
            raise Exception(
                f"Error 2005: Failed to delete canvas {canvas_id}: {e}") from e

    # --- Collection Methods ---
    def search_collections(self, search_params: Optional[Union[dict, SearchParams]] = None) -> dict:
        """
        Searches for collections.

        Args:
            search_params (dict or SearchParams, optional): Collection search filters. Defaults to None.

        Returns:
            dict: The list of collections.

        Raises:
            Exception: If the search fails.
        """
        try:
            if isinstance(search_params, SearchParams):
                data = search_params.model_dump(exclude_none=True)
            else:
                data = search_params or {}
            return self.client.call("POST", "/api/v1/vmeta/collection/search", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2011: Failed to search collections: {e}") from e

    def create_collection(self, collection_data: Union[dict, CollectionCreate]) -> dict:
        """
        Creates a new collection.

        Args:
            collection_data (dict or CollectionCreate): The collection data.

        Returns:
            dict: The created collection.

        Raises:
            Exception: If creation fails.
        """
        try:
            if isinstance(collection_data, CollectionCreate):
                data = collection_data.model_dump(exclude_none=True)
            else:
                data = collection_data
            return self.client.call("POST", "/api/v1/vmeta/collection/create", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2012: Failed to create collection: {e}") from e

    def get_collection(self, collection_id: str) -> dict:
        """
        Retrieves a collection by ID.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            dict: The collection details.

        Raises:
            Exception: If retrieval fails.
        """
        try:
            return self.client.call("GET", f"/api/v1/vmeta/collection/{collection_id}")
        except Exception as e:
            raise Exception(
                f"Error 2013: Failed to get collection {collection_id}: {e}") from e

    def update_collection(self, collection_id: str, update_data: Union[dict, CollectionUpdate]) -> dict:
        """
        Updates a collection.

        Args:
            collection_id (str): The ID of the collection.
            update_data (dict or CollectionUpdate): The data to update.

        Returns:
            dict: The updated collection.

        Raises:
            Exception: If update fails.
        """
        try:
            if isinstance(update_data, CollectionUpdate):
                data = update_data.model_dump(exclude_none=True)
            else:
                data = update_data
            return self.client.call("PATCH", f"/api/v1/vmeta/collection/{collection_id}", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2014: Failed to update collection {collection_id}: {e}") from e

    def delete_collection(self, collection_id: str) -> dict:
        """
        Deletes a collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            dict: Deletion confirmation.

        Raises:
            Exception: If deletion fails.
        """
        try:
            return self.client.call("DELETE", f"/api/v1/vmeta/collection/{collection_id}")
        except Exception as e:
            raise Exception(
                f"Error 2015: Failed to delete collection {collection_id}: {e}") from e

    # --- Field Methods ---
    def search_fields(self, search_params: Optional[Union[dict, SearchParams]] = None) -> dict:
        """
        Searches for metadata fields.

        Args:
            search_params (dict or SearchParams, optional): Filters for the field search.

        Returns:
            dict: The list of fields.

        Raises:
            Exception: If the search fails.
        """
        try:
            if isinstance(search_params, SearchParams):
                data = search_params.model_dump(exclude_none=True)
            else:
                data = search_params or {}
            return self.client.call("POST", "/api/v1/vmeta/field/search", data=data)
        except Exception as e:
            raise Exception(f"Error 2021: Failed to search fields: {e}") from e

    def create_field(self, field_data: Union[dict, FieldCreate]) -> dict:
        """
        Creates a new metadata field.

        Args:
            field_data (dict or FieldCreate): The data for the new field.

        Returns:
            dict: The created field.

        Raises:
            Exception: If creation fails.
        """
        try:
            if isinstance(field_data, FieldCreate):
                data = field_data.model_dump(exclude_none=True)
            else:
                data = field_data
            return self.client.call("POST", "/api/v1/vmeta/field/create", data=data)
        except Exception as e:
            raise Exception(f"Error 2022: Failed to create field: {e}") from e

    def get_field(self, field_id: str) -> dict:
        """
        Retrieves a metadata field by ID.

        Args:
            field_id (str): ID of the field.

        Returns:
            dict: Field details.

        Raises:
            Exception: If retrieval fails.
        """
        try:
            return self.client.call("GET", f"/api/v1/vmeta/field/{field_id}")
        except Exception as e:
            raise Exception(
                f"Error 2023: Failed to get field {field_id}: {e}") from e

    def update_field(self, field_id: str, update_data: Union[dict, FieldUpdate]) -> dict:
        """
        Updates a metadata field.

        Args:
            field_id (str): ID of the field to update.
            update_data (dict or FieldUpdate): Updated field data.

        Returns:
            dict: Updated field.

        Raises:
            Exception: If update fails.
        """
        try:
            if isinstance(update_data, FieldUpdate):
                data = update_data.model_dump(exclude_none=True)
            else:
                data = update_data
            return self.client.call("PATCH", f"/api/v1/vmeta/field/{field_id}", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2024: Failed to update field {field_id}: {e}") from e

    def delete_field(self, field_id: str) -> dict:
        """
        Deletes a metadata field.

        Args:
            field_id (str): ID of the field.

        Returns:
            dict: Deletion confirmation.

        Raises:
            Exception: If deletion fails.
        """
        try:
            return self.client.call("DELETE", f"/api/v1/vmeta/field/{field_id}")
        except Exception as e:
            raise Exception(
                f"Error 2025: Failed to delete field {field_id}: {e}") from e

    def get_collection_fields(self, collection_id: str) -> dict:
        """
        Retrieves a metadata field by collection_id.

        Args:
            collection_id (str): collectionID of the field.

        Returns:
            dict: Field details.

        Raises:
            Exception: If retrieval fails.
        """
        try:
            search_params = {
                "filter": {
                    "collectionID": collection_id
                }
            }
            return self.search_fields(search_params)
        except Exception as e:
            raise Exception(
                f"Error 2026: Failed to get fields for collection: {collection_id}: {e}") from e

    def get_canvas_fields(self, canvas_id: str) -> dict:
        """
        Retrieves all metadata fields for a given canvas by accumulating fields from all its collections.

        Args:
            canvas_id (str): canvasID of the field.

        Returns:
            dict: All fields for the canvas, accumulated in a single dictionary with a "data" key containing a list.

        Raises:
            Exception: If retrieval fails.
        """
        try:
            search_params = {
                "filter": {
                    "canvasID": canvas_id
                }
            }
            collections = self.search_collections(search_params)
            all_fields = []
            for collection in collections["data"]:
                fields = self.get_collection_fields(collection['_id'])

                # fields["data"] is expected to be a list of field dicts
                if "data" in fields and isinstance(fields["data"], list):
                    all_fields.extend(fields["data"])

            return {"data": all_fields}
        except Exception as e:
            raise Exception(
                f"Error 2027: Failed to get fields for canvas {canvas_id}: {e}") from e

    # --- Dataset Methods ---

    def search_dataset_files(self, dataset_id: str, filter_data: Optional[Union[dict, SearchParams]] = None) -> dict:
        """
        Lists files associated with a dataset.

        Args:
            dataset_id (str): ID of the dataset.
            filter_data (dict, optional): Filter criteria.

        Returns:
            dict: Matching files.

        Raises:
            Exception: If listing fails.
        """
        try:
            if isinstance(filter_data, SearchParams):
                data = filter_data.model_dump(exclude_none=True)
            else:
                data = filter_data or {}
            return self.client.call("POST", f"/api/v1/vmeta/dataset/{dataset_id}/files/search", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2036: Failed to search dataset files for {dataset_id}: {e}") from e

    def add_files_to_dataset(self, dataset_id: str, file_data: Union[dict, FileAddRequest]) -> dict:
        """
        Adds files to a dataset.

        Args:
            dataset_id (str): ID of the dataset.
            file_data (dict or FileAddRequest): File metadata.

        Returns:
            dict: Confirmation of file addition.

        Raises:
            Exception: If operation fails.
        """
        try:
            if isinstance(file_data, FileAddRequest):
                data = file_data.model_dump(exclude_none=True)
            else:
                data = file_data
            return self.client.call("POST", f"/api/v1/vmeta/dataset/{dataset_id}/addFile", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2037: Failed to add files to dataset {dataset_id}: {e}") from e

    # --- Data Methods ---
    def search_data(self, canvas_id: str, collection_name: str, filter_data: Optional[Union[dict, SearchParams]] = None) -> dict:
        """
        Searches data entries in a collection.

        Args:
            canvas_id (str): Canvas ID.
            collection_name (str): Collection name.
            filter_data (dict, optional): Filter criteria.

        Returns:
            dict: Search results.

        Raises:
            Exception: If search fails.
        """
        try:
            if isinstance(filter_data, SearchParams):
                data = filter_data.model_dump(exclude_none=True)
            else:
                data = filter_data or {}
            return self.client.call("POST", f"/api/v1/vmeta/canvas/{canvas_id}/data/{collection_name}/search", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2041: Failed to search data for {collection_name}: {e}") from e


    def get_data(self, canvas_id: str, collection_name: str, data_id: str) -> dict:
        """
        Retrieves a data entry by ID.

        Args:
            canvas_id (str): Canvas ID.
            collection_name (str): Collection name.
            data_id (str): Data entry ID.

        Returns:
            dict: Data record.

        Raises:
            Exception: If retrieval fails.
        """
        try:
            return self.client.call("GET", f"/api/v1/vmeta/canvas/{canvas_id}/data/{collection_name}/{data_id}")
        except Exception as e:
            raise Exception(
                f"Error 2042: Failed to get data {data_id}: {e}") from e

    def update_data(self, canvas_id: str, collection_name: str, data_id: str, update_data: Union[dict, DataEntryUpdate]) -> dict:
        """
        Updates a data entry.

        Args:
            canvas_id (str): Canvas ID.
            collection_name (str): Collection name.
            data_id (str): Data entry ID.
            update_data (dict or DataEntryUpdate): Update payload.

        Returns:
            dict: Updated data entry.

        Raises:
            Exception: If update fails.
        """
        try:
            if isinstance(update_data, DataEntryUpdate):
                data = update_data.model_dump(exclude_none=True)
            else:
                data = update_data
            return self.client.call("PATCH", f"/api/v1/vmeta/canvas/{canvas_id}/data/{collection_name}/{data_id}", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2043: Failed to update data {data_id}: {e}") from e

    def delete_data(self, canvas_id: str, collection_name: str, data_id: str) -> dict:
        """
        Deletes a data entry.

        Args:
            canvas_id (str): Canvas ID.
            collection_name (str): Collection name.
            data_id (str): Data entry ID.

        Returns:
            dict: Deletion result.

        Raises:
            Exception: If deletion fails.
        """
        try:
            return self.client.call("DELETE", f"/api/v1/vmeta/canvas/{canvas_id}/data/{collection_name}/{data_id}")
        except Exception as e:
            raise Exception(
                f"Error 2044: Failed to delete data {data_id}: {e}") from e

    def create_data(self, canvas_id: str, collection_name: str, data_entry: Union[dict, DataEntryUpdate]) -> dict:
        """
        Creates a new data entry in a collection.

        Args:
            canvas_id (str): Canvas ID.
            collection_name (str): Collection name.
            data_entry (dict or DataEntryUpdate): Data to insert.

        Returns:
            dict: The created data entry.

        Raises:
            Exception: If creation fails.
        """
        try:
            if isinstance(data_entry, DataEntryUpdate):
                data = data_entry.model_dump(exclude_none=True)
            else:
                data = data_entry
            return self.client.call("POST", f"/api/v1/vmeta/canvas/{canvas_id}/data/{collection_name}/create", data=data)
        except Exception as e:
            raise Exception(
                f"Error 2045: Failed to create data in {collection_name}: {e}") from e



