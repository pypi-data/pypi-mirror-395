from typing import Iterator

from sayou.core.schemas import SayouPacket, SayouTask

from ..interfaces.base_generator import BaseGenerator


class SqliteGenerator(BaseGenerator):
    """
    Concrete implementation of BaseGenerator for SQL pagination.

    Generates a sequence of database query tasks using LIMIT and OFFSET strategies.
    It continues to yield tasks by incrementing the offset until the Fetcher returns
    an empty result or a partial batch, indicating the end of the dataset.
    """

    component_name = "SqliteGenerator"
    SUPPORTED_TYPES = ["sqlite"]

    def initialize(self, source: str, query: str, batch_size: int = 1000, **kwargs):
        """
        Configure the SQL scanning strategy with pagination.

        Args:
            source (str): The database connection string or file path.
            query (str): The base SQL query (without LIMIT/OFFSET).
            batch_size (int): Number of rows to fetch per task.
            **kwargs: Ignored additional arguments.
        """
        self.conn_str = source
        self.base_query = query.strip().rstrip(";")
        self.batch_size = batch_size
        self.current_offset = 0
        self.stop_flag = False

    def _do_generate(self) -> Iterator[SayouTask]:
        """
        Yield pagination tasks until the stop flag is set.

        Yields:
            Iterator[SayouTask]: Tasks with `source_type='sqlite'` and pagination params.
        """
        while not self.stop_flag:
            paginated_query = f"{self.base_query} LIMIT {self.batch_size} OFFSET {self.current_offset}"

            task = SayouTask(
                source_type="sqlite",
                uri=self.conn_str,
                params={"query": paginated_query},
                meta={"offset": self.current_offset, "batch": self.batch_size},
            )

            yield task

            self.current_offset += self.batch_size

    def _do_feedback(self, result: SayouPacket):
        """
        Determine if pagination should stop based on the fetch result.

        If the number of fetched rows is less than `batch_size` or if the fetch failed,
        the generator stops producing tasks.

        Args:
            result (SayouPacket): The result from the Fetcher.
        """
        # 1. 실패했거나 데이터가 없으면 종료
        if not result.success or not result.data:
            self._log("No data returned or fetch failed. Stopping.", level="warning")
            self.stop_flag = True
            return

        # 2. 가져온 데이터가 배치 사이즈보다 작으면 '마지막 페이지'임
        rows = result.data
        if isinstance(rows, list) and len(rows) < self.batch_size:
            self._log(
                f"Reached end of records (Fetched {len(rows)} < Batch {self.batch_size})."
            )
            self.stop_flag = True
