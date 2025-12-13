import sys
import os

def help_message():
    return """Usage: summarizer <input-file> [--out output-file]

Summaries a text file by counting:
- Number of lines
- Number of words
- Number of characters

Options:
    -h, --help      Show this help message
    --out <file>    Write output to a file instead of printing
"""

def summarize_file(path):
    """Return a dictionary summary of the file contents."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return {
        "lines": text.count("\n") + 1 if text else 0,
        "words": len(text.split()),
        "characters": len(text)
    }

def main():
    args = sys.argv[1:]

    # Handle help
    if not args or args[0] in ("-h", "--help"):
        print(help_message())
        return

    input_path = args[0]

    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    # Check for out
    output_path = None
    if "--out" in args:
        idx = args.index("--out")
        if idx + 1 >= len(args):
            print("Error: Missing output file after --out")
            return
        output_path = args[idx + 1]

    summary = summarize_file(input_path)

    output = (
        f"Summary of {input_path}:\n"
        f"Lines: {summary['lines']}\n"
        f"Words: {summary['words']}\n"
        f"Characters: {summary['characters']}\n"
    )

    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Summary written to {output_path}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        print(output)
