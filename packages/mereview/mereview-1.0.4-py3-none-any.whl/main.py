#!/usr/bin/env python3
"""
mereview - A CLI tool for reviewing coding assignments and notebooks
"""

import os
import sys
import json
import zipfile
import tempfile
import shutil
import difflib
from pathlib import Path
from typing import Optional, Dict, Any
import click
import requests
import nbformat
from nbconvert import PythonExporter

try:
    import google.generativeai as genai

    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None


class Colors:
    """ANSI color codes for terminal output"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_step(step_num: int, message: str):
    """Print a formatted step message"""
    click.echo(f"\n{Colors.OKBLUE}{Colors.BOLD}Step {step_num}: {message}{Colors.ENDC}")


def print_success(message: str):
    """Print a success message"""
    click.echo(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_warning(message: str):
    """Print a warning message"""
    click.echo(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print an error message"""
    click.echo(f"{Colors.FAIL}✗ {message}{Colors.ENDC}", err=True)


def check_ai_content_gptzero(content: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Check if content is AI-generated using GPTZero API

    Args:
        content: Text content to check
        api_key: GPTZero API key

    Returns:
        Dictionary with detection results or None if failed
    """
    try:
        url = "https://api.gptzero.me/v2/predict/text"
        headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
        payload = {"document": content}

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        return {
            "completely_generated_prob": result.get("documents", [{}])[0].get(
                "completely_generated_prob", 0
            ),
            "average_generated_prob": result.get("documents", [{}])[0].get(
                "average_generated_prob", 0
            ),
            "is_ai_generated": result.get("documents", [{}])[0].get(
                "completely_generated_prob", 0
            )
            > 0.5,
            "raw_result": result,
        }
    except requests.exceptions.RequestException as e:
        print_error(f"GPTZero API request failed: {e}")
        return None
    except Exception as e:
        print_error(f"Error checking AI content: {e}")
        return None


def find_zip_file(directory: Path) -> Optional[Path]:
    """Find a zip file in the given directory"""
    zip_files = list(directory.glob("*.zip"))
    if not zip_files:
        return None
    if len(zip_files) > 1:
        print_warning(f"Multiple zip files found, using: {zip_files[0].name}")
    return zip_files[0]


def extract_zip_file(zip_path: Path, extract_to: Path) -> Optional[Path]:
    """
    Extract zip file and return the TASK_ folder path

    Args:
        zip_path: Path to zip file
        extract_to: Directory to extract to

    Returns:
        Path to TASK_ folder or None if not found
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        # Find TASK_ folder
        task_folders = [
            d for d in extract_to.iterdir() if d.is_dir() and d.name.startswith("TASK_")
        ]
        if not task_folders:
            print_error("No folder starting with 'TASK_' found in zip file")
            return None

        if len(task_folders) > 1:
            print_warning(
                f"Multiple TASK_ folders found, using: {task_folders[0].name}"
            )

        return task_folders[0]
    except zipfile.BadZipFile:
        print_error(f"Invalid zip file: {zip_path}")
        return None
    except Exception as e:
        print_error(f"Error extracting zip file: {e}")
        return None


def convert_notebook_to_python(notebook_path: Path) -> Optional[str]:
    """
    Convert Jupyter notebook to Python code

    Args:
        notebook_path: Path to .ipynb file

    Returns:
        Python code as string or None if failed
    """
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        exporter = PythonExporter()
        python_code, _ = exporter.from_notebook_node(notebook)

        return python_code
    except Exception as e:
        print_error(f"Error converting notebook {notebook_path.name}: {e}")
        return None


def remove_docstrings(code: str) -> str:
    """
    Remove docstrings from Python code

    Args:
        code: Python source code

    Returns:
        Code with docstrings removed
    """
    # Remove triple-quoted strings (docstrings)
    lines = code.split("\n")
    result_lines = []
    in_docstring = False
    docstring_char = None

    for line in lines:
        stripped = line.strip()

        # Check for docstring start/end
        if not in_docstring:
            if stripped.startswith('"""') or stripped.startswith("'''"):
                docstring_char = stripped[:3]
                if stripped.endswith(docstring_char) and len(stripped) > 6:
                    # Single-line docstring, skip it
                    continue
                else:
                    # Multi-line docstring starts
                    in_docstring = True
                    continue
            result_lines.append(line)
        else:
            if docstring_char in line:
                # Docstring ends
                in_docstring = False
                docstring_char = None
            continue

    return "\n".join(result_lines)


def calculate_diff_stats(old_code: str, new_code: str) -> Dict[str, int]:
    """
    Calculate statistics about differences between two code strings

    Args:
        old_code: Original code
        new_code: Modified code

    Returns:
        Dictionary with diff statistics
    """
    old_lines = old_code.splitlines()
    new_lines = new_code.splitlines()

    diff = difflib.unified_diff(old_lines, new_lines, lineterm="")

    additions = 0
    deletions = 0

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            deletions += 1

    return {
        "additions": additions,
        "deletions": deletions,
        "total_changes": additions + deletions,
        "old_lines": len(old_lines),
        "new_lines": len(new_lines),
    }


def generate_html_diff(
    old_code: str,
    new_code: str,
    output_path: Path,
    old_label: str = "Initial",
    new_label: str = "Final",
):
    """
    Generate an HTML diff file

    Args:
        old_code: Original code
        new_code: Modified code
        output_path: Path to save HTML file
        old_label: Label for old code
        new_label: Label for new code
    """
    old_lines = old_code.splitlines()
    new_lines = new_code.splitlines()

    diff_html = difflib.HtmlDiff(wrapcolumn=80)
    html_content = diff_html.make_file(
        old_lines,
        new_lines,
        fromdesc=f"{old_label} Notebook",
        todesc=f"{new_label} Notebook",
        context=True,
        numlines=3,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print_success(f"HTML diff saved to: {output_path}")


def check_test_variables_with_gemini(
    test_code: str, plans_content: str, initial_notebook_code: str, api_key: str
) -> Optional[str]:
    """
    Use Gemini API to check for variables asserted in tests but not in plans or initial notebook

    Args:
        test_code: Content of test_notebook.py
        plans_content: Content of plans.txt
        initial_notebook_code: Python code from initial_notebook.ipynb
        api_key: Gemini API key

    Returns:
        Response from Gemini or None if failed
    """
    if not GENAI_AVAILABLE:
        print_error("google-generativeai package is not installed")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")

        prompt = f"""You are a code analysis assistant. Analyze the following test file, plans document, and initial notebook code.

Your task:
1. Identify all variables, functions, and class definitions that are being asserted for existence in the test file (e.g., checking if they exist, calling them, accessing their properties).
2. Check if each of these identifiers is mentioned in either the requirements.md or the initial_notebook.py code.
3. For each identifier that is asserted in the test but NOT found in either requirements.md or initial_notebook.py, output ONE line in this exact format:
   FLAGGED: <identifier_name> | Asserted at: test_notebook.py line <line_number> | Reason: Not found in requirements.md or initial_notebook.py

If no issues are found, respond with: "No variables flagged."

TEST FILE (test_notebook.py):
```python
{test_code}
```

PLANS DOCUMENT (requirements.md):
```
{plans_content}
```

INITIAL NOTEBOOK CODE (initial_notebook.py):
```python
{initial_notebook_code}
```

Analyze the code and provide your response:"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print_error(f"Error calling Gemini API: {e}")
        return None


@click.command()
@click.option(
    "--dir",
    "-d",
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
    help="Directory containing plans.txt and zip file (default: current directory)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="review_results",
    help="Output directory for results (default: review_results)",
)
def main(directory: str, output: str):
    """
    mereview - Review coding assignments and notebooks

    Requires requirements.md and a zip file in the specified directory.
    Optional environment variables: GPTZERO_API_KEY, GEMINI_API_KEY
    """
    click.echo(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}")
    click.echo("  mereview - Code Review Tool")
    click.echo(f"{'=' * 60}{Colors.ENDC}\n")

    dir_path = Path(directory).resolve()
    output_path = Path(output).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    results = {
        "ai_detection": None,
        "diff_with_docstrings": None,
        "diff_without_docstrings": None,
        "gemini_analysis": None,
    }

    # Check for required files
    plans_file = dir_path / "requirements.md"
    if not plans_file.exists():
        print_error(f"requirements.md not found in {dir_path}")
        sys.exit(1)

    zip_file = find_zip_file(dir_path)
    if not zip_file:
        print_error(f"No zip file found in {dir_path}")
        sys.exit(1)

    print_success(f"Found requirements.md and {zip_file.name}")

    # STEP 1: AI Detection (Optional)
    print_step(1, "Checking if requirements.md is AI-generated (GPTZero)")
    gptzero_api_key = os.getenv("GPTZERO_API_KEY", "").strip()

    if not gptzero_api_key:
        print_warning("GPTZERO_API_KEY not found in environment, skipping AI detection")
    else:
        with open(plans_file, "r", encoding="utf-8") as f:
            plans_content = f.read()

        ai_result = check_ai_content_gptzero(plans_content, gptzero_api_key)
        if ai_result:
            results["ai_detection"] = ai_result
            is_ai = ai_result.get("is_ai_generated", False)
            prob = ai_result.get("completely_generated_prob", 0) * 100

            if is_ai:
                print_warning(
                    f"Content appears to be AI-generated (confidence: {prob:.1f}%)"
                )
            else:
                print_success(
                    f"Content appears to be human-written (AI probability: {prob:.1f}%)"
                )

    # STEP 2: Extract zip file
    print_step(2, f"Extracting {zip_file.name}")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        task_folder = extract_zip_file(zip_file, temp_path)

        if not task_folder:
            sys.exit(1)

        print_success(f"Extracted to: {task_folder.name}")

        # Check for required files
        initial_notebook = task_folder / "initial_notebook.ipynb"
        final_notebook = task_folder / "final_notebook.ipynb"
        test_file = task_folder / "test_notebook.py"

        missing_files = []
        if not initial_notebook.exists():
            missing_files.append("initial_notebook.ipynb")
        if not final_notebook.exists():
            missing_files.append("final_notebook.ipynb")
        if not test_file.exists():
            missing_files.append("test_notebook.py")

        if missing_files:
            print_error(f"Missing required files: {', '.join(missing_files)}")
            sys.exit(1)

        # Copy entire TASK_ folder contents to output
        print_step(3, "Copying all extracted files to output directory")

        # Copy all files and folders from TASK_ folder
        for item in task_folder.iterdir():
            src = task_folder / item.name
            dst = output_path / item.name

            if src.is_dir():
                # Copy directory recursively
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                # Copy file
                shutil.copy2(src, dst)

        print_success(f"All files from {task_folder.name} copied to output directory")

        # STEP 4: Convert notebooks to Python
        print_step(4, "Converting Jupyter notebooks to Python")

        initial_py = convert_notebook_to_python(initial_notebook)
        final_py = convert_notebook_to_python(final_notebook)

        if not initial_py or not final_py:
            print_error("Failed to convert notebooks")
            sys.exit(1)

        # Save converted files
        initial_py_path = output_path / "initial_notebook.py"
        final_py_path = output_path / "final_notebook.py"

        with open(initial_py_path, "w", encoding="utf-8") as f:
            f.write(initial_py)
        with open(final_py_path, "w", encoding="utf-8") as f:
            f.write(final_py)

        print_success(f"Converted notebooks saved to {output_path}")

        # Calculate diff with docstrings
        print_step(5, "Calculating diff statistics (with docstrings)")
        diff_stats_with = calculate_diff_stats(initial_py, final_py)
        results["diff_with_docstrings"] = diff_stats_with

        click.echo(f"  Lines added: {diff_stats_with['additions']}")
        click.echo(f"  Lines deleted: {diff_stats_with['deletions']}")
        click.echo(f"  Total changes: {diff_stats_with['total_changes']}")

        # STEP 5: Remove docstrings and diff
        print_step(6, "Calculating diff statistics (without docstrings)")

        initial_py_no_doc = remove_docstrings(initial_py)
        final_py_no_doc = remove_docstrings(final_py)

        diff_stats_without = calculate_diff_stats(initial_py_no_doc, final_py_no_doc)
        results["diff_without_docstrings"] = diff_stats_without

        click.echo(f"  Lines added: {diff_stats_without['additions']}")
        click.echo(f"  Lines deleted: {diff_stats_without['deletions']}")
        click.echo(f"  Total changes: {diff_stats_without['total_changes']}")

        # STEP 6: Generate HTML diff
        print_step(7, "Generating HTML diff report")
        html_diff_path = output_path / "diff_report.html"
        generate_html_diff(initial_py_no_doc, final_py_no_doc, html_diff_path)

        # STEP 7: Gemini analysis
        print_step(8, "Analyzing test file with Gemini AI")
        gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()

        if not gemini_api_key:
            print_warning(
                "GEMINI_API_KEY not found in environment, skipping test analysis"
            )
        else:
            with open(test_file, "r", encoding="utf-8") as f:
                test_content = f.read()
            with open(plans_file, "r", encoding="utf-8") as f:
                plans_content = f.read()

            gemini_result = check_test_variables_with_gemini(
                test_content, plans_content, initial_py, gemini_api_key
            )

            if gemini_result:
                results["gemini_analysis"] = gemini_result
                click.echo(f"\n{Colors.OKCYAN}Gemini Analysis Results:{Colors.ENDC}")
                click.echo(gemini_result)

                # Save Gemini results
                gemini_output = output_path / "gemini_analysis.txt"
                with open(gemini_output, "w", encoding="utf-8") as f:
                    f.write(gemini_result)
                print_success(f"Gemini analysis saved to: {gemini_output}")

    # Save final results summary
    print_step(9, "Saving results summary")
    results_json = output_path / "results_summary.json"
    with open(results_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    print_success(f"Results summary saved to: {results_json}")

    click.echo(f"\n{Colors.BOLD}{Colors.OKGREEN}{'=' * 60}")
    click.echo("  Review Complete!")
    click.echo(f"  All results saved to: {output_path}")
    click.echo(f"{'=' * 60}{Colors.ENDC}\n")


if __name__ == "__main__":
    main()
