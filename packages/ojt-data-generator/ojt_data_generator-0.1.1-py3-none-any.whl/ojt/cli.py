import pandas as pd
from ojt import TEMPLATE_NAMES, TEMPLATE_MENU, generate_data

def main():
    # CLI
    print("Select a template:")
    for number, name in TEMPLATE_NAMES.items():
        print(f"{number}. {name}")

    choice = input("Enter template number: ").strip()
    if not choice.isdigit() or int(choice) not in TEMPLATE_MENU:
        print("Invalid choice!")
        exit()
    choice = int(choice)

    n_rows = input("Number of rows (default 1): ").strip()
    n_rows = int(n_rows) if n_rows else 1

    seed_input = input("Seed (optional): ").strip()
    seed = int(seed_input) if seed_input else None

    # Generate data
    data = generate_data(choice, n_rows, seed)

    # Print as pandas DataFrame
    df = pd.DataFrame(data)
    print(df)

    # Save to CSV
    save_csv = input("Save data to CSV? (y/n): ").strip().lower()
    if save_csv == "y":
        filename = input("Enter CSV file name (default: output.csv): ").strip()
        filename = filename if filename else "output.csv"
        if not filename.endswith('.csv'):
            filename = f"{filename}.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
