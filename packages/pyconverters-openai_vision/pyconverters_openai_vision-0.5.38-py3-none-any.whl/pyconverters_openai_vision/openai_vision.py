import base64
import os
import re
from enum import Enum
from logging import Logger
from re import Pattern
from typing import List, cast, Type, Dict, Any, Optional

import filetype as filetype
from log_with_context import add_logging_context
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText
from starlette.datastructures import UploadFile

from .openai_utils import create_openai_model_enum, openai_chat_completion, gpt_filter, \
    NO_DEPLOYED_MODELS, OAuthToken, all_filter, check_litellm_defined

logger = Logger("pymultirole")
SHOW_INTERNAL = bool(os.getenv("SHOW_INTERNAL", "false"))


class OpenAIVisionBaseParameters(ConverterParameters):
    base_url: str = Field(
        None,
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model_str: str = Field(
        None, extra="advanced"
    )
    model: str = Field(
        None, extra="internal"
    )
    prompt: str = Field(
        """If the attached file is an image: describe the image.""",
        description="""Contains the prompt as a string""",
        extra="multiline",
    )
    max_tokens: int = Field(
        16384,
        description="""The maximum number of tokens to generate in the completion.
    The token count of your prompt plus max_tokens cannot exceed the model's context length.
    Most models have a context length of 2048 tokens (except for the newest models, which support 4096).""",
    )
    system_prompt: str = Field(
        None,
        description="""Contains the system prompt""",
        extra="multiline,advanced",
    )
    temperature: float = Field(
        0.1,
        description="""What sampling temperature to use, between 0 and 2.
    Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    We generally recommend altering this or `top_p` but not both.""",
        extra="advanced",
    )
    top_p: int = Field(
        1,
        description="""An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
    So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    We generally recommend altering this or `temperature` but not both.""",
        extra="advanced",
    )
    n: int = Field(
        1,
        description="""How many completions to generate for each prompt.
    Note: Because this parameter generates many completions, it can quickly consume your token quota.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    best_of: int = Field(
        1,
        description="""Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token).
    Results cannot be streamed.
    When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    presence_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.""",
        extra="advanced",
    )
    frequency_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.""",
        extra="advanced",
    )


class OpenAIVisionModel(str, Enum):
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"
    gpt_4_1 = "gpt-4.1"
    gpt_4_1_mini = "gpt-4.1-mini"
    gpt_4_1_nano = "gpt-4.1-nano"
    gpt_5 = "gpt-5"
    gpt_5_mini = "gpt-5-mini"
    gpt_5_nano = "gpt-5-nano"


check_litellm_defined()
OPENAI_PREFIX = ""
OPENAI_API_BASE = os.getenv(OPENAI_PREFIX + "OPENAI_API_BASE", None)
CHAT_GPT_MODEL_ENUM, DEFAULT_CHAT_GPT_MODEL = create_openai_model_enum('OpenAIModel2', prefix=OPENAI_PREFIX,
                                                                       base_url=OPENAI_API_BASE,
                                                                       key=gpt_filter if OPENAI_API_BASE is None else all_filter)


class OpenAIVisionParameters(OpenAIVisionBaseParameters):
    base_url: Optional[str] = Field(
        os.getenv(OPENAI_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: CHAT_GPT_MODEL_ENUM = Field(
        DEFAULT_CHAT_GPT_MODEL,
        description="""The [OpenAI model](https://platform.openai.com/docs/models) used for completion.""",
        extra="pipeline-naming-hint"
    )


DEEPINFRA_PREFIX = "DEEPINFRA_"
DEEPINFRA_OPENAI_API_BASE = os.getenv(DEEPINFRA_PREFIX + "OPENAI_API_BASE", None)
DEEPINFRA_CHAT_GPT_MODEL_ENUM, DEEPINFRA_DEFAULT_CHAT_GPT_MODEL = create_openai_model_enum('DeepInfraOpenAIModel',
                                                                                           prefix=DEEPINFRA_PREFIX,
                                                                                           base_url=DEEPINFRA_OPENAI_API_BASE)


class DeepInfraOpenAIVisionParameters(OpenAIVisionBaseParameters):
    base_url: str = Field(
        os.getenv(DEEPINFRA_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: DEEPINFRA_CHAT_GPT_MODEL_ENUM = Field(
        None,
        description="""The [DeepInfra 'OpenAI compatible' model](https://deepinfra.com/models?type=text-generation) used for completion. It must be deployed on your [DeepInfra dashboard](https://deepinfra.com/dash).""",
        extra="pipeline-naming-hint"
    )


class OpenAIVisionConverterBase(ConverterBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it."""
    PREFIX: str = ""
    oauth_token: OAuthToken = OAuthToken()

    def compute_args(self, params: OpenAIVisionBaseParameters, source: UploadFile, kind
                     ) -> Dict[str, Any]:
        data = source.file.read()
        rv = base64.b64encode(data)
        if kind.mime.startswith("image"):
            binary_block = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{kind.mime};base64,{rv.decode('utf-8')}"
                }
            }
        messages = [{"role": "system", "content": params.system_prompt}] if params.system_prompt is not None else []
        messages.append({"role": "user",
                         "content": [
                             {
                                 "type": "text",
                                 "text": params.prompt
                             },
                             binary_block
                         ]})
        kwargs = {
            'model': params.model_str,
            'messages': messages,
            'max_tokens': params.max_tokens,
            'temperature': params.temperature,
            'top_p': params.top_p,
            'n': params.n,
            'frequency_penalty': params.frequency_penalty,
            'presence_penalty': params.presence_penalty,
        }
        return kwargs

    def compute_result(self, base_url, **kwargs):
        pattern: Pattern = re.compile(r"```(?:markdown\s+)?(\W.*?)```", re.DOTALL)
        """Regex pattern to parse the output."""
        response = openai_chat_completion(self.PREFIX, self.oauth_token, base_url, **kwargs)
        contents = []
        result = None
        for choice in response.choices:
            if choice.message.content:
                if "```" in choice.message.content:
                    action_match = pattern.search(choice.message.content)
                    if action_match is not None:
                        contents.append(action_match.group(1).strip())
                else:
                    contents.append(choice.message.content)
        if contents:
            result = "\n".join(contents)
        return result

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:

        params: OpenAIVisionBaseParameters = cast(
            OpenAIVisionBaseParameters, parameters
        )
        OPENAI_MODEL = os.getenv(self.PREFIX + "OPENAI_MODEL", None)
        if OPENAI_MODEL:
            params.model_str = OPENAI_MODEL
        doc = None
        try:
            kind = filetype.guess(source.file)
            source.file.seek(0)
            if kind.mime.startswith("image"):
                result = None
                kwargs = self.compute_args(params, source, kind)
                if kwargs['model'] != NO_DEPLOYED_MODELS:
                    result = self.compute_result(params.base_url, **kwargs)
                if result:
                    doc = Document(identifier=source.filename, text=result)
                    doc.properties = {"fileName": source.filename}
        except BaseException as err:
            raise err
        if doc is None:
            raise TypeError(f"Conversion of file {source.filename} failed")
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIVisionBaseParameters


class OpenAIVisionConverter(OpenAIVisionConverterBase):
    __doc__ = """Convert audio using [OpenAI Audio](https://platform.openai.com/docs/guides/speech-to-text) API"""

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: OpenAIVisionParameters = cast(
            OpenAIVisionParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().convert(source, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIVisionParameters


class DeepInfraOpenAIVisionConverter(OpenAIVisionConverterBase):
    __doc__ = """Convert images using [DeepInfra Vision](https://deepinfra.com/docs/tutorials/whisper) API"""
    PREFIX = DEEPINFRA_PREFIX

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: DeepInfraOpenAIVisionParameters = cast(
            DeepInfraOpenAIVisionParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().convert(source, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepInfraOpenAIVisionParameters


def guess_kind(base64_src):
    kind = None
    img_regex = r"data:(image/[^;]+);base64"
    matches = re.search(img_regex, base64_src)
    if matches:
        mime = matches.group(1)
        kind = filetype.get_type(mime)
    return kind


class OpenAIVisionProcessorBaseParameters(ProcessorParameters):
    base_url: str = Field(
        None,
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model_str: str = Field(
        None, extra="advanced"
    )
    model: str = Field(
        None, extra="internal"
    )
    max_tokens: int = Field(
        16384,
        description="""The maximum number of tokens to generate in the completion.
        The token count of your prompt plus max_tokens cannot exceed the model's context length.
        Most models have a context length of 2048 tokens (except for the newest models, which support 4096).""",
    )
    replace_refs_altTexts_by_descriptions: bool = Field(
        True,
        description="""Replace references to images in text by their textual description.""",
        extra="advanced"
    )
    system_prompt: str = Field(
        None,
        description="""Contains the system prompt""",
        extra="multiline,advanced",
    )
    prompt: str = Field(
        "Generate a textual description of the image",
        description="""Contains the prompt""",
        extra="multiline",
    )
    temperature: float = Field(
        0.1,
        description="""What sampling temperature to use, between 0 and 2.
        Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
        We generally recommend altering this or `top_p` but not both.""",
        extra="advanced",
    )
    top_p: int = Field(
        1,
        description="""An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
        So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        We generally recommend altering this or `temperature` but not both.""",
        extra="advanced",
    )
    n: int = Field(
        1,
        description="""How many completions to generate for each prompt.
        Note: Because this parameter generates many completions, it can quickly consume your token quota.
        Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    best_of: int = Field(
        1,
        description="""Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token).
        Results cannot be streamed.
        When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.
        Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    presence_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
        Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.""",
        extra="advanced",
    )
    frequency_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
        Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.""",
        extra="advanced",
    )


class OpenAIVisionProcessorBase(ProcessorBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it."""
    PREFIX: str = ""
    oauth_token: OAuthToken = OAuthToken()

    def compute_args(self, params: OpenAIVisionProcessorBaseParameters, source: str, kind
                     ) -> Dict[str, Any]:
        if kind.mime.startswith("image"):
            binary_block = {
                "type": "image_url",
                "image_url": {
                    "url": source
                }
            }
        messages = [{"role": "system", "content": params.system_prompt}] if params.system_prompt is not None else []
        messages.append({"role": "user",
                         "content": [
                             {
                                 "type": "text",
                                 "text": params.prompt
                             },
                             binary_block
                         ]})
        kwargs = {
            'model': params.model_str,
            'messages': messages,
            'max_tokens': params.max_tokens,
            'temperature': params.temperature,
            'top_p': params.top_p,
            'n': params.n,
            'frequency_penalty': params.frequency_penalty,
            'presence_penalty': params.presence_penalty,
        }
        return kwargs

    def compute_result(self, base_url, **kwargs):
        pattern: Pattern = re.compile(r"```(?:markdown\s+)?(\W.*?)```", re.DOTALL)
        """Regex pattern to parse the output."""
        response = openai_chat_completion(self.PREFIX, self.oauth_token, base_url, **kwargs)
        contents = []
        result = None
        for choice in response.choices:
            if choice.message.content:
                if "```" in choice.message.content:
                    action_match = pattern.search(choice.message.content)
                    if action_match is not None:
                        contents.append(action_match.group(1).strip())
                else:
                    contents.append(choice.message.content)
        if contents:
            result = "\n".join(contents)
        return result

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        # supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)

        params: OpenAIVisionProcessorBaseParameters = cast(
            OpenAIVisionProcessorBaseParameters, parameters
        )
        OPENAI_MODEL = os.getenv(self.PREFIX + "OPENAI_MODEL", None)
        if OPENAI_MODEL:
            params.model_str = OPENAI_MODEL
        try:
            for document in documents:
                with add_logging_context(docid=document.identifier):
                    if document.altTexts:
                        altTexts = document.altTexts
                        alts = {altText.name: altText.text for altText in altTexts}
                        anames = list(alts.keys())
                        for aname in anames:
                            atext = alts[aname]
                            result = None
                            kind = guess_kind(atext)
                            if kind is not None and kind.mime.startswith("image"):
                                kwargs = self.compute_args(params, atext, kind)
                                if kwargs['model'] != NO_DEPLOYED_MODELS:
                                    result = self.compute_result(params.base_url, **kwargs)
                            if result is not None and isinstance(result, str):
                                alts[aname] = result
                            else:
                                del alts[aname]
                        if alts:
                            document.altTexts = []

                            if params.replace_refs_altTexts_by_descriptions:
                                text = document.text
                                link_regex = r"!\[([^]]+)\]\(([^]]+)\)"

                                def convert_links(matchobj):
                                    m = matchobj.group(0)
                                    m_id = matchobj.group(1)
                                    if m_id in alts:
                                        # markdown blockquote
                                        m_desc = "\n".join(["> " + li for li in alts[m_id].splitlines()])
                                        return f"{m}\n{m_desc}\n"
                                    return m

                                ptext = re.sub(link_regex, convert_links, text, 0,
                                               re.MULTILINE)
                                document.text = ptext
                                for altText in altTexts:
                                    if altText.name not in alts:
                                        document.altTexts.append(altText)
                            else:
                                for altText in altTexts:
                                    if altText.name in alts:
                                        document.altTexts.append(AltText(name=altText.name, text=alts[altText.name]))
                                    else:
                                        document.altTexts.append(altText)

        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIVisionProcessorBaseParameters


class OpenAIVisionProcessorParameters(OpenAIVisionProcessorBaseParameters):
    base_url: Optional[str] = Field(
        os.getenv(OPENAI_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: CHAT_GPT_MODEL_ENUM = Field(
        DEFAULT_CHAT_GPT_MODEL,
        description="""The [OpenAI model](https://platform.openai.com/docs/models) used for completion.""",
        extra="pipeline-naming-hint"
    )


class OpenAIVisionProcessor(OpenAIVisionProcessorBase):
    __doc__ = """Convert audio using [OpenAI Audio](https://platform.openai.com/docs/guides/speech-to-text) API"""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: OpenAIVisionProcessorParameters = cast(
            OpenAIVisionProcessorParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().process(documents, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIVisionProcessorParameters


class DeepInfraOpenAIVisionProcessorParameters(OpenAIVisionProcessorBaseParameters):
    base_url: str = Field(
        os.getenv(DEEPINFRA_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: DEEPINFRA_CHAT_GPT_MODEL_ENUM = Field(
        None,
        description="""The [DeepInfra 'OpenAI compatible' model](https://deepinfra.com/models?type=text-generation) used for completion. It must be deployed on your [DeepInfra dashboard](https://deepinfra.com/dash).""",
        extra="pipeline-naming-hint"
    )


class DeepInfraOpenAIVisionProcessor(OpenAIVisionProcessorBase):
    __doc__ = """Convert images using [DeepInfra Vision](https://deepinfra.com/docs/tutorials/whisper) API"""
    PREFIX = DEEPINFRA_PREFIX

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: DeepInfraOpenAIVisionProcessorParameters = cast(
            DeepInfraOpenAIVisionProcessorParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().process(documents, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepInfraOpenAIVisionProcessorParameters
