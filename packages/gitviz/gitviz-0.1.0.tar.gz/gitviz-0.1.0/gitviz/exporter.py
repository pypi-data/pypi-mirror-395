import pandas as pd
import json

def export_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """Export DataFrame to CSV file."""
    df.to_csv(filepath, index=False)

def export_to_json(df: pd.DataFrame, filepath: str) -> None:
    """Export DataFrame to JSON file."""
    df.to_json(filepath, orient="records", lines=True, date_format="iso")

def save_dashborad_config(config: dict, filepath: str) -> None:
    """Save dashboard configuration to a JSON file."""
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def load_dashboard_config(filepath: str) -> dict:
    """Load dashboard configuration from a JSON file."""
    with open(filepath, "r", encoding='utf-8') as f:
        config = json.load(f)
    return config