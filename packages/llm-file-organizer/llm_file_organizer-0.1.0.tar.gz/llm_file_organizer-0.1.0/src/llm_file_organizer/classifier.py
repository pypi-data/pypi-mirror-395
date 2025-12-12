"""LLM-based classification functionality with multi-provider support and async execution."""

import asyncio
import json
import os
from abc import ABC, abstractmethod
from collections import defaultdict

from .config import Config, LLMProvider
from .scanner import DirectoryInfo, FileInfo

# Known file type mappings - no LLM needed for these
KNOWN_CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".heic", ".tiff", ".raw"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"},
    "Spreadsheets": {".csv", ".xlsx", ".xls", ".numbers", ".ods"},
    "Presentations": {".ppt", ".pptx", ".key", ".odp"},
    "Code": {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala", ".sh", ".bash", ".zsh", ".fish"},
    "Data": {".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".conf", ".cfg"},
    "Archives": {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z", ".dmg", ".iso"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".aiff"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "Ebooks": {".epub", ".mobi", ".azw", ".azw3"},
    "Disk_Images": {".dmg", ".iso", ".img"},
    "Web": {".html", ".htm", ".css", ".scss", ".sass", ".less"},
    "Markdown": {".md", ".markdown", ".rst"},
}

# Reverse lookup: extension -> category
EXTENSION_TO_CATEGORY: dict[str, str] = {}
for category, extensions in KNOWN_CATEGORIES.items():
    for ext in extensions:
        EXTENSION_TO_CATEGORY[ext] = category

# Standard categories to encourage consistent grouping
STANDARD_CATEGORIES = [
    "Archives",
    "Audio",
    "Code",
    "Data",
    "Design",
    "Documents",
    "Finance",
    "Images",
    "Legal",
    "Marketing",
    "Personal",
    "Projects",
    "Reference",
    "Resumes",
    "Screenshots",
    "Software",
    "Video",
    "Work",
]

# Classification prompt - emphasizes BROAD categories
CLASSIFICATION_PROMPT = """Organize these {item_type} into BROAD, general-purpose folders.

ITEMS:
{items_text}

RULES:
1. Use BROAD categories - prefer fewer folders with more items over many specific folders
2. Standard categories to use when applicable: {standard_categories}
3. Only create a new category if items truly don't fit ANY standard category
4. Group similar items together even if not identical (e.g., all CSV data files go in "Data", not separate folders)
5. Use simple, single-word category names when possible

OUTPUT: JSON object mapping category names to arrays of exact item names.
Example: {{"Documents": ["file1.pdf", "file2.doc"], "Data": ["data.csv", "export.json"]}}

JSON only, no explanation:"""

# Consolidation prompt - merges similar categories
CONSOLIDATION_PROMPT = """You have these category folders from organizing files. Many are too specific and should be merged.

CURRENT CATEGORIES:
{categories}

TASK: Merge similar/related categories into broader groups.

RULES:
1. Merge anything data-related (CSVs, datasets, exports, etc.) into "Data"
2. Merge document variants (PDFs, contracts, legal, etc.) into "Documents"
3. Merge code/development/scripts into "Code" or "Projects"
4. Merge media variants into their base type (Images, Video, Audio)
5. Keep max 15-20 final categories
6. Prefer standard names: {standard_categories}

OUTPUT: JSON object mapping EVERY old category to its new (possibly same) category name.
Example: {{"Data_CSV": "Data", "Data_JSON": "Data", "Documents": "Documents", "Legal_Docs": "Documents"}}

JSON only:"""


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def complete(self, prompt: str, json_mode: bool = True) -> str:
        """Send a prompt and get a response."""
        pass

    @abstractmethod
    async def complete_async(self, prompt: str, json_mode: bool = True) -> str:
        """Async version of complete."""
        pass

    def classify(self, items_text: str, item_type: str) -> dict[str, list[str]]:
        """Classify items and return category -> item names mapping."""
        prompt = CLASSIFICATION_PROMPT.format(
            items_text=items_text,
            item_type=item_type,
            standard_categories=", ".join(STANDARD_CATEGORIES),
        )
        response = self.complete(prompt, json_mode=True)
        return json.loads(response.strip()) if response else {}

    async def classify_async(self, items_text: str, item_type: str) -> dict[str, list[str]]:
        """Async version of classify."""
        prompt = CLASSIFICATION_PROMPT.format(
            items_text=items_text,
            item_type=item_type,
            standard_categories=", ".join(STANDARD_CATEGORIES),
        )
        response = await self.complete_async(prompt, json_mode=True)
        return json.loads(response.strip()) if response else {}

    def consolidate(self, categories: list[str]) -> dict[str, str]:
        """Get a mapping to consolidate similar categories."""
        prompt = CONSOLIDATION_PROMPT.format(
            categories="\n".join(f"- {c}" for c in sorted(categories)),
            standard_categories=", ".join(STANDARD_CATEGORIES),
        )
        response = self.complete(prompt, json_mode=True)
        return json.loads(response.strip()) if response else {}

    async def consolidate_async(self, categories: list[str]) -> dict[str, str]:
        """Async version of consolidate."""
        prompt = CONSOLIDATION_PROMPT.format(
            categories="\n".join(f"- {c}" for c in sorted(categories)),
            standard_categories=", ".join(STANDARD_CATEGORIES),
        )
        response = await self.complete_async(prompt, json_mode=True)
        return json.loads(response.strip()) if response else {}


class OpenAIClient(LLMClient):
    """OpenAI API client with async support."""

    def __init__(self, model: str) -> None:
        """Initialize the OpenAI client."""
        try:
            from openai import AsyncOpenAI, OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Set it with: export OPENAI_API_KEY='your-key-here'"
            )

        self.client = OpenAI()
        self.async_client = AsyncOpenAI()
        self.model = model

    def complete(self, prompt: str, json_mode: bool = True) -> str:
        """Send a prompt and get a response."""
        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    async def complete_async(self, prompt: str, json_mode: bool = True) -> str:
        """Async version of complete."""
        kwargs = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = await self.async_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""


class AnthropicClient(LLMClient):
    """Anthropic API client with async support."""

    def __init__(self, model: str) -> None:
        """Initialize the Anthropic client."""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
            )

        self.client = anthropic.Anthropic()
        self.async_client = anthropic.AsyncAnthropic()
        self.model = model

    def _parse_response(self, response_text: str) -> str:
        """Parse response text, handling markdown code blocks."""
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        return response_text.strip()

    def complete(self, prompt: str, json_mode: bool = True) -> str:
        """Send a prompt and get a response."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return self._parse_response(response.content[0].text)

    async def complete_async(self, prompt: str, json_mode: bool = True) -> str:
        """Async version of complete."""
        response = await self.async_client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return self._parse_response(response.content[0].text)


class OllamaClient(LLMClient):
    """Ollama (local) API client with async support."""

    def __init__(self, model: str) -> None:
        """Initialize the Ollama client."""
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "httpx package not installed. Install with: pip install httpx"
            )

        self.model = model
        self.base_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self._httpx = httpx

    def complete(self, prompt: str, json_mode: bool = True) -> str:
        """Send a prompt and get a response."""
        response = self._httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "format": "json" if json_mode else None,
                "stream": False,
            },
            timeout=120.0,
        )
        response.raise_for_status()
        return response.json().get("response", "")

    async def complete_async(self, prompt: str, json_mode: bool = True) -> str:
        """Async version of complete."""
        async with self._httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "format": "json" if json_mode else None,
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json().get("response", "")


def create_llm_client(provider: LLMProvider, model: str) -> LLMClient:
    """Factory function to create the appropriate LLM client."""
    clients = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "ollama": OllamaClient,
    }

    client_class = clients.get(provider)
    if not client_class:
        raise ValueError(f"Unknown LLM provider: {provider}")

    return client_class(model)


class Classifier:
    """Classifies files and directories using an LLM with async parallel execution."""

    # Batch sizes for LLM calls
    SMART_MODE_BATCH_SIZE = 200  # Only unknown files go to LLM
    FULL_MODE_BATCH_SIZE = 500   # All files go to LLM, use larger batches

    # Default max concurrent requests (to avoid rate limiting)
    DEFAULT_MAX_CONCURRENT = 10

    # Threshold for triggering consolidation
    CONSOLIDATION_THRESHOLD = 15  # If more than this many categories, consolidate

    def __init__(
        self,
        config: Config,
        verbose: bool = False,
        mode: str = "smart",
        max_concurrent: int | None = None,
        consolidate: bool = True,
    ) -> None:
        """
        Initialize the classifier.

        Args:
            config: Configuration object
            verbose: Whether to print progress
            mode: "smart" (auto-classify known types) or "full" (everything to LLM)
            max_concurrent: Maximum concurrent LLM requests (default: 10)
            consolidate: Whether to run consolidation pass to merge similar categories
        """
        self.config = config
        self.verbose = verbose
        self.mode = mode
        self.max_concurrent = max_concurrent or self.DEFAULT_MAX_CONCURRENT
        self.consolidate_enabled = consolidate
        self._client: LLMClient | None = None  # Lazy initialization

    @property
    def client(self) -> LLMClient:
        """Lazily initialize the LLM client (only when needed)."""
        if self._client is None:
            # llm_model is guaranteed non-None after Config.__post_init__
            self._client = create_llm_client(self.config.llm_provider, self.config.llm_model)  # type: ignore[arg-type]
        return self._client

    def _get_batch_size(self) -> int:
        """Get the batch size to use."""
        # Use config batch_size if explicitly set to non-default
        if self.config.batch_size != 50:  # 50 is the old default
            return self.config.batch_size
        # Otherwise use mode-appropriate default
        return self.FULL_MODE_BATCH_SIZE if self.mode == "full" else self.SMART_MODE_BATCH_SIZE

    def _pre_classify_files(
        self, files: list[FileInfo]
    ) -> tuple[dict[str, list[str]], list[FileInfo]]:
        """
        Pre-classify files based on known extensions.
        Returns (classifications, remaining_files_needing_llm).
        """
        classifications: dict[str, list[str]] = defaultdict(list)
        unknown_files: list[FileInfo] = []

        for file in files:
            ext = file.extension.lower() if file.extension else ""
            if ext in EXTENSION_TO_CATEGORY:
                category = EXTENSION_TO_CATEGORY[ext]
                classifications[category].append(file.name)
            else:
                unknown_files.append(file)

        return dict(classifications), unknown_files

    def _format_items(
        self, items: list[FileInfo] | list[DirectoryInfo]
    ) -> str:
        """Format items for the LLM prompt."""
        descriptions = []
        for item in items:
            desc = f"- {item.name}"
            if isinstance(item, FileInfo) and item.extension:
                desc += f" ({item.extension})"
            if isinstance(item, DirectoryInfo) and item.sample_contents:
                desc += f" [contains: {', '.join(item.sample_contents[:3])}]"
            descriptions.append(desc)
        return "\n".join(descriptions)

    def _apply_consolidation(
        self,
        classifications: dict[str, list[str]],
        mapping: dict[str, str],
    ) -> dict[str, list[str]]:
        """Apply a consolidation mapping to classifications."""
        consolidated: dict[str, list[str]] = defaultdict(list)

        for old_category, items in classifications.items():
            new_category = mapping.get(old_category, old_category)
            consolidated[new_category].extend(items)

        return dict(consolidated)

    async def _consolidate_categories_async(
        self,
        file_classifications: dict[str, list[str]],
        dir_classifications: dict[str, list[str]],
    ) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """Consolidate similar categories using one final LLM call."""
        all_categories = set(file_classifications.keys()) | set(dir_classifications.keys())

        # Skip if under threshold
        if len(all_categories) <= self.CONSOLIDATION_THRESHOLD:
            if self.verbose:
                print(f"  {len(all_categories)} categories - no consolidation needed")
            return file_classifications, dir_classifications

        if self.verbose:
            print(f"  Consolidating {len(all_categories)} categories...")

        try:
            mapping = await self.client.consolidate_async(list(all_categories))

            # Apply mapping
            new_file_class = self._apply_consolidation(file_classifications, mapping)
            new_dir_class = self._apply_consolidation(dir_classifications, mapping)

            new_count = len(set(new_file_class.keys()) | set(new_dir_class.keys()))
            if self.verbose:
                print(f"  Consolidated to {new_count} categories")

            return new_file_class, new_dir_class

        except Exception as e:
            if self.verbose:
                print(f"  Warning: Consolidation failed: {e}")
            return file_classifications, dir_classifications

    async def classify_batch_async(
        self,
        items: list[FileInfo] | list[DirectoryInfo],
        item_type: str,
        batch_num: int = 0,
        total_batches: int = 0,
    ) -> dict[str, list[str]]:
        """Classify a batch of items asynchronously."""
        items_text = self._format_items(items)
        try:
            result = await self.client.classify_async(items_text, item_type)
            if self.verbose and total_batches > 1:
                print(f"    Batch {batch_num}/{total_batches} complete")
            return result
        except json.JSONDecodeError as e:
            if self.verbose:
                print(f"Warning: Failed to parse LLM response (batch {batch_num}): {e}")
            return {"Unsorted": [item.name for item in items]}
        except Exception as e:
            if self.verbose:
                print(f"Warning: LLM request failed (batch {batch_num}): {e}")
            return {"Unsorted": [item.name for item in items]}

    async def _run_batches_async(
        self,
        batches: list[tuple[list[FileInfo] | list[DirectoryInfo], str, int, int]],
    ) -> list[dict[str, list[str]]]:
        """Run multiple batches with concurrency limit."""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def limited_classify(
            items: list[FileInfo] | list[DirectoryInfo],
            item_type: str,
            batch_num: int,
            total_batches: int,
        ) -> dict[str, list[str]]:
            async with semaphore:
                return await self.classify_batch_async(items, item_type, batch_num, total_batches)

        tasks = [
            limited_classify(items, item_type, batch_num, total_batches)
            for items, item_type, batch_num, total_batches in batches
        ]

        return await asyncio.gather(*tasks)

    async def classify_all_async(
        self,
        files: list[FileInfo],
        directories: list[DirectoryInfo],
    ) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """Classify all files and directories using async parallel execution."""
        file_classifications: dict[str, list[str]] = defaultdict(list)
        dir_classifications: dict[str, list[str]] = defaultdict(list)

        batch_size = self._get_batch_size()
        batches: list[tuple[list[FileInfo] | list[DirectoryInfo], str, int, int]] = []

        # Prepare file batches
        if files:
            if self.mode == "smart":
                # Smart mode: Pre-classify files by known extensions
                pre_classified, unknown_files = self._pre_classify_files(files)

                # Add pre-classified files
                for category, names in pre_classified.items():
                    file_classifications[category].extend(names)

                if self.verbose:
                    known_count = len(files) - len(unknown_files)
                    if known_count > 0:
                        print(f"  Auto-classified {known_count} files by extension")

                files_for_llm = unknown_files
            else:
                # Full mode: Send all files to LLM
                files_for_llm = files

            # Create file batches
            if files_for_llm:
                total_file_batches = (len(files_for_llm) - 1) // batch_size + 1
                if self.verbose:
                    print(f"  Classifying {len(files_for_llm)} files ({total_file_batches} batch{'es' if total_file_batches > 1 else ''})...")

                for i in range(0, len(files_for_llm), batch_size):
                    batch = files_for_llm[i : i + batch_size]
                    batch_num = i // batch_size + 1
                    batches.append((batch, "files", batch_num, total_file_batches))
            elif self.verbose:
                print("  No files need LLM classification")

        # Create directory batches
        if directories:
            total_dir_batches = (len(directories) - 1) // batch_size + 1

            if self.verbose:
                print(f"  Classifying {len(directories)} directories ({total_dir_batches} batch{'es' if total_dir_batches > 1 else ''})...")

            for i in range(0, len(directories), batch_size):
                batch = directories[i : i + batch_size]
                batch_num = i // batch_size + 1
                batches.append((batch, "directories/folders", batch_num, total_dir_batches))

        # Run all batches concurrently
        if batches:
            total_batches = len(batches)
            if self.verbose:
                print(f"  Running {total_batches} LLM requests (max {self.max_concurrent} concurrent)...")

            results = await self._run_batches_async(batches)

            # Merge results
            for (items, item_type, _, _), classifications in zip(batches, results):
                target = file_classifications if item_type == "files" else dir_classifications
                for category, names in classifications.items():
                    target[category].extend(names)

            if self.verbose:
                print(f"  Classification complete!")

        # Consolidation pass
        if self.consolidate_enabled:
            file_classifications, dir_classifications = await self._consolidate_categories_async(
                dict(file_classifications), dict(dir_classifications)
            )

        return dict(file_classifications), dict(dir_classifications)

    def classify_all(
        self,
        files: list[FileInfo],
        directories: list[DirectoryInfo],
    ) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """Classify all files and directories (runs async internally)."""
        return asyncio.run(self.classify_all_async(files, directories))
