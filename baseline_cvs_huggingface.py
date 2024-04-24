import argparse
import csv

def read_csv_file(csv_path):
    """
    Read a CSV file with the given header structure.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    data = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def main():
    parser = argparse.ArgumentParser(description='Read CSV file with specific header structure.')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file to be read.')

    args = parser.parse_args()

    csv_data = read_csv_file(args.csv_path)
    print(csv_data)

if __name__ == '__main__':
    main()
