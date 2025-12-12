from ..types.generative import (
    OpenaiPayload, PromptOptions, AgentOptions, SessionOptions, 
    StateOptions, AbilityOptions, ImageOptions, GenerateResponse
)
from typing import Optional, Union, Dict, Any, List

class GenerativeResource:
    def __init__(self, client):
        self._client = client

    def create(
            self,
            # Required Fields for Payload Construction
            prompt: str,
            agent_id: str,
            session_id: str,
            
            # Optional/Boolean Fields
            agent_version: Optional[str] = None,
            files: Optional[List[Dict[str, Any]]] = None,
            conversation_id: Optional[str] = None,
            new_conversation: Optional[bool] = None,
            cancel_generation: bool = False,
            reasoning: bool = True,
            web_search: bool = False,
            **kwargs
            ) -> GenerateResponse:
        """
        Generate text based on a prompt.
        Accepts specific args or a raw dictionary for future-proofing.
        """
        payload = OpenaiPayload(
            promptOptions=PromptOptions(
                prompt=prompt,
                files=[ImageOptions(**f) for f in files] if files else None
            ),
            stateOptions=StateOptions(
                newConversation=new_conversation,
                cancelGeneration=cancel_generation
            ),
            sessionOptions=SessionOptions(
                sessionId=session_id,
                conversationId=conversation_id
            ),
            agentOptions=AgentOptions(
                agentId=agent_id,
                agentVersion=agent_version
            ),
            abilityOptions=AbilityOptions(
                reasoning=reasoning,
                webSearch=web_search
            )
        ).model_dump(by_alias=True, exclude_none=True)


        data = self._client.post("/v1beta/models/generate", json=payload)

        return GenerateResponse(**data)

class AsyncGenerativeResource:
    def __init__(self, client):
        self._client = client

    async def create(
            self,
            # Required Fields for Payload Construction
            prompt: str,
            agent_id: str,
            agent_version: str,
            platform_id: str,
            session_id: str,
            
            # Optional/Boolean Fields
            files: Optional[List[Dict[str, Any]]] = None,
            conversation_id: Optional[str] = None,
            new_conversation: Optional[bool] = None,
            cancel_generation: bool = False,
            reasoning: bool = True,
            web_search: bool = False,
            **kwargs
    ) -> GenerateResponse:
        payload = OpenaiPayload(
            promptOptions=PromptOptions(
                prompt=prompt,
                files=[ImageOptions(**f) for f in files] if files else None
            ),
            stateOptions=StateOptions(
                newConversation=new_conversation,
                cancelGeneration=cancel_generation
            ),
            sessionOptions=SessionOptions(
                sessionId=session_id,
                conversationId=conversation_id
            ),
            agentOptions=AgentOptions(
                agentId=agent_id,
                agentVersion=agent_version
            ),
            abilityOptions=AbilityOptions(
                reasoning=reasoning,
                webSearch=web_search
            )
        ).model_dump(by_alias=True, exclude_none=True)

        data = await self._client.post("/v1beta/models/generate", json=payload)
       
        return GenerateResponse(**data)