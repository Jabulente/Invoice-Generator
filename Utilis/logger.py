from datetime import datetime

def log_success(filename: str) -> None:
    """Log successful invoice generation."""
    total_length = 100
    save_message = "Invoice Generated Successfully  ✔✔✔✔"
    remaining_length = total_length - len(filename) - len(save_message) - 3
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time}: {filename} : {'-' * remaining_length} {save_message}")
    