from typing import Any, Dict, List, Optional

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run
from sayou.core.schemas import SayouBlock

from .core.exceptions import RefineryError
from .interfaces.base_normalizer import BaseNormalizer
from .interfaces.base_processor import BaseProcessor
from .normalizer.doc_markdown_normalizer import DocMarkdownNormalizer
from .normalizer.html_text_normalizer import HtmlTextNormalizer
from .normalizer.record_normalizer import RecordNormalizer
from .processor.deduplicator import Deduplicator
from .processor.imputer import Imputer
from .processor.outlier_handler import OutlierHandler
from .processor.pii_masker import PiiMasker
from .processor.text_cleaner import TextCleaner


class RefineryPipeline(BaseComponent):
    """
    Orchestrates the data refinement process.
    1. Selects a Normalizer to convert raw data into standard SayouBlocks.
    2. Runs a chain of Processors to clean and transform the blocks.
    """

    component_name = "RefineryPipeline"

    def __init__(
        self,
        extra_normalizers: Optional[List[BaseNormalizer]] = None,
        processors: Optional[List[BaseProcessor]] = None,
    ):
        super().__init__()
        self.normalizers: Dict[str, BaseNormalizer] = {}

        # 1. Register Default Normalizers
        defaults = [DocMarkdownNormalizer(), HtmlTextNormalizer(), RecordNormalizer()]
        self._register(defaults)

        # 2. Register User Extras
        if extra_normalizers:
            self._register(extra_normalizers)

        # 3. Setup Processors Chain
        self.processors = (
            processors
            if processors is not None
            else [
                TextCleaner(),
                PiiMasker(),
                Deduplicator(),
                Imputer(),
                OutlierHandler(),
            ]
        )

    def _register(self, comps: List[BaseNormalizer]):
        for c in comps:
            for t in getattr(c, "SUPPORTED_TYPES", []):
                self.normalizers[t] = c

    @safe_run(default_return=None)
    def initialize(self, **kwargs):
        """
        Initialize all sub-components (Normalizers and Processors).
        Passes global configuration (like PII masking rules) down to components.
        """
        for norm in set(self.normalizers.values()):
            norm.initialize(**kwargs)

        for proc in self.processors:
            proc.initialize(**kwargs)

        self._log(
            f"Refinery initialized with {len(self.processors)} processors in chain."
        )

    def run(self, raw_data: Any, source_type: str = "standard_doc") -> List[SayouBlock]:
        """
        Execute the refinement pipeline.

        Args:
            raw_data: The raw input data (dict, html string, db row list, etc.)
            source_type: The type of input data (e.g., 'standard_doc', 'html', 'json')

        Returns:
            List[SayouBlock]: A list of clean, normalized blocks.
        """
        # Step 1: Normalize (Structure Transformation)
        normalizer = self.normalizers.get(source_type)
        if not normalizer:
            supported = list(self.normalizers.keys())
            raise RefineryError(
                f"Unknown source_type '{source_type}'. Supported: {supported}"
            )

        try:
            blocks = normalizer.normalize(raw_data)
        except Exception as e:
            self.logger.error(f"Normalization step failed: {e}")
            return []

        # Step 2: Process (Content Cleaning)
        # Processors modify blocks in-place or return new lists
        for processor in self.processors:
            blocks = processor.process(blocks)

        return blocks
