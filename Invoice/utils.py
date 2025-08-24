from datetime import datetime
import pandas as pd
import os

def save_to_csv(df: pd.DataFrame, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")

def load_dataset(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)



# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'   # Reset color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_success(filename: str) -> None:
    total_length = 100
    save_message = f"{Colors.OKGREEN}{Colors.BOLD} Invoice Generated Successfully ✔{Colors.ENDC}"
    remaining_length = total_length - len(filename) - len(" : ") - len(" : ") - len("Invoice Generated Successfully")  
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"{Colors.OKCYAN}{current_time}{Colors.ENDC} : "
        f"{Colors.OKBLUE}{filename}{Colors.ENDC} "
        f"{'-' * remaining_length} "
        f"{save_message}"
    )
