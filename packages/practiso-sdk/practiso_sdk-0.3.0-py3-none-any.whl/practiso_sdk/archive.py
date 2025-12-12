import xml.etree.ElementTree as Xml
from datetime import datetime, UTC
from io import BytesIO
from typing import Callable, Any, IO
from xml.sax import saxutils

NAMESPACE = 'http://schema.zhufucdev.com/practiso'


def _get_attribute_safe(element: Xml.Element, attr_name: str, convert: Callable[[str], Any] | None = None) -> Any:
    if attr_name not in element.attrib:
        raise TypeError(f'Missing attribute {attr_name} in tag {element.tag}')
    if convert:
        return convert(element.attrib[attr_name])
    else:
        return element.attrib[attr_name]


def _get_simple_tag_name(element: Xml.Element):
    rb = element.tag.index('}')
    if rb < 0:
        return element.tag
    else:
        return element.tag[rb + 1:]


def _namespace_extended(tag: str):
    return '{' + NAMESPACE + '}' + tag


class ArchiveFrame:
    """
    Abstraction of supported frames.
    """

    def append_to_element(self, element: Xml.Element):
        pass

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'ArchiveFrame':
        tag_name = _get_simple_tag_name(element)
        if tag_name == 'text':
            return Text.parse_xml_element(element)
        elif tag_name == 'image':
            return Image.parse_xml_element(element)
        elif tag_name == 'options':
            return Options.parse_xml_element(element)

    def __hash__(self):
        raise RuntimeError(f'Unimplemented method __hash__ for {type(self).__name__}')


class Text(ArchiveFrame):
    """
    Abstraction of a text frame.
    """
    content: str

    def __init__(self, content: str):
        self.content = content

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'text')
        sub.text = saxutils.escape(self.content)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Text':
        if _get_simple_tag_name(element) != 'text':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Text(element.text)

    def __hash__(self):
        return hash(self.content) * 31

    def __eq__(self, other):
        return isinstance(other, Text) and other.content == self.content


class Image(ArchiveFrame):
    """
    Abstraction of an image frame.
    """
    filename: str
    width: int
    height: int
    alt_text: str | None

    def __init__(self, filename: str, width: int, height: int, alt_text: str | None = None):
        self.filename = filename
        self.width = width
        self.height = height
        self.alt_text = alt_text

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'image',
                             attrib={'src': self.filename, 'width': str(self.width), 'height': str(self.height)})
        if self.alt_text:
            sub.attrib['alt'] = self.alt_text

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Image':
        if _get_simple_tag_name(element) != 'image':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Image(
            filename=_get_attribute_safe(element, 'src'),
            width=_get_attribute_safe(element, 'width', int),
            height=_get_attribute_safe(element, 'height', int),
            alt_text=element.attrib['alt'] if 'alt' in element.attrib else None
        )

    def __hash__(self):
        return hash(self.alt_text) * 31 + hash(self.filename) * 31 + hash(self.width * 31 + self.height) * 31

    def __eq__(self, other):
        return isinstance(other, Image) and other.width == self.width \
            and other.height == self.height \
            and other.filename == self.filename \
            and other.alt_text == self.alt_text


class OptionItem:
    """
    Abstraction of a selectable option item.
    """
    is_key: bool
    """
    True if this option is one of or the only correct ones.
    """
    priority: int
    """
    How this option is ranked. Options with the same priority
    will be shuffled randomly, while ones of higher priority (smaller value)
    will be ranked ascent.
    """
    content: ArchiveFrame

    def __init__(self, content: ArchiveFrame, is_key: bool = False, priority: int = 0):
        self.content = content
        self.is_key = is_key
        self.priority = priority

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'item', attrib={'priority': str(self.priority)})
        if self.is_key:
            sub.attrib['key'] = 'true'
        self.content.append_to_element(sub)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'OptionItem':
        if _get_simple_tag_name(element) != 'item':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')
        if len(element) != 1:
            raise TypeError(f'Unexpected {len(element)} children tag')

        return OptionItem(
            content=ArchiveFrame.parse_xml_element(element[0]),
            is_key='key' in element.attrib and element.attrib['key'] == 'true',
            priority=_get_attribute_safe(element, 'priority', int)
        )

    def __hash__(self):
        return hash(self.is_key) * 31 + self.priority * 31 + hash(self.content)

    def __eq__(self, other):
        return isinstance(other, OptionItem) and other.content == self.content \
            and other.is_key == self.is_key \
            and other.priority == self.priority


class Options(ArchiveFrame):
    """
    Abstraction of an options frame, composed of OptionItem.
    """
    content: set[OptionItem]
    name: str | None

    def __init__(self, content: set[OptionItem] | list[OptionItem], name: str | None = None):
        self.content = content if isinstance(content, set) else set(content)
        self.name = name

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'options')
        for item in self.content:
            item.append_to_element(sub)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'ArchiveFrame':
        if _get_simple_tag_name(element) != 'options':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Options(
            content=list(OptionItem.parse_xml_element(e) for e in element if _get_simple_tag_name(e) == 'item'),
            name=element.attrib['name'] if 'name' in element.attrib else None
        )

    def __hash__(self):
        return hash(self.content) * 31 + hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Options) \
            and other.content == self.content \
            and other.name == self.name


class Dimension:
    """
    What knowledge point a question is related to and how much so.
    """
    name: str
    __intensity: float

    @property
    def intensity(self):
        """
        How much the knowledge is related to a question,
        ranging in (0, 1].
        :return: Length of the vector representing the relativity in this dimension.
        """
        return self.__intensity

    @intensity.setter
    def intensity(self, value: float):
        if value > 1 or value <= 0:
            raise ValueError('intensity must fall in range of (0, 1]')
        self.__intensity = value

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'dimension', attrib={'name': self.name})
        sub.text = str(self.intensity)

    def __init__(self, name: str, intensity: float):
        self.name = name
        self.intensity = intensity

    def __hash__(self):
        return hash(self.name) * 31 + hash(self.__intensity)

    def __eq__(self, other):
        return isinstance(other, Dimension) \
            and other.name == self.name \
            and other.__intensity == self.__intensity

    def __repr__(self):
        return f'({self.name}, {self.intensity})'

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Dimension':
        if _get_simple_tag_name(element) != 'dimension':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Dimension(
            name=_get_attribute_safe(element, 'name'),
            intensity=float(element.text)
        )


class Quiz:
    """
    Basic unit of a Practiso session representing a question.
    A quiz is composed of an array of frames, where each either
    presents the question itself or the answerable fields.
    This only affects how the user sees the question and how the system
    handles the answers and recommendations, not how the user interacts
    with the interface.
    """
    name: str | None
    creation_time: datetime
    modification_time: datetime | None
    frames: list[ArchiveFrame]
    dimensions: set[Dimension]

    def __init__(self, frames: list[ArchiveFrame] | None = None,
                 dimensions: set[Dimension] | list[Dimension] | None = None,
                 name: str | None = None, creation_time: datetime | None = None,
                 modification_time: datetime | None = None):
        self.name = name
        self.creation_time = creation_time if creation_time is not None else datetime.now(UTC)
        self.modification_time = modification_time
        self.frames = frames or []
        self.dimensions = set() if dimensions is None \
            else dimensions if isinstance(dimensions, set)\
            else set(dimensions)

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'quiz',
                             attrib={'creation': self.creation_time.isoformat()})
        if self.name:
            sub.attrib['name'] = self.name
        if self.modification_time:
            sub.attrib['modification'] = self.modification_time.isoformat()

        frames_element = Xml.SubElement(sub, 'frames')
        for frame in self.frames:
            frame.append_to_element(frames_element)

        for dimension in self.dimensions:
            dimension.append_to_element(sub)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Quiz':
        if _get_simple_tag_name(element) != 'quiz':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        frames_iter = (e for e in element if _get_simple_tag_name(e) == 'frames')
        try:
            frames_element = next(frames_iter)
        except StopIteration:
            raise TypeError('Expected one frames child, got none')

        try:
            next(frames_iter)
            raise TypeError('Unexpected multi-frames-children tag')
        except StopIteration:
            pass

        return Quiz(
            name=element.attrib['name'] if 'name' in element.attrib else None,
            creation_time=_get_attribute_safe(element, 'creation', datetime.fromisoformat),
            modification_time=datetime.fromisoformat(
                element.attrib['modification']) if 'modification' in element.attrib else None,
            dimensions=list(Dimension.parse_xml_element(e) for e in element if _get_simple_tag_name(e) == 'dimension'),
            frames=list(ArchiveFrame.parse_xml_element(e) for e in frames_element)
        )

    def __eq__(self, other):
        return isinstance(other, Quiz) and other.name == self.name \
            and other.creation_time == self.creation_time \
            and other.modification_time == self.modification_time \
            and other.frames == self.frames \
            and other.dimensions == self.dimensions


class QuizContainer:
    """
    Derivation from a snapshot of the database, removing unnecessary items
    (i.e. reducing SQL relations to direct object composition)
    and is enough to be imported to reconstruct the meaningful part.

    Note: binary resources such as images is probably not included if
    this instance was created by an archive builder, depending on the
    upstream opearation, which can be passing down a file descriptor
    where the actual data is not buffered and relays on the file system.

    Note: this instance is context manageable.
    """
    creation_time: datetime
    content: list[Quiz]
    resources: dict[str, IO]

    def __init__(self, content: list[Quiz], creation_time: datetime | None = None,
                 resources: dict[str, IO] | None = None):
        self.content = content
        self.creation_time = creation_time if creation_time is not None else datetime.now(UTC)
        self.resources = resources if resources else dict()

    def __enter__(self) -> 'QuizContainer':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for fp in self.resources.values():
            fp.close()

    def to_xml_element(self) -> Xml.Element:
        """
        Convert to an XML hierarchy.
        :return: XML hierarchy where the root element represents the archive.
        """
        doc = Xml.Element('archive', attrib={'xmlns': NAMESPACE,
                                             'creation': self.creation_time.isoformat()})
        for quiz in self.content:
            quiz.append_to_element(doc)
        return doc

    def to_bytes(self) -> bytes:
        """
        Convert to a byte array, which once gzipped is ready
        to be imported by Practiso.
        :return: A byte array representing the archive.
        """
        ele = self.to_xml_element()
        xml_bytes = Xml.tostring(ele, xml_declaration=True, encoding='utf-8', short_empty_elements=False)
        if len(self.resources) <= 0:
            return xml_bytes

        buffer = bytearray()
        buffer.extend(xml_bytes)
        buffer.append(0)
        for (name, content) in self.resources.items():
            buffer.extend(name.encode('utf-8'))
            buffer.append(0)
            cb = content.read()
            content.seek(0)
            buffer.extend(len(cb).to_bytes(4))
            buffer.extend(cb)

        return buffer

    def __eq__(self, other):
        return isinstance(other, QuizContainer) \
            and other.content == self.content \
            and other.creation_time == self.creation_time

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'QuizContainer':
        """
        Convert an XML hierarchy to a comprehensible quiz composite.
        :param element: The XML hierarchy to be parsed.
        :return: The quiz composite.
        """
        if _get_simple_tag_name(element) != 'archive':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return QuizContainer(
            creation_time=_get_attribute_safe(element, 'creation', datetime.fromisoformat),
            content=list(Quiz.parse_xml_element(e) for e in element if _get_simple_tag_name(e) == 'quiz')
        )


def open(fp: IO) -> 'QuizContainer':
    """
    Read an archive into a structured object.
    :param fp: The stream to read.
    :return: Quiz container with all resources and frames.
    """
    content = fp.read()
    try:
        i = content.index(0)
    except ValueError:
        i = len(content)

    tree = Xml.ElementTree()
    tree.parse(source=BytesIO(content[:i]))

    container = QuizContainer.parse_xml_element(tree.getroot())
    head = i + 1
    while head < len(content):
        i = content.index(0, head)
        name = content[head:i].decode('utf-8')
        head = i + 1
        size = int.from_bytes(content[head:head + 4])
        head += 4
        container.resources[name] = BytesIO(content[head:head + size])
        head += size

    return container
