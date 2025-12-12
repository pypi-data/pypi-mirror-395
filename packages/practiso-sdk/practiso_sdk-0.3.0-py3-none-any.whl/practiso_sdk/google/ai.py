import json
import xml.etree.ElementTree as ElementTree

import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

from practiso_sdk.archive import Quiz, Dimension
from practiso_sdk.build import VectorizeAgent, RetriableError


def get_dimension_from_ai_safe(text: str) -> set[Dimension]:
    try:
        response_content = json.loads(text)
    except json.JSONDecodeError:
        raise RetriableError('invalid json format')
    if 'dimensions' not in response_content or not all(
            'name' in dim and 'intensity' in dim \
            and isinstance(dim['name'], str) and isinstance(dim['intensity'], float) \
            for dim in response_content['dimensions']):
        raise RetriableError('invalid response format')

    return set(Dimension(dim['name'], dim['intensity']) for dim in response_content['dimensions'])


class GeminiAgent(VectorizeAgent):
    """
    Uses Gemini flash to determine dimensions of questions.
    """
    __api_key: str
    __model: genai.GenerativeModel

    def __init__(self, api_key: str, temperature: float = 0, top_p: float = 0.95, top_k: float = 40):
        self.__api_key = api_key
        # noinspection PyTypeChecker
        self.__model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                'temperature': temperature,
                'top_p': top_p,
                'top_k': top_k,
                'max_output_tokens': 8192,
                'response_schema': content.Schema(
                    type=content.Type.OBJECT,
                    enum=[],
                    required=['dimensions'],
                    properties={
                        'dimensions': content.Schema(
                            type=content.Type.ARRAY,
                            items=content.Schema(
                                type=content.Type.OBJECT,
                                enum=[],
                                required=['name', 'intensity'],
                                properties={
                                    'name': content.Schema(
                                        type=content.Type.STRING,
                                    ),
                                    'intensity': content.Schema(
                                        type=content.Type.NUMBER,
                                    ),
                                },
                            ),
                        ),
                    },
                ),
                'response_mime_type': 'application/json',
            },
            system_instruction='You are a student tagging quizzes from your collections. '
                               'You always look at the XML presentation of a quiz and '
                               'determine what category the quiz falls into and how much '
                               'so, rating the intensity from 0 to 1. You always name the '
                               'category in the language the quiz is written in, and break '
                               'the categories into several small knowledge points. '
                               'Here comes your first quiz.',
        )

    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        genai.configure(api_key=self.__api_key)

        container = ElementTree.Element('container')
        quiz.append_to_element(container)
        quiz_xml = str(ElementTree.tostring(container[0], encoding='utf-8', xml_declaration=False))

        quiz_content = content.Content()
        quiz_content.role = 'user'
        xml_part = content.Part()
        xml_part.text = quiz_xml
        quiz_content.parts = [xml_part]

        chat_session = self.__model.start_chat(history=[quiz_content])
        response = await chat_session.send_message_async("INSERT_INPUT_HERE")

        return get_dimension_from_ai_safe(response.text)
