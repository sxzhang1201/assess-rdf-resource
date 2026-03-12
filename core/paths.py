"""Path utilities for output files."""

from pathlib import Path
from typing import Dict

from core.constants import OUTPUT_DIR, PICKLE_DIR


def get_output_paths(label: str) -> Dict[str, Path]:
    """Get all output file paths for a given resource label."""
    output_label_dir = OUTPUT_DIR / label
    return {
        "resolvable": output_label_dir / f"uri-resolvable-{label}.csv",
        "parsable": output_label_dir / f"uri-parsable-{label}.csv",
        "consistent": output_label_dir / f"uri-consistent-{label}.csv",
        "intermediate": output_label_dir / f"uri-intermediate-{label}.csv",
        "report": output_label_dir / f"report-{label}.ttl",
    }


def get_pickle_path(label: str) -> Path:
    """Get pickle file path for a resource graph."""
    return PICKLE_DIR / f"{label}_graph.pickle"
