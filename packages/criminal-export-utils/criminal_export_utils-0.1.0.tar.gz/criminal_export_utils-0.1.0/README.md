# Criminal Export Utils

A utility library for exporting data to Excel and CSV files in PySide6 applications.

## Installation

pip install criminal-export-utils

## Usage

from criminal_export_utils import export_data_to_file

data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
export_data_to_file(data, parent_widget, "output_filename")

## Features

- Export data to Excel (.xlsx) format
- Export data to CSV format
- File dialog integration with PySide6
