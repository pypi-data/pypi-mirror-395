# mereview

A CLI tool for reviewing coding assignments and Jupyter notebooks with AI-powered analysis.

## Features

- **AI Detection**: Checks if requirements.md is AI-generated using GPTZero API (optional)
- **Notebook Analysis**: Converts Jupyter notebooks to Python and performs diff analysis
- **Diff Reports**: Generates both statistical and HTML diff reports
- **Test Validation**: Uses Gemini AI to validate test assertions against plans and initial code

## Installation

### From PyPI (recommended):

```bash
pip install mereview
```

## Usage

```bash
mereview [OPTIONS]
```

### Options

- `--dir, -d`: Directory containing requirements.md and zip file (default: current directory)
- `--output, -o`: Output directory for results (default: review_results)
- `--help`: Show help message

### Example

```bash
# Run in current directory
mereview

# Specify directory and output location
mereview --dir ./submissions --output ./reviews
```

## Required Files

The tool expects the following files in the specified directory:

1. **requirements.md** - The project requirements document
2. **[name].zip** - A zip file containing:
   - A folder starting with `TASK_`
   - Inside the folder:
     - `initial_notebook.ipynb`
     - `final_notebook.ipynb`
     - `test_notebook.py`

## Environment Variables

Set these environment variables before running the tool (optional):

```bash
export GPTZERO_API_KEY="your_gptzero_api_key"
export GEMINI_API_KEY="your_gemini_api_key"
```

- `GPTZERO_API_KEY` (optional): API key for GPTZero AI detection service - Get from https://gptzero.me/
- `GEMINI_API_KEY` (optional): API key for Google Gemini AI analysis - Get from https://ai.google.dev/

If these keys are not provided, the respective steps will be skipped with warnings.

## Output

The tool generates the following files in the output directory:

- `initial_notebook.ipynb` - Copy of original initial notebook
- `final_notebook.ipynb` - Copy of original final notebook
- `test_notebook.py` - Copy of original test file
- `initial_notebook.py` - Converted initial notebook (Python)
- `final_notebook.py` - Converted final notebook (Python)
- `diff_report.html` - HTML visualization of code differences
- `gemini_analysis.txt` - Gemini AI analysis of test assertions
- `results_summary.json` - Complete results summary in JSON format

## How It Works

1. **Step 1**: Checks if requirements.md is AI-generated (optional with GPTZero)
2. **Step 2**: Extracts the zip file and locates the TASK_ folder
3. **Step 3**: Copies original notebooks and test file to output directory
4. **Step 4**: Converts Jupyter notebooks to Python files
5. **Step 5**: Calculates diff statistics with docstrings included
6. **Step 6**: Removes docstrings and recalculates diff statistics
7. **Step 7**: Generates an HTML diff report
8. **Step 8**: Analyzes test file with Gemini AI to check for undocumented assertions
9. **Step 9**: Saves all results to the output directory

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
