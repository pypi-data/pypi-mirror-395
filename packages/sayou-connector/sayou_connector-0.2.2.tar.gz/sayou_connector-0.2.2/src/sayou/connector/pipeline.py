from typing import Dict, Iterator, List, Optional

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run
from sayou.core.schemas import SayouPacket, SayouTask

from .fetcher.file_fetcher import FileFetcher
from .fetcher.requests_fetcher import RequestsFetcher
from .fetcher.sqlite_fetcher import SqliteFetcher
from .generator.file_generator import FileGenerator
from .generator.requests_generator import RequestsGenerator
from .generator.sqlite_generator import SqliteGenerator
from .interfaces.base_fetcher import BaseFetcher
from .interfaces.base_generator import BaseGenerator


class ConnectorPipeline(BaseComponent):
    """
    Orchestrates the data collection process by connecting Generators and Fetchers.
    """

    component_name = "ConnectorPipeline"

    def __init__(
        self,
        extra_generators: Optional[List[BaseGenerator]] = None,
        extra_fetchers: Optional[List[BaseFetcher]] = None,
    ):
        """
        Initialize the pipeline with default and optional plugins.

        Args:
            extra_generators (Optional[List[BaseGenerator]]): Custom generators to register.
            extra_fetchers (Optional[List[BaseFetcher]]): Custom fetchers to register.
        """
        super().__init__()

        self.gen_map: Dict[str, BaseGenerator] = {}
        self.fetch_map: Dict[str, BaseFetcher] = {}

        self._register(
            self.gen_map, [FileGenerator(), SqliteGenerator(), RequestsGenerator()]
        )
        self._register(
            self.fetch_map, [FileFetcher(), SqliteFetcher(), RequestsFetcher()]
        )

        if extra_generators:
            self._register(self.gen_map, extra_generators)
        if extra_fetchers:
            self._register(self.fetch_map, extra_fetchers)

    def _register(self, target_map, components):
        """
        Register a list of components into the target mapping.

        Args:
            target_map (dict): The dictionary to store the components (key: type).
            components (list): List of component instances to register.
        """
        for c in components:
            for t in getattr(c, "SUPPORTED_TYPES", []):
                target_map[t] = c

    @safe_run(default_return=None)
    def initialize(self, **kwargs):
        """
        Perform global initialization for the pipeline.

        This method is protected by safe_run decorators in the actual implementation
        to prevent initialization crashes.

        Args:
            **kwargs: Global configuration parameters.
        """
        self._log("ConnectorPipeline initialized.")

    def run(
        self, source: str, strategy: str = "auto", **kwargs
    ) -> Iterator[SayouPacket]:
        """
        Execute the collection pipeline.

        This is the main entry point. It selects a Generator based on the strategy,
        produces Tasks, routes them to the appropriate Fetcher, and yields the results.

        Args:
            source (str): The root source (e.g., file path, URL, connection string).
            strategy (str): The name of the generator strategy to use (default: "auto").
            **kwargs: Additional arguments passed to the Generator's initialize method.

        Yields:
            Iterator[SayouPacket]: A stream of packets containing fetched data.

        Raises:
            ValueError: If the specified strategy is not registered.
        """
        # 1. Generator 선택
        # v0.1.x
        # generator = self.gen_map.get(strategy)
        # if not generator:
        #     raise ValueError(f"Unknown strategy: {strategy}")
        # v0.2.0
        generator = self._resolve_generator(source, strategy)

        # 2. Generator 초기화
        generator.initialize(source=source, **kwargs)
        self._log(f"Connector started using strategy '{strategy}' on '{source}'")

        # 3. Execution Loop
        count = 0
        success_count = 0

        for task in generator.generate():
            if not isinstance(task, SayouTask):
                self._log(
                    f"Invalid task type from generator: {type(task)}", level="warning"
                )
                continue

            # 4. Fetcher 라우팅
            fetcher = self.fetch_map.get(task.source_type)
            if not fetcher:
                self._log(
                    f"Skipping task {task.uri}: No fetcher for type '{task.source_type}'"
                )
                continue

            # 5. Fetch 수행
            packet = fetcher.fetch(task)

            # 6. 결과 처리
            if packet.success:
                success_count += 1
                yield packet
            else:
                self._log(f"Fetch failed: {packet.error}")

            # 7. Feedback Loop
            generator.feedback(packet)
            count += 1

        self._log(f"Connector finished. Processed: {count}, Success: {success_count}")

    def _resolve_generator(self, source: str, strategy: str) -> BaseGenerator:
        """
        Determines the appropriate generator strategy to use.

        Prioritizes the strategy explicitly specified by the user. If the strategy
        is set to 'auto' or None, it attempts to detect the most suitable generator
        based on the source string using the `can_handle` method of registered generators.

        Args:
            source (str): The input source string (e.g., file path, URL, connection string).
            strategy (str): The name of the strategy to use (e.g., 'file', 'sqlite').
                            If 'auto' or None, automatic detection is performed.

        Returns:
            BaseGenerator: The initialized generator instance ready for execution.

        Raises:
            ValueError: If a specific strategy is requested but not found in the registry.
        """
        if strategy and strategy != "auto":
            gen = self.gen_map.get(strategy)
            if not gen:
                raise ValueError(f"Unknown strategy: {strategy}")
            return gen

        best_score = 0.0
        best_gen = None

        for gen in self.gen_map.values():
            score = gen.can_handle(source)
            if score > best_score:
                best_score = score
                best_gen = gen

        if best_gen and best_score > 0.5:
            self._log(
                f"Auto-detected strategy: '{best_gen.component_name}' (Score: {best_score})"
            )
            return best_gen

        self._log(
            "Auto-detection failed. Falling back to default strategy 'file'.",
            level="warning",
        )
        return self.gen_map["file"]
