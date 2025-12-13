import argparse
import re
import importlib.util
import os
import sys
import json

# --- Configuration ---
MAX_RECURSION_DEPTH = 10
NODES_DIR = "nodes"
OUTPUT_DIR = "output"
MAIN_FILE = "main.md"
OUTPUT_FILE = "output.md"


# --- Command Functions ---


def run_builder():
    """Reads main.md, processes tags recursively, and writes to output."""
    if not os.path.exists(MAIN_FILE):
        print(f"Error: '{MAIN_FILE}' not found. Run 'builder make' to start.")
        return

    print(f"Reading {MAIN_FILE}...")
    with open(MAIN_FILE, "r", encoding="utf-8") as f:
        main_content = f.read()

    print("Building content...")
    try:
        final_content = process_content(main_content)
    except Exception as e:
        print(f"Critical Error: {e}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Success! Output saved to: {output_path}")


def scaffold_project():
    """Creates the default folder structure and example files."""
    # Create Directories
    os.makedirs(NODES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Created directories: /{NODES_DIR}, /{OUTPUT_DIR}")

    # Create main.md
    if not os.path.exists(MAIN_FILE):
        with open(MAIN_FILE, "w", encoding="utf-8") as f:
            f.write("# My Document\n\nWelcome to my automated document.\n\n{[header]}")
        print(f"Created file: {MAIN_FILE}")
    else:
        print(f"Skipped: {MAIN_FILE} (already exists)")

    # Create example node (Markdown)
    example_md = os.path.join(NODES_DIR, "header.md")
    if not os.path.exists(example_md):
        with open(example_md, "w", encoding="utf-8") as f:
            f.write(
                "## Header Section\nGenerated on: {{date}}\nAuthor: {{author}}\n\nThis is a dynamic section."
            )
        print(f"Created file: {example_md}")

    # Create example node (Python)
    example_py = os.path.join(NODES_DIR, "header.py")
    if not os.path.exists(example_py):
        with open(example_py, "w", encoding="utf-8") as f:
            code = (
                "import datetime\n\n"
                "def header():\n"
                "    return {\n"
                "        'date': str(datetime.date.today()),\n"
                "        'author': 'Radoslaw'\n"
                "    }"
            )
            f.write(code)
        print(f"Created file: {example_py}")

    print("\nSetup complete! Try running: builder run")


# --- Core Logic (Recursive) ---


def process_content(content, depth=0):
    if depth > MAX_RECURSION_DEPTH:
        return content + "\n\n[ERROR: Max recursion depth exceeded]\n"

    found_items = find_custom_patterns(content)

    if not found_items:
        return content

    # Używamy set(), aby nie przetwarzać tego samego tagu wielokrotnie, jeśli występuje kilka razy
    for item in set(found_items):
        try:
            # 1. Execute Python Script (if exists)
            script_path = os.path.join(NODES_DIR, f"{item}.py")
            parameters = {}

            if os.path.exists(script_path):
                script_result = execute_external_function(script_path, item)
                if isinstance(script_result, (dict, str)):
                    # Normalize result to dict if it's JSON string
                    if isinstance(script_result, str):
                        try:
                            parameters = json.loads(script_result)
                        except json.JSONDecodeError:
                            print(f"Warning: {item}.py returned invalid JSON string.")
                    else:
                        parameters = script_result

            # 2. Read Markdown Template
            md_path = os.path.join(NODES_DIR, f"{item}.md")
            node_content = ""

            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as sub_file:
                    node_content = sub_file.read()

                # Replace {{variables}}
                for key, value in parameters.items():
                    node_content = node_content.replace(f"{{{{{key}}}}}", str(value))

                # RECURSION: Process this node's content for nested tags
                node_content = process_content(node_content, depth + 1)
            else:
                print(f"Warning: Template {item}.md not found.")
                # Jeśli szablon nie istnieje, wstawiamy pusty string
                node_content = ""

            # 3. Replace tag in parent content
            # Używamy replace dla wszystkich wystąpień danego tagu
            content = content.replace(f"{{[{item}]}}", node_content)

        except Exception as e:
            print(f"Error processing node '{item}': {e}")
            # W razie błędu usuwamy tag z outputu
            content = content.replace(f"{{[{item}]}}", "")

    return content


# --- Helpers ---


def find_custom_patterns(input_string):
    pattern = r"\{\[(.*?)\]\}"
    return re.findall(pattern, input_string)


def execute_external_function(file_path, function_name, *args, **kwargs):
    if not os.path.exists(file_path):
        return {}  # Fail silently or handle logic elsewhere

    try:
        module_name = os.path.basename(file_path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return {}

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore

        if hasattr(module, function_name):
            target_func = getattr(module, function_name)
            return target_func(*args, **kwargs)
        else:
            print(f"Warning: Function '{function_name}' not found in {file_path}")
            return {}
    except Exception as e:
        print(f"Script Error ({file_path}): {e}")
        return {}


def main():
    # Initialize Argument Parser
    parser = argparse.ArgumentParser(description="Markdown Template Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: run
    parser_run = subparsers.add_parser(
        "run", help="Compile the main.md file into output.md"
    )

    # Command: make
    parser_make = subparsers.add_parser(
        "make", help="Create directory structure and sample files"
    )

    args = parser.parse_args()

    if args.command == "run":
        run_builder()
    elif args.command == "make":
        scaffold_project()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
