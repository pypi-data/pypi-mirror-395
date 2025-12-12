#!/usr/bin/env python3
"""
Notebook Manager - Handle Jupyter notebook operations

This module provides utilities to:
- Load and parse .ipynb files
- Extract cells and metadata
- Add/modify/delete cells
- Save notebooks back to disk
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class CellType(Enum):
    """Jupyter notebook cell types"""
    CODE = "code"
    MARKDOWN = "markdown"
    RAW = "raw"


@dataclass
class NotebookCell:
    """Represents a single notebook cell"""
    cell_type: CellType
    source: str
    metadata: Dict[str, Any]
    execution_count: Optional[int] = None
    outputs: List[Dict[str, Any]] = None
    cell_id: Optional[str] = None

    def __post_init__(self):
        if self.outputs is None:
            self.outputs = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert cell to notebook JSON format"""
        cell_dict = {
            "cell_type": self.cell_type.value,
            "metadata": self.metadata,
            "source": self.source.split('\n') if isinstance(self.source, str) else self.source,
        }

        if self.cell_id:
            cell_dict["id"] = self.cell_id

        if self.cell_type == CellType.CODE:
            cell_dict["execution_count"] = self.execution_count
            cell_dict["outputs"] = self.outputs

        return cell_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NotebookCell':
        """Create cell from notebook JSON format"""
        source = data.get("source", [])
        if isinstance(source, list):
            source = '\n'.join(source)

        return cls(
            cell_type=CellType(data.get("cell_type", "code")),
            source=source,
            metadata=data.get("metadata", {}),
            execution_count=data.get("execution_count"),
            outputs=data.get("outputs", []),
            cell_id=data.get("id")
        )


class NotebookManager:
    """Manages Jupyter notebook operations"""

    def __init__(self, notebook_path: Optional[str] = None):
        self.notebook_path = notebook_path
        self.cells: List[NotebookCell] = []
        self.metadata: Dict[str, Any] = {}
        self.nbformat: int = 4
        self.nbformat_minor: int = 5

        if notebook_path and os.path.exists(notebook_path):
            self.load(notebook_path)

    def load(self, notebook_path: str) -> None:
        """Load notebook from file"""
        self.notebook_path = notebook_path

        with open(notebook_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.metadata = data.get("metadata", {})
        self.nbformat = data.get("nbformat", 4)
        self.nbformat_minor = data.get("nbformat_minor", 5)

        self.cells = [
            NotebookCell.from_dict(cell_data)
            for cell_data in data.get("cells", [])
        ]

    def save(self, notebook_path: Optional[str] = None) -> None:
        """Save notebook to file"""
        path = notebook_path or self.notebook_path
        if not path:
            raise ValueError("No notebook path specified")

        notebook_data = {
            "cells": [cell.to_dict() for cell in self.cells],
            "metadata": self.metadata,
            "nbformat": self.nbformat,
            "nbformat_minor": self.nbformat_minor
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=2, ensure_ascii=False)

    def create_new(self, title: str = "New Notebook") -> None:
        """Create a new empty notebook"""
        self.cells = []
        self.metadata = {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            },
            "title": title
        }
        self.nbformat = 4
        self.nbformat_minor = 5

    def add_cell(
        self,
        cell_type: CellType,
        source: str,
        position: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Add a new cell to the notebook"""
        cell = NotebookCell(
            cell_type=cell_type,
            source=source,
            metadata=metadata or {}
        )

        if position is None:
            self.cells.append(cell)
            return len(self.cells) - 1
        else:
            self.cells.insert(position, cell)
            return position

    def delete_cell(self, index: int) -> None:
        """Delete a cell by index"""
        if 0 <= index < len(self.cells):
            del self.cells[index]

    def update_cell(self, index: int, source: str) -> None:
        """Update cell content by index"""
        if 0 <= index < len(self.cells):
            self.cells[index].source = source

    def get_cell(self, index: int) -> Optional[NotebookCell]:
        """Get a cell by index"""
        if 0 <= index < len(self.cells):
            return self.cells[index]
        return None

    def get_structure(self) -> str:
        """Get a text representation of notebook structure"""
        structure = []
        structure.append(f"Notebook: {self.notebook_path or 'Untitled'}")
        structure.append(f"Total cells: {len(self.cells)}")
        structure.append("\nCells:")

        for i, cell in enumerate(self.cells):
            preview = cell.source[:50].replace('\n', ' ')
            if len(cell.source) > 50:
                preview += "..."
            structure.append(f"  [{i}] {cell.cell_type.value}: {preview}")

        return '\n'.join(structure)

    def get_content_summary(self) -> str:
        """Get a detailed summary of notebook content"""
        summary = []
        summary.append(f"=== Notebook: {self.notebook_path or 'Untitled'} ===\n")

        for i, cell in enumerate(self.cells):
            summary.append(f"Cell {i} ({cell.cell_type.value}):")
            summary.append(f"{cell.source}\n")
            summary.append("-" * 50)

        return '\n'.join(summary)

    def find_empty_cells(self) -> List[int]:
        """Find indices of empty cells"""
        return [i for i, cell in enumerate(self.cells) if not cell.source.strip()]

    def find_cells_by_pattern(self, pattern: str) -> List[int]:
        """Find cell indices containing a specific pattern"""
        return [
            i for i, cell in enumerate(self.cells)
            if pattern.lower() in cell.source.lower()
        ]

    def count_by_type(self) -> Dict[str, int]:
        """Count cells by type"""
        counts = {ct.value: 0 for ct in CellType}
        for cell in self.cells:
            counts[cell.cell_type.value] += 1
        return counts
