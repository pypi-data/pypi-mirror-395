from functools import reduce
import asyncio
import os.path
import uuid
from datetime import datetime, UTC
from typing import Any, IO

import PIL.Image
import tqdm

from practiso_sdk.archive import Quiz, ArchiveFrame, OptionItem, Text, Image, Options, QuizContainer, Dimension


class RetriableError(Exception):
    def __init__(self, message: str):
        """
        Initialize an RetriableError, and expect the raising
        procedure be restarted.
        :param message: Message to display, should start in lowercase.
        """
        self.message = message
        super().__init__(message)


class TooManyRetrialsError(Exception):
    def __init__(self, last: RetriableError):
        self.last_retrial = last

    def __repr__(self):
        return self.last_retrial.message

    def __str__(self):
        return f'TooManyRetrials: {self.last_retrial.message}'


class VectorizeAgent:
    """
    Determines what categories a question falls into and how much so.
    """

    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        """
        Throws RetriableError if any exceptional situation strikes, meaning
        this is supposed to be caught and the procedure is called again.
        """
        pass


class DefaultVectorizeAgent(VectorizeAgent):
    """
    An VectorizeAgent where all results are predetermined.
    """
    default: set[Dimension]

    def __init__(self, default: set[Dimension] | list[Dimension]):
        """
        Initialize a DefaultVectorizeAgent.
        :param default: The predetermined categorization result.
        """
        self.default = default if isinstance(default, set) else set(default)

    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        return self.default


class RateLimitedVectorizeAgent(VectorizeAgent):
    """
    A VectorizeAgent which wraps another agent
    and limits how much execution there is in some time.
    """
    __wrapped: VectorizeAgent
    __rpm: float
    __batch_size: int
    __semaphore: asyncio.Semaphore | None
    __mutex: asyncio.Lock

    def __init__(self, wrapped: VectorizeAgent, rpm: float, batch_size: int = 0):
        """
        Initialize a rate-limited vectorize agent. This agent wraps around another agent
        and limits the request rate.
        :param wrapped: The underlying agent which actually carries the action.
        :param rpm: Request per minute. Can be any positive real number.
        :param batch_size: How many requests are sent together.
        """
        self.__wrapped = wrapped
        self.__rpm = rpm
        self.__batch_size = batch_size
        self.__mutex = asyncio.Lock()
        self.__semaphore = None

    def __reset_signals(self):
        if self.__semaphore.locked():
            for _ in range(self.__batch_size):
                self.__semaphore.release()
        self.__semaphore = None

    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        await self.__mutex.acquire()

        if self.__semaphore is None and self.__batch_size > 0:
            self.__semaphore = asyncio.Semaphore(self.__batch_size)

            asyncio.get_event_loop().call_later(60 / self.__rpm * self.__batch_size, self.__reset_signals)

        if self.__semaphore:
            await self.__semaphore.acquire()

        try:
            return await self.__wrapped.get_dimensions(quiz)
        finally:
            self.__mutex.release()


class Builder:
    """
    Utility class to build an archive.
    """

    def __init__(self, creation_time: datetime | None = None):
        self.__quizzes = list()
        self.__staging_stack = list()
        self.__creation_time = creation_time if creation_time else datetime.now(UTC)
        self.__resource_buffer = dict()

    def begin_quiz(self, name: str | None = None, creation_time: datetime | None = None,
                   modification_time: datetime | None = None) -> 'Builder':
        """
        Begin a quiz, which is added after end_quiz is called.
        """
        self.__staging_stack.append(Quiz(list(), set(), name, creation_time, modification_time))
        return self

    def end_quiz(self) -> 'Builder':
        """
        Add the previously begun quiz to the resulting archive.
        """
        self.__quizzes.append(self.__pop_staged_stack_safe([Quiz]))
        return self

    def __get_staged_peak_safe(self, t: list[type]) -> Any:
        e = self.__staging_stack[-1]
        if not any(isinstance(e, x) for x in t):
            p1 = ', '.join(x.__name__ for x in t[:-1])
            p2 = t[-1].__name__
            raise TypeError(f'Begin a {p1} or {p2} first' if p1 else f'Begin a {p2} first')
        return e

    def __pop_staged_stack_safe(self, t: list[type]) -> Any:
        e = self.__get_staged_peak_safe(t)
        self.__staging_stack.pop()
        return e

    def add_text(self, content: str) -> 'Builder':
        """
        Add a text frame directly into the current quiz / option.
        """
        peak = self.__get_staged_peak_safe([Quiz, OptionItem])
        if isinstance(peak, Quiz):
            peak.frames.append(Text(content))
        elif isinstance(peak, OptionItem):
            peak.content = Text(content)
        return self

    def begin_image(self, alt_text: str | None = None) -> 'Builder':
        """
        Begin an image frame, which is added to the current quiz / option
        after calling end_image.
        """
        self.__staging_stack.append(Image('', 0, 0, alt_text))
        return self

    def attach_image(self, fp: IO, extension: str = '') -> 'Builder':
        """
        Stream into the staging resource buffer, and set the current image frame
        to its size if it is seekable.
        The resource buffer will be baked into the result when calling build.
        :param fp: The image content.
        :param extension: Optional suffix to the resource id.
        """
        if extension and not extension.startswith('.'):
            extension = '.' + extension

        res_id = str(uuid.uuid4()) + extension
        self.__resource_buffer[res_id] = fp

        frame = self.__get_staged_peak_safe([Image])
        frame.filename = res_id
        if fp.seekable():
            image = PIL.Image.open(fp)
            (width, height) = image.size
            frame.width = width
            frame.height = height

            fp.seek(0)

        return self

    def attach_image_file(self, filename: str) -> 'Builder':
        """
        Copy a file into the staging resource buffer, and set the current image frame
        to its size. The resource buffer will be baked into the result when calling build.
        The frame filename doesn't represent the argumental one.
        :param filename: the filename in local system.
        """
        _, extension = os.path.splitext(filename)
        return self.attach_image(open(filename, 'rb'), extension)

    def end_image(self) -> 'Builder':
        """
        Add the previously begun image frame into the current
        quiz / option.
        """
        image = self.__pop_staged_stack_safe([Image])
        peak = self.__get_staged_peak_safe([Quiz, OptionItem])
        if isinstance(peak, Quiz):
            peak.frames.append(image)
        elif isinstance(peak, OptionItem):
            peak.content = image
        return self

    def begin_options(self, name: str | None = None) -> 'Builder':
        """
        Begin an options frame, which is added to the current quiz
        after end_options is called.
        :param name: caption of the frame
        """
        self.__staging_stack.append(Options(set(), name))
        return self

    def end_options(self) -> 'Builder':
        """
        Add the options frame previously begun to the current quiz.
        """
        e = self.__pop_staged_stack_safe([Options])
        self.__get_staged_peak_safe([Quiz]).frames.append(e)
        return self

    def begin_option(self, is_key: bool = False, priority: int = 0) -> 'Builder':
        """
        Begin an option item, which is added to the current options frame
        after end_option is called.
        :param is_key: True if the option is considered one of or the only answer
        :param priority: how this option should be sorted when a Practiso session begins
        :return:
        """
        self.__staging_stack.append(OptionItem(ArchiveFrame(), is_key, priority))
        return self

    def end_option(self) -> 'Builder':
        """
        Add the previously begun option to the current options frame.
        """
        e: OptionItem = self.__pop_staged_stack_safe([OptionItem])
        if type(e) == ArchiveFrame:
            raise ValueError('Empty option item')

        self.__get_staged_peak_safe([Options]).content.add(e)

        return self

    async def build(self, vectorizer: VectorizeAgent | None = None) -> 'QuizContainer':
        """
        Call it a day.
        :param vectorizer: The agent used to determine what dimensions are the quizzes respectively falls into.
        :return: The archive.
        """
        if vectorizer is not None:
            with tqdm.tqdm(total=len(self.__quizzes)) as pbar:
                async def update_dimensions(quiz: Quiz):
                    retrials = 0
                    while True:
                        try:
                            quiz.dimensions = await vectorizer.get_dimensions(quiz)
                            break
                        except RetriableError as e:
                            print(f'Error from {type(vectorizer).__name__}: {e.message}')
                            retrials += 1
                            if retrials >= 10:
                                raise RuntimeError(e.message)

                    pbar.update(1)

                await asyncio.gather(*(update_dimensions(quiz) for quiz in self.__quizzes))

        return QuizContainer(self.__quizzes, self.__creation_time, self.__resource_buffer)

def merge(*builders: Builder) -> Builder:
    if len(builders) == 0:
        return Builder()
    result = Builder(creation_time=builders[0]._Builder__creation_time)
    result._Builder__quizzes = list(reduce(lambda b, s: b + s._Builder__quizzes, builders, []))
    return result
    
