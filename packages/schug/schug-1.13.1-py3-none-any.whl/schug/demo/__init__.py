from pathlib import Path

import importlib_resources

# Paths
EXONS_37_FILE_PATH: Path = Path(
    importlib_resources.files("schug"), "demo", "exons_37.tsv"
)
EXONS_38_FILE_PATH: Path = Path(
    importlib_resources.files("schug"), "demo", "exons_38.tsv"
)
GENES_37_FILE_PATH: Path = Path(
    importlib_resources.files("schug"), "demo", "genes_37.tsv"
)
GENES_38_FILE_PATH: Path = Path(
    importlib_resources.files("schug"), "demo", "genes_38.tsv"
)
TRANSCRIPTS_37_FILE_PATH: Path = Path(
    importlib_resources.files("schug"), "demo", "transcripts_37.tsv"
)
TRANSCRIPTS_38_FILE_PATH: Path = Path(
    importlib_resources.files("schug"), "demo", "transcripts_38.tsv"
)
