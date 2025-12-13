import inspect
import json
import os
import re
from collections import defaultdict
from enum import Enum
from functools import lru_cache
from logging import Logger
from string import Template
from typing import List, cast, Type, Dict, Tuple, Any, Optional

import jinja2
from collections_extended import RangeMap
from log_with_context import add_logging_context
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText, Annotation, Category, Sentence

from .openai_utils import create_openai_model_enum, openai_chat_completion, gpt_filter, apollo_filter, \
    NO_DEPLOYED_MODELS, OAuthToken, all_filter, check_litellm_defined
from .schema import NERV2, NERV3, SegmentV3, SegmentV2

logger = Logger("pymultirole")
SHOW_INTERNAL = bool(os.getenv("SHOW_INTERNAL", "false"))


class OpenAIFunction(str, Enum):
    add_annotations = "add_annotations"
    add_categories = "add_categories"


class TemplateLanguage(str, Enum):
    none = "none"
    string = "string"
    jinja2 = "jinja2"


class OpenAICompletionBaseParameters(ProcessorParameters):
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
        "$text",
        description="""Contains the prompt as a template string, templates can be:
         <li>a simple (python template string)[https://docs.python.org/3/library/string.html#template-strings]<br/>
         where the document elements can be substituted using `$based`-syntax<br/>
         `$text` to be substituted by the document text<br/>
         `$title` to be substituted by the document title
         <li>a more complex (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/]
         where the document is injected as `doc` and can be used in jinja2 variables like<br/>
         `{{ doc.text }}` to be substituted by the document text etc...""",
        extra="multiline",
    )
    max_tokens: int = Field(
        8192,
        description="""Most models have a context length of 2048 tokens (except for the newest models, which support 8192).""",
    )
    completion_altText: str = Field(
        None,
        description="""<li>If defined: generates the completion as an alternative text of the input document,
    <li>if not: replace the text of the input document.""",
    )
    prompt_altText: str = Field(
        None,
        description="""<li>If defined: add the generated prompt as an alternative text of the input document.""",
    )
    system_prompt: str = Field(
        None,
        description="""Contains the system prompt""",
        extra="multiline,advanced",
    )
    temperature: float = Field(
        1.0,
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
    function: OpenAIFunction = Field(
        None,
        description="""The function to call. Options currently available:</br>
                        <li>`add_categories` - .
                        <li>`add_annotations` - .
                        """,
        extra="advanced" + ("" if SHOW_INTERNAL else ",internal"),
    )
    candidate_labels: Dict[str, str] = Field(
        None,
        description="""The list of possible labels to extract.""",
        extra="advanced,key:label,inject" + ("" if SHOW_INTERNAL else ",internal"),
    )


class OpenAIModel(str, Enum):
    gpt_4 = "gpt-4"
    gpt_4_32k = "gpt-4-32k"
    gpt_4_0613 = "gpt-4-0613"
    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_3_5_turbo_16k = "gpt-3.5-turbo-16k"
    gpt_3_5_turbo_16k_0613 = "gpt-3.5-turbo-16k-0613"


check_litellm_defined()
OPENAI_PREFIX = ""
OPENAI_API_BASE = os.getenv(OPENAI_PREFIX + "OPENAI_API_BASE", None)
CHAT_GPT_MODEL_ENUM, DEFAULT_CHAT_GPT_MODEL = create_openai_model_enum('OpenAIModel2', prefix=OPENAI_PREFIX,
                                                                       base_url=OPENAI_API_BASE,
                                                                       key=gpt_filter if OPENAI_API_BASE is None else all_filter)


class OpenAICompletionParameters(OpenAICompletionBaseParameters):
    base_url: Optional[str] = Field(
        os.getenv(OPENAI_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: CHAT_GPT_MODEL_ENUM = Field(
        DEFAULT_CHAT_GPT_MODEL,
        description="""The [OpenAI model](https://platform.openai.com/docs/models) used for completion. Options currently available:</br>
                        <li>`gpt_4` - More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration.
                        <li>`gpt-3.5-turbo` - Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.
                        """, extra="pipeline-naming-hint"
    )


AZURE_PREFIX = "AZURE_"
AZURE_OPENAI_API_BASE = os.getenv(AZURE_PREFIX + "OPENAI_API_BASE", None)
AZURE_CHAT_GPT_MODEL_ENUM, AZURE_DEFAULT_CHAT_GPT_MODEL = create_openai_model_enum('AzureOpenAIModel',
                                                                                   prefix=AZURE_PREFIX,
                                                                                   base_url=AZURE_OPENAI_API_BASE)


class AzureOpenAICompletionParameters(OpenAICompletionBaseParameters):
    base_url: str = Field(
        os.getenv(AZURE_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: AZURE_CHAT_GPT_MODEL_ENUM = Field(
        AZURE_DEFAULT_CHAT_GPT_MODEL,
        description="""The [Azure OpenAI model](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints#keyword-argument-for-model) deployment name used for completion. It must be deployed on your OpenAI Azure instance.
        """, extra="pipeline-naming-hint"
    )


APOLLO_PREFIX = "APOLLO_"
APOLLO_OPENAI_API_BASE = os.getenv(APOLLO_PREFIX + "OPENAI_API_BASE", None)
if APOLLO_OPENAI_API_BASE is None:
    APOLLO_OPENAI_API_BASE = os.getenv(APOLLO_PREFIX + "API", None)
APOLLO_CHAT_GPT_MODEL_ENUM, APOLLO_DEFAULT_CHAT_GPT_MODEL = create_openai_model_enum('ApolloOpenAIModel',
                                                                                     prefix=APOLLO_PREFIX,
                                                                                     base_url=APOLLO_OPENAI_API_BASE,
                                                                                     key=apollo_filter)


class ApolloOpenAICompletionParameters(OpenAICompletionBaseParameters):
    base_url: str = Field(
        os.getenv(APOLLO_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: APOLLO_CHAT_GPT_MODEL_ENUM = Field(
        APOLLO_DEFAULT_CHAT_GPT_MODEL,
        description="""The Apollo OpenAI model used for completion. It must be deployed in Apollo.
        """, extra="pipeline-naming-hint"
    )


DEEPINFRA_PREFIX = "DEEPINFRA_"
DEEPINFRA_OPENAI_API_BASE = os.getenv(DEEPINFRA_PREFIX + "OPENAI_API_BASE", None)
DEEPINFRA_CHAT_GPT_MODEL_ENUM, DEEPINFRA_DEFAULT_CHAT_GPT_MODEL = create_openai_model_enum('DeepInfraOpenAIModel',
                                                                                           prefix=DEEPINFRA_PREFIX,
                                                                                           base_url=DEEPINFRA_OPENAI_API_BASE)


class DeepInfraOpenAICompletionParameters(OpenAICompletionBaseParameters):
    base_url: str = Field(
        os.getenv(DEEPINFRA_PREFIX + "OPENAI_API_BASE", None),
        description="""OpenAI endpoint base url""", extra="advanced"
    )
    model: DEEPINFRA_CHAT_GPT_MODEL_ENUM = Field(
        None,
        description="""The [DeepInfra 'OpenAI compatible' model](https://deepinfra.com/models?type=text-generation) used for completion. It must be deployed on your [DeepInfra dashboard](https://deepinfra.com/dash).
                        """, extra="pipeline-naming-hint"
    )


# SUPPORTED_LANGUAGES = "de,en,es,fr,it,nl,pt"
def add_annotations(document: Document, params: OpenAICompletionBaseParameters, result: str):
    """Add name entities with a label and a start and end offset in the original text"""
    if not document.sentences:
        document.sentences = [Sentence(start=0, end=len(document.text), metadata=document.metadata)]
    try:
        jresult = json.loads(result.strip())
    except Exception:
        jresult = None
    if jresult is not None and isinstance(jresult, list):
        try:
            jresult_v2 = NERV2.parse_obj(jresult)
            return add_annotations_v2(document, params, jresult_v2.__root__)
        except Exception:
            try:
                jresult_v3 = NERV3.parse_obj(jresult)
                return add_annotations_v3(document, params, jresult_v3.__root__)
            except Exception:
                pass
    return add_annotations_v1(document, params, result)


def add_annotations_v2(document: Document, params: OpenAICompletionBaseParameters, jresult: List[SegmentV2]):
    candidate_names = {v: k for k, v in params.candidate_labels.items()} if (params.candidate_labels and len(
        params.candidate_labels) > 0) else {}
    seen_offsets = defaultdict(set)
    sentMap = {f"{sent.start}:{sent.end}": sent for sent in document.sentences}
    annotations = []
    for result in jresult:
        sent = sentMap[result.id]
        sstart = sent.start
        stext = document.text[sent.start:sent.end]
        for alabel, atexts in result.mentions.items():
            alabelName = candidate_names.get(alabel, None)
            if len(atexts) > 0:
                for atext in atexts:
                    for m in re.finditer(f"\\b{atext}\\b", stext):
                        ann = Annotation(label=alabel, labelName=alabelName, start=m.start() + sstart,
                                         end=m.end() + sstart, text=m.group())
                        if (ann.start, ann.end) not in seen_offsets:
                            seen_offsets[(ann.start, ann.end)].add(ann.label)
                            annotations.append(ann)
                        else:
                            existing = seen_offsets[(ann.start, ann.end)]
                            if ann.label not in existing:
                                seen_offsets[(ann.start, ann.end)].add(ann.label)
                                annotations.append(ann)
    document.annotations = annotations
    return document


def add_annotations_v3(document: Document, params: OpenAICompletionBaseParameters, jresult: List[SegmentV3]):
    candidate_names = {v: k for k, v in params.candidate_labels.items()} if (params.candidate_labels and len(
        params.candidate_labels) > 0) else {}
    seen_offsets = defaultdict(set)
    sentMap = {f"{sent.start}:{sent.end}": sent for sent in document.sentences}
    annotations = []
    for result in jresult:
        sent = sentMap[result.id]
        sstart = sent.start
        stext = document.text[sent.start:sent.end]
        if result.mentions:
            for mention in result.mentions:
                if stext[mention.offset:mention.offset + len(mention.text)] != mention.text:
                    print("Adjust positon")
                else:
                    alabelName = candidate_names.get(mention.label, None)
                    ann = Annotation(label=mention.label, labelName=alabelName, end=mention.offset + len(mention.text) + sstart,
                                     start=mention.start + sstart, text=mention.text)
                    if (ann.start, ann.end) not in seen_offsets:
                        seen_offsets[(ann.start, ann.end)].add(ann.label)
                        annotations.append(ann)
                    else:
                        existing = seen_offsets[(ann.start, ann.end)]
                        if ann.label not in existing:
                            seen_offsets[(ann.start, ann.end)].add(ann.label)
                            annotations.append(ann)
    document.annotations = annotations
    return document


def add_annotations_v1(document: Document, params: OpenAICompletionBaseParameters, result: str):
    candidate_names = {v: k for k, v in params.candidate_labels.items()} if (params.candidate_labels and len(
        params.candidate_labels) > 0) else {}
    seen_offsets = RangeMap()
    sentMap = {f"{sent.start}:{sent.end}": sent for sent in document.sentences}
    label_separator_regex = r"^\s*(?P<label>[^:]+):(?P<text>.+)$"
    segment_separator_regex = r"^\s*<segment id=\"(?P<id>[^\"]+)\">\s*"
    annotations = []
    sresults = result.split("</segment>") if "</segment>" in result else [result]
    for sresult in sresults:
        smatch = re.match(segment_separator_regex, sresult)
        if smatch:
            sid = smatch.group('id')
            sent = sentMap[sid]
            sstart = sent.start
            stext = document.text[sent.start:sent.end]
            sresult = sresult[smatch.end():]
            matches = re.finditer(label_separator_regex, sresult, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                alabel = match.group('label')
                alabelName = candidate_names.get(alabel, None)
                atexts = match.group('text').split('|')
                if len(atexts) > 0 and atexts[0] != "-":
                    for atext in atexts:
                        atext = re.sub(r"\s+", r"\\s+", atext)
                        atext = re.sub(r"\(", r"\\(", atext)
                        atext = re.sub(r"\)", r"\\)", atext)
                        for m in re.finditer(f"\\b{atext}\\b", stext):
                            ann = Annotation(label=alabel, labelName=alabelName, start=m.start() + sstart,
                                             end=m.end() + sstart, text=m.group())
                            annotations.append(ann)

    sorted_annotations = sorted(annotations, key=left_longest_match, reverse=True)
    annotations = []
    for ann in sorted_annotations:
        if (
                ann.end > ann.start
                and seen_offsets.get(ann.start) is None
                and seen_offsets.get(ann.end - 1) is None
        ):
            annotations.append(ann)
            seen_offsets[ann.start: ann.end] = ann
        else:
            # don't keep
            pass
    document.annotations = sorted(annotations, key=natural_order, reverse=True)
    return document


def add_categories(document: Document, params: OpenAICompletionBaseParameters, result: str):
    candidate_names = {v: k for k, v in params.candidate_labels.items()} if (params.candidate_labels and len(
        params.candidate_labels) > 0) else {}
    seen_labels = set()
    label_separator_regex = r"^\s*(?P<label>.+)$"
    matches = re.finditer(label_separator_regex, result, re.MULTILINE)
    categories = []
    for matchNum, match in enumerate(matches, start=1):
        alabel = match.group('label').strip()
        alabelName = candidate_names.get(alabel, None)
        c = Category(label=alabel, labelName=alabelName, score=1.0)
        if alabel not in seen_labels:
            seen_labels.add(alabel)
            categories.append(c)
    document.categories = categories
    return document


FUNCTIONS = {
    "add_annotations": add_annotations,
    "add_categories": add_categories,
}


# noqa: E501
def fix_offsets(doc: Document, indexed_annotations: List[Tuple[int, Annotation]]):
    annotations = []
    seg_annotations = defaultdict(list)
    for i, a in indexed_annotations:
        seg_annotations[i].append(a)
    for i, ann_list in seg_annotations.items():
        ann_list.sort(key=lambda x: x.start, reverse=False)
        seg = doc.sentences[i]
        stext = doc.text[seg.start:seg.end]
        for a in ann_list:
            idx = stext.find(a.text, a.start)
            if idx >= 0:
                a.start = idx + seg.start
                a.end = idx + len(a.text)
                annotations.append(a)
            else:
                logger.warning(f"Can't locate entity {a.text} ({a.start},{a.end}) in text segment: {stext}")
    return annotations


class OpenAICompletionProcessorBase(ProcessorBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it."""
    PREFIX: str = ""
    oauth_token: OAuthToken = OAuthToken()

    def compute_args(self, params: OpenAICompletionBaseParameters, prompt: str, system_prompt: str
                     ) -> Dict[str, Any]:
        messages = [{"role": "system", "content": system_prompt}] if system_prompt is not None else []
        messages.append({"role": "user", "content": prompt})
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
        response = openai_chat_completion(self.PREFIX, self.oauth_token, base_url, **kwargs)
        contents = []
        result = ""
        for choice in response.choices:
            if choice.message.content:
                contents.append(choice.message.content)
            # elif choice.message.function_call:
            #     function_name = choice.message.function_call.name
            #     function = FUNCTIONS.get(function_name, None)
            #     if function:
            #         fuction_to_call = function[0]
            #         function_args = json.loads(choice.message.function_call.arguments)
            #         function_response = fuction_to_call(**function_args)
            #         result = (function_name, function_response)
        if contents:
            result = "\n".join(contents)
        return result

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        # supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)

        params: OpenAICompletionBaseParameters = cast(
            OpenAICompletionBaseParameters, parameters
        )
        OPENAI_MODEL = os.getenv(self.PREFIX + "OPENAI_MODEL", None)
        if OPENAI_MODEL:
            params.model_str = OPENAI_MODEL
        try:
            templ, prompt_templ = get_template(params.prompt)
            system_templ, system_prompt_templ = get_template(params.system_prompt)

            for document in documents:
                with add_logging_context(docid=document.identifier):
                    altTexts = document.altTexts or []
                    result = None
                    prompt = render_template(templ, prompt_templ, document, params)
                    system_prompt = render_template(system_templ, system_prompt_templ, document, params)

                    kwargs = self.compute_args(params, prompt, system_prompt)
                    if kwargs['model'] != NO_DEPLOYED_MODELS:
                        result = self.compute_result(params.base_url, **kwargs)

                    if params.prompt_altText is not None and len(
                            params.prompt_altText
                    ):
                        altTexts.append(
                            AltText(name=params.prompt_altText, text=prompt)
                        )
                    if result:
                        if isinstance(result, str):
                            if params.completion_altText is not None and len(
                                    params.completion_altText
                            ):
                                altTexts.append(
                                    AltText(name=params.completion_altText, text=result)
                                )
                            if params.function is not None:
                                document = FUNCTIONS[params.function.value](document, params, result)
                            elif params.completion_altText is None or not len(
                                    params.completion_altText
                            ):
                                document.text = result
                                document.sentences = []
                                document.annotations = []
                                document.categories = []
                        document.altTexts = altTexts
                        # elif isinstance(result, Tuple):
                        #     function_name, function_response = result
                        #     for _, item in function_response:
                        #         item.labelName = candidate_names.get(item.label)
                        #     if function_name == "add_annotations":
                        #         document.annotations = fix_offsets(document, function_response)
                        #     elif function_name in ["add_categories", "add_exclusive_category"]:
                        #         _, cats = zip(*function_response)
                        #         document.categories = cats
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAICompletionBaseParameters


class OpenAICompletionProcessor(OpenAICompletionProcessorBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it.
    #tags:question-answerer"""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: OpenAICompletionParameters = cast(
            OpenAICompletionParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().process(documents, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAICompletionParameters


class AzureOpenAICompletionProcessor(OpenAICompletionProcessorBase):
    __doc__ = """Generate text using [Azure OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it.
    #tags:question-answerer"""
    PREFIX = AZURE_PREFIX

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: AzureOpenAICompletionParameters = cast(
            AzureOpenAICompletionParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().process(documents, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AzureOpenAICompletionParameters


class ApolloOpenAICompletionProcessor(OpenAICompletionProcessorBase):
    __doc__ = """Generate text using [Apollo OpenAI Text Completion] API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it.
    #tags:question-answerer"""
    PREFIX = APOLLO_PREFIX
    BASE_URL = os.getenv(APOLLO_PREFIX + "OPENAI_API_BASE", os.getenv(APOLLO_PREFIX + "API", None))

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: ApolloOpenAICompletionParameters = cast(
            ApolloOpenAICompletionParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        params.base_url = self.BASE_URL
        return super().process(documents, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ApolloOpenAICompletionParameters


class DeepInfraOpenAICompletionProcessor(OpenAICompletionProcessorBase):
    __doc__ = """Generate text using [DeepInfra Text Completion](https://deepinfra.com/docs/advanced/openai_api) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it.
    #tags:question-answerer"""
    PREFIX = DEEPINFRA_PREFIX

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: DeepInfraOpenAICompletionParameters = cast(
            DeepInfraOpenAICompletionParameters, parameters
        )
        model_str = params.model_str if bool(params.model_str and params.model_str.strip()) else None
        model = params.model.value if params.model is not None else None
        params.model_str = model_str or model
        return super().process(documents, params)

    #     def compute_result(self, **kwargs):
    #         client = set_openai(self.PREFIX)
    #         deepinfra_url = client.base_url
    #         inference_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/v1/inference/{kwargs['model']}"
    #         prompt = kwargs['messages'][0]['content']
    #         input_str = f"""[INST]
    # {prompt}
    # [/INST]"""
    #         response = requests.post(inference_url,
    #                                  json={
    #                                      "input": input_str,
    #                                      "temperature": kwargs['temperature'],
    #                                      "max_new_tokens": kwargs['max_tokens'],
    #                                      "top_p": kwargs['top_p'],
    #                                      "num_responses": kwargs['n'],
    #                                      "frequency_penalty": kwargs['frequency_penalty'],
    #                                      "presence_penalty": kwargs['presence_penalty']
    #                                  },
    #                                  headers={'Content-Type': "application/json", 'Accept': "application/json",
    #                                           'Authorization': f"Bearer {client.api_key}"})
    #         if response.ok:
    #             result = response.json()
    #             return result['text']

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepInfraOpenAICompletionParameters


def flatten_document(doc: Document):
    y = doc.dict()
    out = {}

    def flatten(x, name=""):

        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:

            for a in x:
                flatten(x[a], name + a + "_")

        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:

            i = 0

            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and "language" in doc.metadata:
        return doc.metadata["language"]
    return default


def get_template(prompt: str, default: str = None):
    if prompt:
        if "$" in prompt:
            prompt_templ = Template(prompt)
            return TemplateLanguage.string, prompt_templ
        elif "{{" in prompt:
            environment = get_jinja2_env()
            prompt_dedented = inspect.cleandoc(prompt)
            prompt_templ = environment.from_string(prompt_dedented)
            return TemplateLanguage.jinja2, prompt_templ
    return TemplateLanguage.none, prompt


def render_template(templ, prompt_templ, document, params):
    if templ == TemplateLanguage.string:
        flatten_doc = flatten_document(document)
        prompt = prompt_templ.safe_substitute(flatten_doc)
    elif templ == TemplateLanguage.jinja2:
        prompt = prompt_templ.render(doc=document, parameters=params)
    else:
        prompt = prompt_templ
    return prompt


@lru_cache(maxsize=None)
def get_jinja2_env():
    return jinja2.Environment(extensions=["jinja2.ext.do"])


def left_longest_match(a: Annotation):
    return a.end - a.start, -a.start


def natural_order(a: Annotation):
    return -a.start, a.end - a.start
