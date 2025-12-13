import importlib
import pkgutil
from typing import Iterator

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run
from sayou.core.registry import COMPONENT_REGISTRY
from sayou.core.schemas import SayouPacket, SayouTask

from .interfaces.base_fetcher import BaseFetcher
from .interfaces.base_generator import BaseGenerator


class ConnectorPipeline(BaseComponent):
    """
    Orchestrates the data collection process by connecting Generators and Fetchers.
    """

    component_name = "ConnectorPipeline"

    def __init__(self, **kwargs):
        """
        Initializes the pipeline and discovers available components.

        Sets up the internal storage for generators and fetchers, scans specific
        package paths to automatically discover plugins, and loads them from the
        global registry into the local mapping.

        Args:
            **kwargs: Configuration arguments passed to the parent component.
        """
        super().__init__()

        self.gen_map = {}
        self.fetch_map = {}

        self._register("sayou.connector.generator")
        self._register("sayou.connector.fetcher")
        self._register("sayou.connector.plugins")

        self._load_from_registry()

    def _register(self, package_name: str):
        """
        Automatically discovers and registers plugins from the specified package.

        Scans the directory of the given package name and attempts to import all
        submodules found. Importing these modules triggers the `@register_component`
        decorator attached to the classes, effectively registering them into the
        global `COMPONENT_REGISTRY`.

        Args:
            package_name (str): The dot-separated Python package path to scan
                                (e.g., "sayou.connector.generator").
        """
        try:
            package = importlib.import_module(package_name)
            if hasattr(package, "__path__"):
                for _, name, _ in pkgutil.iter_modules(package.__path__):
                    full_name = f"{package_name}.{name}"
                    try:
                        importlib.import_module(full_name)
                        self._log(f"Discovered module: {full_name}", level="debug")
                    except Exception as e:
                        self._log(
                            f"Failed to import module {full_name}: {e}", level="warning"
                        )
        except ImportError as e:
            self._log(f"Package not found: {package_name} ({e})", level="warning")

    def _load_from_registry(self):
        """
        Populates local component maps from the global registry.

        Iterates through the global `COMPONENT_REGISTRY` to retrieve registered
        generator and fetcher classes. It stores references to these classes in
        `self.gen_map` and instantiates fetchers in `self.fetch_map`.
        """
        for name, cls in COMPONENT_REGISTRY["generator"].items():
            self.gen_map[name] = cls
            supported = getattr(cls, "SUPPORTED_TYPES", [])
            for t in supported:
                self.gen_map[t] = cls

        for name, cls in COMPONENT_REGISTRY["fetcher"].items():
            instance = cls()
            for t in getattr(instance, "SUPPORTED_TYPES", []):
                self.fetch_map[t] = instance

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
        generator_cls = self._resolve_generator(source, strategy)
        generator = generator_cls()

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
