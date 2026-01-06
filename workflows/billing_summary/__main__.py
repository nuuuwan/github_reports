import os
import webbrowser
from pathlib import Path

import pandas as pd


def get_csv_file():
    """Find and return the CSV file from the desktop directory."""
    dir_desktop = os.environ.get("DIR_DESKTOP")
    if not dir_desktop:
        raise EnvironmentError(
            "Environment variable 'DIR_DESKTOP' is not set."
        )

    desktop_path = Path(dir_desktop)
    csv_files = list(desktop_path.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {dir_desktop}")

    if len(csv_files) > 1:
        raise ValueError(f"Multiple CSV files found: {csv_files}")

    return csv_files[0]


def aggregate_billing_data(csv_file):
    """Read CSV and return aggregated billing data by repository."""
    print(f"Reading billing data from: {csv_file}")
    df = pd.read_csv(csv_file)

    aggregated = (
        df.groupby("repository").agg({"gross_amount": "sum"}).round(2)
    )

    aggregated = aggregated.sort_values("gross_amount", ascending=False)

    total = aggregated["gross_amount"].sum()
    aggregated["% of Total"] = (
        aggregated["gross_amount"] / total * 100
    ).round(2)

    return aggregated


def open_repositories(repositories, github_username):
    """Open the top repositories in the web browser."""
    for repo in repositories:
        url = f"https://github.com/{github_username}/{repo}"
        print(f"Opening: {url}")
        webbrowser.open(url)


def main():
    csv_file = get_csv_file()
    aggregated = aggregate_billing_data(csv_file)

    print("\nBilling Summary by Repository:")
    print(aggregated.to_string())

    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        raise EnvironmentError(
            "Environment variable 'GITHUB_USERNAME' is not set."
        )

    top_10 = aggregated.head(10).index.tolist()
    open_repositories(top_10, github_username)


if __name__ == "__main__":
    main()
