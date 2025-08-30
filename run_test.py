import subprocess
import json
import os

def run_postman_collection(collection_file, environment_file, output_file):
    """
    Runs a Postman collection using Newman via the absolute path to npx.
    
    Args:
        collection_file (str): Path to the Postman collection.json file.
        environment_file (str): Path to the Postman environment.json file.
        output_file (str): Path to the output JSON file for the report.
    """
    try:
        # Using the absolute path to npx.cmd for maximum reliability.
        npx_command = 'C:/Users/DELL/AppData/Roaming/npm/npx.cmd'
        
        command = [
            npx_command, 'newman', 'run', collection_file,
            '--environment', environment_file,
            '--reporters', 'cli,json',
            '--reporter-json-export', output_file
        ]
        
        # Execute the command with utf-8 encoding and error handling.
        process = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print("Newman run successful!")
        print(process.stdout)
        
    except FileNotFoundError:
        print("Error: The 'npx' command was not found at the specified path.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Newman run failed with error code {e.returncode}")
        print("Standard Output:")
        print(e.stdout)
        print("Standard Error:")
        print(e.stderr)
        return False
    return True

def process_results(results_file):
    """
    Reads the Newman results JSON file and processes the test results.
    
    Args:
        results_file (str): Path to the Newman results JSON file.
    """
    if not os.path.exists(results_file):
        print(f"Results file not found: {results_file}")
        return

    with open(results_file, 'r') as f:
        data = json.load(f)

    # Example: Analyze test run data
    summary = data.get('run', {}).get('failures', [])
    stats = data.get('run', {}).get('stats', {}).get('tests', {})
    
    print("\n--- Test Summary ---")
    if summary:
        print(f"The following {stats['failed']} tests failed:")
        for failure in summary:
            print(f"- {failure['error']['test']}")
            print(f"  - Request: {failure['source']['name']}")
    else:
        print("All tests passed!")
        
    print(f"\nTotal tests run: {stats['total']}")
    print(f"Total tests failed: {stats['failed']}")

if __name__ == "__main__":
    # Define file paths
    collection_path = 'postman_collection.json'
    environment_path = 'postman_environment.json'
    results_path = 'newman_report.json'
    
    if not os.path.exists(collection_path) or not os.path.exists(environment_path):
        print("Error: Postman collection.json or environment.json not found in the project directory.")
    else:
        if run_postman_collection(collection_path, environment_path, results_path):
            process_results(results_path)
