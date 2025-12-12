from typing import IO, Optional, Dict, Any
import requests
import aiohttp
from outerport.models.component import Component, ComponentDeleteResponse
from outerport.resources.base_resource import BaseResource, AsyncBaseResource


class ComponentsResource(BaseResource):
    """Resource for creating and retrieving visual components."""

    def create(
        self,
        file: IO[bytes],
        component_type: str,
        file_name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        timeout: int = 480,
    ) -> Component:
        """
        Upload an image and generate a component from it.
        Waits for processing to complete and returns the component.

        :param file: The image file to upload.
        :param component_type: The type of component to generate.
        :param file_name: Optional name for the file.
        :param config: Optional configuration dict (JSON-encoded in request).
        :param timeout: Timeout in seconds for processing to complete.
        :return: The generated Component.
        """
        url = f"{self.client.base_url}/api/v0/components"
        headers = self.client._form_headers()

        if not file_name:
            file_name = getattr(file, "name", None)
            if not file_name:
                file_name = "image.png"

        files = {"image": (file_name, file, "application/octet-stream")}
        params = {"component_type": component_type}

        data = {}
        if config is not None:
            import json

            data["config"] = json.dumps(config)

        resp = requests.post(
            url, headers=headers, files=files, params=params, data=data
        )
        resp.raise_for_status()

        response_data = resp.json()
        job_status_id = response_data.get("job_status_id")
        component_id = response_data.get("component_id")

        if not job_status_id or not component_id:
            raise ValueError("Response missing job_status_id or component_id.")

        # Wait for job to complete
        self.client.job_statuses.wait_for_completion(job_status_id, timeout=timeout)

        # Retrieve the completed component
        return self.retrieve(str(component_id))

    def retrieve(self, component_id: str) -> Component:
        """
        Retrieve a component by ID.

        :param component_id: The ID of the component to retrieve.
        :return: The Component.
        """
        url = f"{self.client.base_url}/api/v0/components/{component_id}"
        headers = self.client._json_headers()

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()

        data = resp.json()
        return Component(**data)

    def delete(self, component_id: str) -> ComponentDeleteResponse:
        """
        Delete a component by ID.

        :param component_id: The ID of the component to delete.
        :return: Response with message and component_id.
        """
        url = f"{self.client.base_url}/api/v0/components/{component_id}"
        headers = self.client._json_headers()

        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        return ComponentDeleteResponse(**resp.json())


class AsyncComponentsResource(AsyncBaseResource):
    """Async resource for creating and retrieving visual components."""

    async def create(
        self,
        file: IO[bytes],
        component_type: str,
        file_name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        timeout: int = 480,
    ) -> Component:
        """
        Upload an image and generate a component from it.
        Waits for processing to complete and returns the component.

        :param file: The image file to upload.
        :param component_type: The type of component to generate.
        :param file_name: Optional name for the file.
        :param config: Optional configuration dict (JSON-encoded in request).
        :param timeout: Timeout in seconds for processing to complete.
        :return: The generated Component.
        """
        url = f"{self.client.base_url}/api/v0/components"
        headers = self.client._form_headers()

        if not file_name:
            file_name = getattr(file, "name", None)
            if not file_name:
                file_name = "image.png"

        params = {"component_type": component_type}

        async with aiohttp.ClientSession() as session:
            mpwriter = aiohttp.MultipartWriter("form-data")

            file_part = mpwriter.append(file)
            file_part.set_content_disposition(
                "form-data", name="image", filename=file_name, quote_fields=False
            )

            if config is not None:
                import json

                config_part = mpwriter.append(json.dumps(config))
                config_part.set_content_disposition("form-data", name="config")

            async with session.post(
                url, headers=headers, data=mpwriter, params=params
            ) as resp:
                resp.raise_for_status()
                response_data = await resp.json()

                job_status_id = response_data.get("job_status_id")
                component_id = response_data.get("component_id")

                if not job_status_id or not component_id:
                    raise ValueError("Response missing job_status_id or component_id.")

                # Wait for job to complete
                await self.client.job_statuses.wait_for_completion(
                    job_status_id, timeout=timeout
                )

                # Retrieve the completed component
                return await self.retrieve(str(component_id))

    async def retrieve(self, component_id: str) -> Component:
        """
        Retrieve a component by ID.

        :param component_id: The ID of the component to retrieve.
        :return: The Component.
        """
        url = f"{self.client.base_url}/api/v0/components/{component_id}"
        headers = self.client._json_headers()

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return Component(**data)

    async def delete(self, component_id: str) -> ComponentDeleteResponse:
        """
        Delete a component by ID.

        :param component_id: The ID of the component to delete.
        :return: Response with message and component_id.
        """
        url = f"{self.client.base_url}/api/v0/components/{component_id}"
        headers = self.client._json_headers()

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return ComponentDeleteResponse(**data)
