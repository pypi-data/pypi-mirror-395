"""
Entrypoint for CLI tool
"""

import json
import click
import os

@click.command()
@click.option("--string", "-s", help="Raw JSON string")
@click.option("--file", "-f", type=click.File('r'), help="File containing JSON object")
@click.option(
    "--replace", 
    "-r", 
    is_flag=True, 
    default=True,  # <--- Change 1: Set default to True
    help="Overwrite the original input file with the beautified JSON. Default is True; use --no-replace to print to standard output." # <--- Change 2: Update help text
)
@click.argument("input", required=False)

def main(string, file, replace, input):
    ''' Beautify JSON object '''

    input_file_path = None # To store the path if the input is a file we might replace

    if string:
        data = string
    elif file:
        data = file.read()
        # The file option has type=click.File('r'), so 'file' is a file object.
        # We can get the name (path) from its 'name' attribute.
        input_file_path = file.name
    elif input:
        try:
            # Check if 'input' is a file path
            if os.path.exists(input) and os.path.isfile(input):
                with open(input, 'r') as f:
                    data = f.read()
                input_file_path = input
            # Otherwise, treat 'input' as a raw JSON string
            else:
                data = input
        except Exception:
            # Fallback in case of other file-related issues, treat as string
            data = input
    else:
        print("error")
        raise click.UsageError("Error: please provide a JSON string or file")


    try:
        # 1. Parse the JSON data
        parsed = json.loads(data)
        
        # 2. Beautify the JSON
        beautified_json = json.dumps(parsed, indent=4)
        
        # 3. Handle the output based on the 'replace' flag and input type
        # Logic remains the same: overwrite only if 'replace' is True (now default) AND we have a file path.
        if replace and input_file_path: 
            # Overwrite the original file
            with open(input_file_path, 'w') as f:
                f.write(beautified_json)
            # Optionally notify the user
            click.echo(f"Successfully beautified and overwrote file: {input_file_path}", err=True)
        else:
            # Print to standard output
            click.echo(beautified_json)

    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")
    except Exception as e:
        # Catch any other potential errors (like writing to file)
        raise click.ClickException(f"An error occurred: {e}")


if __name__ == "__main__":
    main()