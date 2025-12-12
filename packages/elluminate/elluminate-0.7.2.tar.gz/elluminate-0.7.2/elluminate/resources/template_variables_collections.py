from typing import Any, Dict, List, Tuple

import httpx
from loguru import logger

from elluminate.resources.base import BaseResource
from elluminate.schemas import (
    CollectionColumn,
    CreateCollectionRequest,
    PromptTemplate,
    TemplateVariablesCollection,
    TemplateVariablesCollectionFilter,
    TemplateVariablesCollectionSort,
    TemplateVariablesCollectionWithEntries,
    UpdateCollectionRequest,
)
from elluminate.utils import run_async


class TemplateVariablesCollectionsResource(BaseResource):
    async def aget(
        self,
        name: str,
    ) -> TemplateVariablesCollectionWithEntries:
        """Async version of get_collection."""
        response = await self._aget("collections", params={"name": name})
        collections = [TemplateVariablesCollection.model_validate(c) for c in response.json()["items"]]

        if not collections:
            raise ValueError(f"No collection found with name '{name}'")

        # Since collection name are unique per project, there should be only one if `collections` is nonempty.
        collection = collections[0]

        # Fetch the `collection` by `id` since this response includes the template variables
        response = await self._aget(f"collections/{collection.id}")
        collection = TemplateVariablesCollectionWithEntries.model_validate(response.json())

        return collection

    def get(
        self,
        *,
        name: str,
    ) -> TemplateVariablesCollectionWithEntries:
        """Get a collection by name.

        Args:
            name (str): The name of the collection to get.

        Returns:
            TemplateVariablesCollectionWithEntries: The collection object.

        Raises:
            ValueError: If no collection is found with the given name.

        """
        return run_async(self.aget)(name=name)

    async def aget_by_id(self, id: int) -> TemplateVariablesCollectionWithEntries:
        """Async version of get_by_id."""
        response = await self._aget(f"collections/{id}")

        return TemplateVariablesCollectionWithEntries.model_validate(response.json())

    def get_by_id(self, id: int) -> TemplateVariablesCollectionWithEntries:
        """Get a collection by id.

        Args:
            id (int): The id of the collection.

        Returns:
            (TemplateVariablesCollectionWithEntries): The requested collection.

        """
        return run_async(self.aget_by_id)(id)

    async def alist(
        self,
        filters: TemplateVariablesCollectionFilter | None = None,
        compatible_prompt_template: PromptTemplate | None = None,
        sort_options: TemplateVariablesCollectionSort | None = None,
    ) -> list[TemplateVariablesCollection]:
        """Async version of list_collections."""
        params = {}

        if filters:
            params["filters"] = filters.model_dump()
        if compatible_prompt_template:
            params["compatible_prompt_template_id"] = compatible_prompt_template.id
        if sort_options:
            params["sort_options"] = sort_options.model_dump()

        return await self._paginate("collections", model=TemplateVariablesCollection, params=params)

    def list(
        self,
        filters: TemplateVariablesCollectionFilter | None = None,
        compatible_prompt_template: PromptTemplate | None = None,
        sort_options: TemplateVariablesCollectionSort | None = None,
    ) -> list[TemplateVariablesCollection]:
        """Get a list of template variables collections.

        Args:
            filters (TemplateVariablesCollectionFilter | None): Filter for template variables collections.
            compatible_prompt_template (PromptTemplate | None): Filter collections compatible with a specific prompt template.
            sort_options (TemplateVariablesCollectionSort | None): Sort for template variables collections.

        Returns:
            list[TemplateVariablesCollection]: A list of template variables collections.

        """
        return run_async(self.alist)(
            filters=filters,
            compatible_prompt_template=compatible_prompt_template,
            sort_options=sort_options,
        )

    async def acreate(
        self,
        name: str | None = None,
        description: str = "",
        variables: List[Dict[str, Any]] | None = None,
        columns: List[CollectionColumn] | None = None,
        read_only: bool = False,
    ) -> TemplateVariablesCollectionWithEntries:
        """Async version of create_collection."""
        response = await self._apost(
            "collections",
            json=CreateCollectionRequest(
                name=name, description=description, variables=variables, columns=columns, read_only=read_only
            ).model_dump(exclude_none=True),
        )
        return TemplateVariablesCollectionWithEntries.model_validate(response.json())

    def create(
        self,
        name: str,
        description: str = "",
        variables: List[Dict[str, Any]] | None = None,
        columns: List[CollectionColumn] | None = None,
        read_only: bool = False,
    ) -> TemplateVariablesCollectionWithEntries:
        """Creates a new collection.

        Args:
            name (str): The name for the new collection.
            description (str): Optional description for the collection.
            variables (list[dict[str, Any]]): Optional list of variables to add to the collection.
                Values can be strings for TEXT columns, dicts for CONVERSATION columns, or other types.
            columns (list[CollectionColumn]): Optional list of column definitions for the collection.
            read_only (bool): Whether the collection should be read-only.

        Returns:
            (TemplateVariablesCollection): The newly created collection object.

        Raises:
            httpx.HTTPStatusError: If collection with same name already exists (400 BAD REQUEST)

        """
        return run_async(self.acreate)(
            name=name, description=description, variables=variables, columns=columns, read_only=read_only
        )

    async def aget_or_create(
        self,
        name: str,
        description: str = "",
        variables: List[Dict[str, Any]] | None = None,
        columns: List[CollectionColumn] | None = None,
        read_only: bool = False,
    ) -> Tuple[TemplateVariablesCollectionWithEntries, bool]:
        """Async version of get_or_create_collection."""
        try:
            return await self.acreate(
                name=name, description=description, variables=variables, columns=columns, read_only=read_only
            ), True
        except httpx.HTTPStatusError as e:
            # Code 409 means resource already exists, simply get and return it
            if e.response.status_code == 409:
                collection = await self.aget(name=name)
                if description != "" and collection.description != description:
                    logger.warning(
                        f"Collection with name {name} already exists with a different description (expected: {description}, actual: {collection.description}), returning existing collection."
                    )
                if variables:
                    logger.warning(
                        f"Collection with name {name} already exists. Given variables are ignored. Please use `.template_variables.add_to_collection` to add variables to the collection."
                    )
                if columns:
                    # Validate that existing collection has compatible columns
                    existing_column_types = {col.column_type for col in collection.columns}
                    requested_column_types = {col.column_type for col in columns}

                    if requested_column_types != existing_column_types:
                        raise ValueError(
                            f"Collection '{name}' already exists with different column types. "
                            f"Existing: {existing_column_types}, Requested: {requested_column_types}. "
                            f"Use a different collection name or modify the existing collection."
                        )

                    logger.warning(
                        f"Collection with name {name} already exists. Given columns are ignored. Please use `.update` to modify the collection structure."
                    )
                return collection, False
            raise  # Re-raise any other HTTP status errors s

    def get_or_create(
        self,
        name: str,
        description: str = "",
        variables: List[Dict[str, Any]] | None = None,
        columns: List[CollectionColumn] | None = None,
        read_only: bool = False,
    ) -> tuple[TemplateVariablesCollectionWithEntries, bool]:
        """Gets an existing collection by name or creates a new one if it doesn't exist.

        If a collection with the given name exists:
        - If columns parameter is provided, validates that the existing collection has matching column types
        - Returns the existing collection if compatible, otherwise raises ValueError
        - Other parameters (description, variables, read_only) are ignored with warnings

        Args:
            name: The name of the collection to get or create.
            description: Optional description for the collection if created.
            variables: Optional list of variables to add to the collection if created.
                Values can be strings for TEXT columns, dicts for CONVERSATION columns, or other types.
            columns: Optional list of column definitions for the collection if created.
                If provided and collection exists, column types must match existing collection.
            read_only: Whether the collection should be read-only if created.

        Returns:
            tuple[TemplateVariablesCollectionWithEntries, bool]: A tuple containing:
                - Collection: The retrieved or created collection object
                - bool: True if a new collection was created, False if existing was found

        Raises:
            ValueError: If collection exists but has incompatible column types

        """
        return run_async(self.aget_or_create)(
            name=name, description=description, variables=variables, columns=columns, read_only=read_only
        )

    async def adelete(self, template_variables_collection: TemplateVariablesCollection) -> None:
        await self._adelete(f"collections/{template_variables_collection.id}")

    def delete(self, template_variables_collection: TemplateVariablesCollection) -> None:
        return run_async(self.adelete)(template_variables_collection)

    async def aupdate(
        self,
        collection_id: int,
        name: str,
        description: str | None = None,
        read_only: bool | None = None,
        columns: List[CollectionColumn] | None = None,
    ) -> TemplateVariablesCollection:
        """Async version of update_collection."""
        response = await self._aput(
            f"collections/{collection_id}",
            json=UpdateCollectionRequest(
                name=name,
                description=description,
                read_only=read_only,
                columns=columns,
            ).model_dump(exclude_none=True),
        )
        return TemplateVariablesCollection.model_validate(response.json())

    def update(
        self,
        collection_id: int,
        name: str,
        description: str | None = None,
        read_only: bool | None = None,
        columns: List[CollectionColumn] | None = None,
    ) -> TemplateVariablesCollection:
        """Update an existing collection.

        Args:
            collection_id: The ID of the collection to update.
            name: The new name for the collection.
            description: Optional new description for the collection.
            read_only: Optional new read-only status for the collection.
            columns: Optional list of columns in the desired order. Missing columns are deleted,
                    new columns are created as TEXT with default='', existing columns are reordered.

        Returns:
            TemplateVariablesCollection: The updated collection object.

        Raises:
            httpx.HTTPStatusError: If collection doesn't exist or validation fails.

        """
        return run_async(self.aupdate)(
            collection_id=collection_id,
            name=name,
            description=description,
            read_only=read_only,
            columns=columns,
        )
