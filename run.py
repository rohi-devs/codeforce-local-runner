#!/usr/bin/env python3

import subprocess
import difflib
import os
import sys

def compile_and_execute(source_file, input_file, output_file, expected_output_file):
    try:
        # Define the output executable name
        executable = "./target" if source_file.endswith((".cc", ".cpp")) else "program"

        # Step 1: Compile the code (for C++ and Java)
        if source_file.endswith((".cc", ".cpp")):
            compile_command = ["g++", "-o", executable, source_file]
        elif source_file.endswith(".java"):
            compile_command = ["javac", source_file]
            executable = "java"
        elif source_file.endswith(".py"):
            executable = "python3"
        else:
            raise ValueError("Unsupported language. Only C++, Java, and Python are supported.")

        # Compile if needed
        if source_file.endswith((".cc", ".cpp", ".java")):
            print("Compiling...")
            subprocess.run(compile_command, check=True)

        # Step 2: Execute the program with redirected stdin and stdout
        print("Executing...")
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            if source_file.endswith((".cc", ".cpp")):
                subprocess.run([executable], stdin=infile, stdout=outfile, check=True)
            elif source_file.endswith(".java"):
                class_name = os.path.splitext(os.path.basename(source_file))[0]
                subprocess.run(["java", class_name], stdin=infile, stdout=outfile, check=True)
            elif source_file.endswith(".py"):
                subprocess.run(["python3", source_file], stdin=infile, stdout=outfile, check=True)

        # Step 3: Compare the output with the expected output
        print("Comparing outputs...")
        with open(output_file, "r") as outfile, open(expected_output_file, "r") as expected_file:
            actual_output = outfile.readlines()
            expected_output = expected_file.readlines()

        # Use difflib to show differences
        diff = difflib.unified_diff(
            expected_output, actual_output, 
            fromfile="expected_output", tofile="actual_output", lineterm=""
        )
        diff_result = "\n".join(diff)

        if diff_result:
            print("Output differs from expected:")
            print(diff_result)
        else:
            print("Output matches the expected output!")

    except subprocess.CalledProcessError as e:
        print(f"Error during execution: {e}")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup compiled executable for C++ if it exists
        if os.path.exists(executable) and source_file.endswith((".cc", ".cpp")):
            os.remove(executable)


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5:
        print("Usage: python codeforces_runner.py <source_file> <input_file> <output_file> <expected_output_file>")
        sys.exit(1)

    # Get file paths from command-line arguments
    source_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    expected_output_file = sys.argv[4]

    # Check for missing files
    for file in [source_file, input_file, expected_output_file]:
        if not os.path.exists(file):
            print(f"Error: {file} does not exist.")
            sys.exit(1)

    # Run the program
    compile_and_execute(source_file, input_file, output_file, expected_output_file)
