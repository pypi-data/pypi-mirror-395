from typing import Optional

from seekrai.abstract import api_requestor
from seekrai.resources.resource_base import ResourceBase
from seekrai.types import (
    SeekrFlowRequest,
)
from seekrai.types.explainability import (
    InfluentialFinetuningDataRequest,
    InfluentialFinetuningDataResponse,
)


class Explainability(ResourceBase):
    def get_influential_finetuning_data(
        self,
        model_id: str,
        question: str,
        system_prompt: Optional[str] = None,
        answer: Optional[str] = None,
    ) -> InfluentialFinetuningDataResponse:
        """
        Retrieve influential QA pair fine tuning data for a specific model.
        Args:
            - model_id (str): ID of the model to explain.
            - question (str): question from user,
            - system_prompt (str | None): System prompt for the user's question.
            - answer (str | None): answer of the finetuned model to the question; if None, the answer is retrieved from the finetuned model specified by model_id,
        Returns:
            InfluentialFinetuningDataResponse: Object containing the influential fine tuning data.
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        # Create query parameters dictionary
        parameter_payload = InfluentialFinetuningDataRequest(
            question=question, system_prompt=system_prompt, answer=answer
        ).model_dump()

        # if limit is not None:
        #     params["limit"] = limit
        # TODO  limits =? timeout: float | None = None,  max_retries: int | None = None,

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/explain/models/{model_id}/influential-finetuning-data",
                params=parameter_payload,
            ),
            stream=False,
        )
        return InfluentialFinetuningDataResponse(**response.data)


class AsyncExplainability(ResourceBase):
    async def get_influential_finetuning_data(
        self,
        model_id: str,
        question: str,
        system_prompt: Optional[str] = None,
        answer: Optional[str] = None,
    ) -> InfluentialFinetuningDataResponse:
        """
        Retrieve influential QA pair finetuning data for a specific model asynchronously.
        Args:
            - model_id (str): ID of the model to explain.
            - question (str): question from user,
            - system_prompt (str | None): System prompt for the user's question.
            - answer (str | None): answer of the finetuned model to the question; if None, the answer is retrieved from the finetuned model specified by model_id,
        Returns:
            InfluentialFinetuningDataResponse: Object containing the influential finetuning data.
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        # Create query parameters dictionary
        parameter_payload = InfluentialFinetuningDataRequest(
            model_id=model_id,
            question=question,
            system_prompt=system_prompt,
            answer=answer,
        ).model_dump()

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/explain/models/{model_id}/influential-finetuning-data",
                params=parameter_payload,
            ),
            stream=False,
        )
        return InfluentialFinetuningDataResponse(**response.data)
