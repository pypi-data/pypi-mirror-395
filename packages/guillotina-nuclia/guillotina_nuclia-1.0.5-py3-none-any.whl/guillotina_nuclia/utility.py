from guillotina.async_util import IAsyncUtility
from guillotina.event import notify
from guillotina.events import ObjectModifiedEvent
from guillotina.utils import get_authenticated_user_id
from guillotina_nuclia.interfaces.chat import IChat
from nuclia import sdk
from nuclia.lib.nua_responses import ChatModel
from nuclia_models.common.consumption import Consumption
from nuclia_models.predict.generative_responses import CitationsGenerativeResponse
from nuclia_models.predict.generative_responses import ConsumptionGenerative
from nuclia_models.predict.generative_responses import FootnoteCitationsGenerativeResponse
from nuclia_models.predict.generative_responses import GenerativeChunk
from nuclia_models.predict.generative_responses import GenerativeFullResponse
from nuclia_models.predict.generative_responses import JSONGenerativeResponse
from nuclia_models.predict.generative_responses import MetaGenerativeResponse
from nuclia_models.predict.generative_responses import ReasoningGenerativeResponse
from nuclia_models.predict.generative_responses import StatusGenerativeResponse
from nuclia_models.predict.generative_responses import TextGenerativeResponse
from nuclia_models.predict.generative_responses import ToolsGenerativeResponse
from typing import AsyncIterator
from typing import List
from typing import Optional

import logging


logger = logging.getLogger("nuclia_utility")


class INucliaUtility(IAsyncUtility):
    pass


class NucliaUtility:
    def __init__(self, settings=None, loop=None):
        self._settings = settings
        self.loop = loop
        self._nuclia_auth = sdk.AsyncNucliaAuth()
        self._predict = sdk.AsyncNucliaPredict()
        self._upload = sdk.AsyncNucliaUpload()
        self._search = sdk.AsyncNucliaSearch()
        kbid = self._settings["kbid"] or ""
        api_endpoint = self._settings["api_endpoint"]
        self._base_url_kb = f"{api_endpoint}/{kbid}"

    async def initialize(self, app):
        try:
            await self.auth()
        except Exception:
            logger.error("Error auth", exc_info=True)

    async def auth(self):
        client_id = await self._nuclia_auth.nua(token=self._settings["nua_key"])
        kbid = await self._nuclia_auth.kb(self._base_url_kb, self._settings["apikey"])
        self._nuclia_auth._config.set_default_kb(kbid)
        self._nuclia_auth._config.set_default_nua(client_id)

    async def upload(self, file_path: str):
        await self._upload.file(path=file_path)

    async def predict_chat(self, question: str, chat: IChat):
        try:
            user = get_authenticated_user_id()
        except Exception:
            user = "UNKNOWN"
        generative_model = self._settings.get("generative_model", "chatgpt4o")
        max_tokens = self._settings.get("max_tokens", 4096)

        chat_model = ChatModel(
            question=question,
            query_context=chat.context or [],
            chat_history=chat.history or [],
            user_id=user,
            generative_model=generative_model,
            max_tokens=max_tokens,
        )
        response = await self._predict.generate(text=chat_model)
        user_message = {"author": "USER", "text": question}
        nuclia_message = {"author": "NUCLIA", "text": response.answer}
        chat.history.append(user_message)
        chat.history.append(nuclia_message)
        chat.responses.append(response.answer)
        chat.register()
        await notify(ObjectModifiedEvent(chat, payload={"history": chat.history, "responses": chat.responses}))
        return response

    async def predict_chat_history(
        self,
        question: str,
        history: Optional[list] = None,
        context: Optional[list] = None,
    ):
        try:
            user = get_authenticated_user_id()
        except Exception:
            user = "UNKNOWN"
        generative_model = self._settings.get("generative_model", "chatgpt4o")
        max_tokens = self._settings.get("max_tokens", 4096)

        chat_model = ChatModel(
            question=question,
            query_context=context or [],
            chat_history=history or [],
            user_id=user,
            generative_model=generative_model,
            max_tokens=max_tokens,
        )
        return await self._predict.generate(text=chat_model)

    async def predict_chat_history_stream(
        self,
        question: str,
        history: Optional[List[dict]] = None,
        context: Optional[List[str]] = None,
    ) -> AsyncIterator[object]:
        try:
            user = get_authenticated_user_id()
        except Exception:
            user = "UNKNOWN"
        generative_model = self._settings.get("generative_model", "chatgpt4o")
        max_tokens = self._settings.get("max_tokens", 4096)

        chat_model = ChatModel(
            question=question,
            query_context=context or [],
            chat_history=history or [],
            user_id=user,
            generative_model=generative_model,
            max_tokens=max_tokens,
        )
        stream_result = GenerativeFullResponse(answer="")

        async def _stream():
            async for chunk in self._predict.generate_stream(text=chat_model):
                chunk_text = self._extract_stream_text(chunk)
                if chunk_text:
                    yield chunk_text
                else:
                    self._accumulate_stream_chunk(chunk, stream_result)
            response_payload = stream_result.model_dump()
            yield {
                "type": "end",
                "response": response_payload,
            }

        return _stream()

    async def ask(self, question: str):
        response = await self._search.ask(query=question)
        return response.answer.decode("utf-8")

    async def ask_json(self, question: str, schema: dict):
        response = await self._search.ask_json(query=question, schema=schema)
        return response.answer.decode("utf-8")

    async def search(self, question: str, filters: list = []):
        response = await self._search.search(query=question, filters=filters)
        return response.fulltext.results

    async def find(self, question: str, filters: list = []):
        response = await self._search.find(query=question, filters=filters)
        return response.resources

    async def ask_stream(self, question: str):
        async for line in self._search.ask_stream(query=question):
            if line.item.type == "answer":
                yield line.item.text.encode()
            elif line.item.type == "retrieval":
                yield line.item.results.json().encode()

    async def catalog(self, query):
        return await self._search.catalog(query=query)

    @staticmethod
    def _extract_stream_text(chunk: GenerativeChunk) -> Optional[str]:
        if isinstance(chunk.chunk, TextGenerativeResponse):
            return chunk.chunk.text
        return None

    @staticmethod
    def _accumulate_stream_chunk(chunk: GenerativeChunk, stream_result: GenerativeFullResponse) -> None:
        if isinstance(chunk.chunk, ReasoningGenerativeResponse):
            stream_result.reasoning = (stream_result.reasoning or "") + chunk.chunk.text
        elif isinstance(chunk.chunk, JSONGenerativeResponse):
            stream_result.object = chunk.chunk.object
        elif isinstance(chunk.chunk, MetaGenerativeResponse):
            stream_result.input_tokens = chunk.chunk.input_tokens
            stream_result.output_tokens = chunk.chunk.output_tokens
            stream_result.input_nuclia_tokens = chunk.chunk.input_nuclia_tokens
            stream_result.output_nuclia_tokens = chunk.chunk.output_nuclia_tokens
            stream_result.timings = chunk.chunk.timings
        elif isinstance(chunk.chunk, CitationsGenerativeResponse):
            stream_result.citations = chunk.chunk.citations
        elif isinstance(chunk.chunk, FootnoteCitationsGenerativeResponse):
            stream_result.citation_footnote_to_context = chunk.chunk.footnote_to_context
        elif isinstance(chunk.chunk, StatusGenerativeResponse):
            stream_result.code = chunk.chunk.code
            stream_result.details = chunk.chunk.details
        elif isinstance(chunk.chunk, ToolsGenerativeResponse):
            stream_result.tools = chunk.chunk.tools
        elif isinstance(chunk.chunk, ConsumptionGenerative):
            stream_result.consumption = Consumption(
                normalized_tokens=chunk.chunk.normalized_tokens,
                customer_key_tokens=chunk.chunk.customer_key_tokens,
            )
