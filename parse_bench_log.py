import csv
import sys
from collections import defaultdict
from statistics import median, mean, stdev

def process(input_file, output_file):
    data = defaultdict(list)

    # Read input CSV
    with open(input_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            name = row[0]
            value = float(row[1])  # first numeric column
            data[name].append(value)

    # Write output CSV
    with open(output_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "median", "percent_deviation"])

        for name, values in data.items():
            med = median(values)
            avg = mean(values)
            dev = stdev(values) if len(values) > 1 else 0.0
            percent_dev = (dev / avg * 100) if avg != 0 else 0.0

            writer.writerow([name, f"{med:.4f}", f"{percent_dev:.2f}"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.csv output.csv")
        sys.exit(1)

    process(sys.argv[1], sys.argv[2])