from abc import abstractmethod
from typing import Iterator

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import measure_time
from sayou.core.schemas import SayouPacket, SayouTask

from ..core.exceptions import GeneratorError


class BaseGenerator(BaseComponent):
    """
    (Tier 1) Abstract base class for all task generators.

    Generators are responsible for discovering resources (e.g., listing files,
    crawling links) and creating `SayouTask` objects for the Fetcher.
    """

    component_name = "BaseGenerator"
    SUPPORTED_TYPES = []

    @measure_time
    def generate(self) -> Iterator[SayouTask]:
        """
        Execute the generation strategy and yield tasks one by one.

        This method handles the lifecycle of the generation process, including
        logging and error boundary protection.

        Yields:
            Iterator[SayouTask]: An iterator of tasks to be processed by Fetchers.
        """
        self._log(f"Starting generation strategy: {self.component_name}")
        count = 0
        try:
            for task in self._do_generate():
                count += 1
                yield task
        except Exception as e:
            wrapped_error = GeneratorError(
                f"[{self.component_name}] Strategy crashed: {str(e)}"
            )
            self.logger.error(wrapped_error, exc_info=True)
        finally:
            self._log(f"Generator finished. Total tasks yielded: {count}")

    @abstractmethod
    def _do_generate(self) -> Iterator[SayouTask]:
        """
        [Abstract Hook] Implement the logic to discover resources.

        Yields:
            SayouTask: A task object representing a unit of work.
        """
        raise NotImplementedError

    def feedback(self, packet: SayouPacket):
        """
        Receive feedback from the execution result of a task.

        This allows the generator to adjust its strategy dynamically
        (e.g., adding new links found in a crawled page).

        Args:
            packet (SayouPacket): The result packet from the Fetcher.
        """
        self._do_feedback(packet)

    def _do_feedback(self, packet: SayouPacket):
        """
        [Optional Hook] Override this to handle feedback logic.
        """
        pass
