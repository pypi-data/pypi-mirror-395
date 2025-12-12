from typing import Any, Dict, List

from seekrai.abstract import api_requestor
from seekrai.resources.resource_base import ResourceBase
from seekrai.seekrflow_response import SeekrFlowResponse
from seekrai.types import (
    AlignmentEstimationRequest,
    AlignmentEstimationResponse,
    AlignmentList,
    AlignmentOutput,
    AlignmentRequest,
    AlignmentResponse,
    AlignmentType,
    SeekrFlowRequest,
    SystemPrompt,
    SystemPromptCreateRequest,
    SystemPromptUpdateRequest,
)
from seekrai.types.abstract import SeekrFlowClient


class Alignment(ResourceBase):
    def __init__(self, client: SeekrFlowClient) -> None:
        super().__init__(client)
        self.system_prompt = SystemPromptResource(client)

    def generate(
        self,
        instructions: str,
        files: List[str],
        type: AlignmentType = AlignmentType.PRINCIPLE,
    ) -> AlignmentResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = AlignmentRequest(
            instructions=instructions, files=files, type=type
        ).model_dump()

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="POST",
                url="flow/alignment/generate",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return AlignmentResponse(**response.data)

    def list(self) -> AlignmentList:
        """
        Lists alignment job history

        Returns:
            AlignmentList: Object containing a list of alignment jobs
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url="flow/alignment",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return AlignmentList(**response.data)

    def retrieve(self, id: str) -> AlignmentResponse:
        """
        Retrieves alignment job details

        Args:
            id (str): Alignment job ID to retrieve.

        Returns:
            AlignmentResponse: Object containing information about alignment job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/alignment/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return AlignmentResponse(**response.data)

    def outputs(self, id: str) -> List[AlignmentOutput]:
        """
        Retrieves output files for an alignment job.

        Args:
            id (str): Alignment job ID whose outputs to fetch.

        Returns:
            list[AlignmentOutput]: Collection of alignment output metadata.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/alignment/{id}/outputs",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return [AlignmentOutput(**output) for output in response.data]  # type: ignore[arg-type]

    def delete(self, id: str) -> None:
        """
        Deletes an alignment job.

        Args:
            id (str): Alignment job ID to delete.

        Returns:
            None
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="DELETE",
                url=f"flow/alignment/{id}",
            ),
            stream=False,
        )

        # Endpoint returns 204 No Content
        return None

    def cancel(self, id: str) -> AlignmentResponse:
        """
        Method to cancel a running alignment job

        Args:
            id (str): Alignment job ID to cancel. A string that starts with `al-`.

        Returns:
            AlignmentResponse: Object containing information about cancelled alignment job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="POST",
                url=f"flow/alignment/{id}/cancel",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return AlignmentResponse(**response.data)

    def estimate(self, files: List[str]) -> AlignmentEstimationResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = AlignmentEstimationRequest(
            files=files,
        ).model_dump()

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="POST",
                url="flow/alignment/estimate",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return AlignmentEstimationResponse(**response.data)


class AsyncAlignment(ResourceBase):
    def __init__(self, client: SeekrFlowClient) -> None:
        super().__init__(client)
        self.system_prompt = AsyncSystemPromptResource(client)

    async def generate(
        self,
        instructions: str,
        files: List[str],
        type: AlignmentType = AlignmentType.PRINCIPLE,
    ) -> AlignmentResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = AlignmentRequest(
            instructions=instructions, files=files, type=type
        ).model_dump()

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="POST",
                url="flow/alignment/generate",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return AlignmentResponse(**response.data)

    async def list(self) -> AlignmentList:
        """
        Lists alignment job history

        Returns:
            AlignmentList: Object containing a list of alignment jobs
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url="flow/alignment",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return AlignmentList(**response.data)

    async def retrieve(self, id: str) -> AlignmentResponse:
        """
        Retrieves alignment job details

        Args:
            id (str): Alignment job ID to retrieve.

        Returns:
            AlignmentResponse: Object containing information about alignment job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/alignment/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return AlignmentResponse(**response.data)

    async def outputs(self, id: str) -> List[AlignmentOutput]:
        """
        Retrieves output files for an alignment job asynchronously.

        Args:
            id (str): Alignment job ID whose outputs to fetch.

        Returns:
            list[AlignmentOutput]: Collection of alignment output metadata.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/alignment/{id}/outputs",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return [AlignmentOutput(**output) for output in response.data]  # type: ignore[arg-type]

    async def delete(self, id: str) -> None:
        """
        Deletes an alignment job asynchronously.

        Args:
            id (str): Alignment job ID to delete.

        Returns:
            None
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="DELETE",
                url=f"flow/alignment/{id}",
            ),
            stream=False,
        )

        # Endpoint returns 204 No Content
        return None

    async def cancel(self, id: str) -> AlignmentResponse:
        """
        Async method to cancel a running alignment job

        Args:
            id (str): Alignment job ID to cancel. A string that starts with `al-`.

        Returns:
            AlignmentResponse: Object containing information about cancelled alignment job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="POST",
                url=f"flow/alignment/{id}/cancel",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return AlignmentResponse(**response.data)

    async def estimate(self, files: List[str]) -> AlignmentEstimationResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = AlignmentEstimationRequest(
            files=files,
        ).model_dump()

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="POST",
                url="flow/alignment/estimate",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return AlignmentEstimationResponse(**response.data)


class SystemPromptResource(ResourceBase):
    def create(self, source_id: str, instructions: str) -> SystemPrompt:
        """
        Creates a new AI-generated system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to create the system prompt for
            instructions (str): Instructions for generating the system prompt

        Returns:
            SystemPrompt: The created system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = SystemPromptCreateRequest(
            instructions=instructions
        ).model_dump()

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="POST",
                url=f"flow/alignment/system_prompt/{source_id}",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    def get(self, source_id: str) -> SystemPrompt:
        """
        Retrieves the system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to retrieve the system prompt for

        Returns:
            SystemPrompt: The retrieved system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/alignment/system_prompt/{source_id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    def regenerate(self, source_id: str, instructions: str) -> SystemPrompt:
        """
        Regenerates the AI-generated system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to regenerate the system prompt for
            instructions (str): Instructions for regenerating the system prompt

        Returns:
            SystemPrompt: The regenerated system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = SystemPromptCreateRequest(
            instructions=instructions
        ).model_dump()

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="POST",
                url=f"flow/alignment/system_prompt/{source_id}/regenerate",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    def update(self, source_id: str, content: str) -> SystemPrompt:
        """
        Updates the system prompt for the given source_id with custom content.

        Args:
            source_id (str): The ID of the source to update the system prompt for
            content (str): The custom content for the system prompt

        Returns:
            SystemPrompt: The updated system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = SystemPromptUpdateRequest(content=content).model_dump()

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="PUT",
                url=f"flow/alignment/system_prompt/{source_id}",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    def delete(self, source_id: str) -> Dict[str, Any]:
        """
        Deletes the system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to delete the system prompt for

        Returns:
            dict: A dictionary with the deletion result
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="DELETE",
                url=f"flow/alignment/system_prompt/{source_id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return response.data


class AsyncSystemPromptResource(ResourceBase):
    async def create(self, source_id: str, instructions: str) -> SystemPrompt:
        """
        Asynchronously creates a new AI-generated system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to create the system prompt for
            instructions (str): Instructions for generating the system prompt

        Returns:
            SystemPrompt: The created system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = SystemPromptCreateRequest(
            instructions=instructions
        ).model_dump()

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="POST",
                url=f"flow/alignment/system_prompt/{source_id}",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    async def get(self, source_id: str) -> SystemPrompt:
        """
        Asynchronously retrieves the system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to retrieve the system prompt for

        Returns:
            SystemPrompt: The retrieved system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/alignment/system_prompt/{source_id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    async def regenerate(self, source_id: str, instructions: str) -> SystemPrompt:
        """
        Asynchronously regenerates the AI-generated system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to regenerate the system prompt for
            instructions (str): Instructions for regenerating the system prompt

        Returns:
            SystemPrompt: The regenerated system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = SystemPromptCreateRequest(
            instructions=instructions
        ).model_dump()

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="POST",
                url=f"flow/alignment/system_prompt/{source_id}/regenerate",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    async def update(self, source_id: str, content: str) -> SystemPrompt:
        """
        Asynchronously updates the system prompt for the given source_id with custom content.

        Args:
            source_id (str): The ID of the source to update the system prompt for
            content (str): The custom content for the system prompt

        Returns:
            SystemPrompt: The updated system prompt
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = SystemPromptUpdateRequest(content=content).model_dump()

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="PUT",
                url=f"flow/alignment/system_prompt/{source_id}",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return SystemPrompt(**response.data)

    async def delete(self, source_id: str) -> Dict[str, Any]:
        """
        Asynchronously deletes the system prompt for the given source_id.

        Args:
            source_id (str): The ID of the source to delete the system prompt for

        Returns:
            dict: A dictionary with the deletion result
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="DELETE",
                url=f"flow/alignment/system_prompt/{source_id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        return response.data
