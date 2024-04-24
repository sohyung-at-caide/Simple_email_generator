import argparse
import csv
from baseline_email_generator_huggingface import get_config, submit_prompt
import datetime
import time

def read_csv_file(csv_path: str):
    """
    Read a CSV file with the given header structure.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        list: A list of dicts where each dict represents a row in the CSV file.
    """
    data = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def write_csv_output(csv_data: list, output_file: str):
    """
    Write the generated text back to a new CSV file.

    Parameters:
        csv_data (list): A list of dictionaries representing CSV rows with 'output' column filled.
        output_file (str): Path to the output CSV file.
    """
    with open(f"results/{output_file}", 'w', newline='') as csvfile:
        fieldnames = csv_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)


def main(csv_path, config_name, output_file):
    # Setting configuration for inference
    config = get_config(config_name)
    # Read the csv data
    csv_data = read_csv_file(f'input/{csv_path}')

    for turn in csv_data:
        start_time = time.time()

        # Generate data using the provided prompts and configuration
        generated_text = submit_prompt(turn['System'], turn['User'], config, True)

        # Calculate execution time
        execution_time = time.time() - start_time

        # Update the 'output', 'execution time', and 'tokens used' columns
        turn['output'] = generated_text
        turn['execution time'] = execution_time

    # Write the updated data to a new CSV file
    write_csv_output(csv_data, output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate data from CSV prompts and write output to CSV.')
    parser.add_argument('--csv_path', type=str, help='Path to the CSV file containing prompts.',
                        default='Prompt_benchmarking_zero-shot.csv')
    parser.add_argument('--config_name', type=str, help='Name of the YAML file containing inference config',
                        default="openchat-3-5-extended")
    parser.add_argument('--output_file', type=str, help='Path to the output CSV file.',
                        default=f'results-{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}.csv')

    args = parser.parse_args()

    main(args.csv_path, args.config_name, args.output_file)

