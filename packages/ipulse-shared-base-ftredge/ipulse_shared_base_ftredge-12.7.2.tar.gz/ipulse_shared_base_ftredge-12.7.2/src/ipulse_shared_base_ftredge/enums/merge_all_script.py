#!/usr/bin/env python3
import os
import sys

# Adjust this list or auto-discover *.py in some folder
ENUM_FILES = [
    "enums_actions.py",
    "enums_alerts.py",
    "enums_data_eng.py",
    "enums_dimensions.py",
    "enums_fincore.py",
    "enums_iam.py",
    "enums_logging.py",
    "enums_pulse.py",
    "enums_resources.py",
    "enums_status.py",
]

OUTPUT_FILE = "enums_all.py"


def combine_enum_files(enum_files, output_file):
    """
    Combine multiple Python enum files into a single file.
    - Collects all unique import statements at the top.
    - Appends the remaining code (enums, etc.) in sequence.
    """
    import_lines = set()
    other_lines = []

    for file_path in enum_files:
        if not os.path.isfile(file_path):
            print(f"Warning: {file_path} not found, skipping.")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                # Trim leading/trailing whitespace just for checking
                stripped = line.strip()
                # Check if it's an import line
                if stripped.startswith("import ") or stripped.startswith("from "):
                    import_lines.add(line.rstrip("\n"))
                else:
                    other_lines.append(line.rstrip("\n"))

    # Write everything out
    with open(output_file, "w", encoding="utf-8") as out:
        # Write imports first
        for imp_line in sorted(import_lines):
            out.write(f"{imp_line}\n")
        out.write("\n")

        # Then write the rest of the code
        for code_line in other_lines:
            out.write(f"{code_line}\n")

    print(f"Combined {len(enum_files)} files into {output_file}")


def main():
    # If you want to discover *.py files in a 'enums/' folder, you could do:
    # directory = 'enums'  # or wherever your files live
    # enum_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.py')]
    # combine_enum_files(enum_files, OUTPUT_FILE)

    # For this example, we'll just use the hardcoded ENUM_FILES list
    combine_enum_files(ENUM_FILES, OUTPUT_FILE)


if __name__ == "__main__":
    main()