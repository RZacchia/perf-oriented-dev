import glob
import os
import numpy as np
import matplotlib.pyplot as plt

def collect_data(profile_type, results_dir='ex03/results'):
    pattern = f"profile_{profile_type}_local_*.txt"
    files = glob.glob(os.path.join(results_dir, pattern))
    functions = {}
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
        start = False
        for line in lines:
            if 'cumulative' in line and '%' in line:
                start = True
                continue
            if start and line.strip():
                parts = line.split()
                if len(parts) >= 7:
                    try:
                        pct = float(parts[0])
                        name = parts[-1]
                        if name not in functions:
                            functions[name] = []
                        functions[name].append(pct)
                    except ValueError:
                        pass
    return functions

def main():
    for profile_type in ['a', 'b']:
        data = collect_data(profile_type)
        results = {}
        for func, pcts in data.items():
            if len(pcts) > 1:
                avg = np.mean(pcts)
                var = np.var(pcts)
            else:
                avg = pcts[0] if pcts else 0
                var = 0
            results[func] = (avg, var)

        # Sort by avg descending
        sorted_funcs = sorted(results.items(), key=lambda x: x[1][0], reverse=True)

        # Print results
        print(f"\nProfile {profile_type.upper()} Statistics:")
        print("Function\t\tAverage %\tVariance")
        for func, (avg, var) in sorted_funcs:
            print(f"{func}\t\t{avg:.2f}\t\t{var:.4f}")

        # Visualization for top 10
        if len(sorted_funcs) > 0:
            top_funcs = sorted_funcs[:10]
            funcs = [f[0] for f in top_funcs]
            avgs = [f[1][0] for f in top_funcs]
            stds = [np.sqrt(f[1][1]) for f in top_funcs]  # std dev for error bars

            plt.figure(figsize=(12, 6))
            plt.bar(funcs, avgs, yerr=stds, capsize=5, color='skyblue', edgecolor='black')
            plt.title(f'Average % Time for Profile {profile_type.upper()} (Top 10 Functions)', fontsize=16)
            plt.ylabel('% Time', fontsize=14)
            plt.xlabel('Functions', fontsize=14)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(f'profile_{profile_type}_stats.png', dpi=300)
            print(f"Visualization saved as profile_{profile_type}_stats.png")

if __name__ == "__main__":
    main()