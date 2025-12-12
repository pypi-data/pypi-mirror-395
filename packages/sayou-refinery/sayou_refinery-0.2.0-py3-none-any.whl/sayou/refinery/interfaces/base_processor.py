from abc import abstractmethod
from typing import List

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import measure_time
from sayou.core.schemas import SayouBlock

from ..core.exceptions import ProcessingError


class BaseProcessor(BaseComponent):
    """
    (Tier 1) Abstract base class for processing/cleaning SayouBlock.

    Processors operate on data that is already normalized. They can modify content
    (e.g., PII masking, Imputation) or filter out blocks (e.g., Deduplication).
    """

    component_name = "BaseProcessor"

    @measure_time
    def process(self, blocks: List[SayouBlock]) -> List[SayouBlock]:
        """
        Execute the processing logic on a list of blocks.

        Args:
            blocks: Input list of SayouBlocks.

        Returns:
            List[SayouBlock]: Processed list of SayouBlocks.

        Raises:
            ProcessingError: If processing logic fails.
        """
        try:
            if not blocks:
                return []

            return self._do_process(blocks)

        except Exception as e:
            wrapped_error = ProcessingError(f"[{self.component_name}] Failed: {str(e)}")
            self.logger.error(wrapped_error, exc_info=True)
            raise wrapped_error

    @abstractmethod
    def _do_process(self, blocks: List[SayouBlock]) -> List[SayouBlock]:
        """
        [Abstract Hook] Implement cleaning/filtering logic.

        Args:
            blocks: List of input SayouBlocks.

        Returns:
            List[SayouBlock]: Modified list of SayouBlocks.
        """
        raise NotImplementedError
