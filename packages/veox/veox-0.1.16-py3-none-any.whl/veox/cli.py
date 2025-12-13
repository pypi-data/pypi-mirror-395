import argparse
import sys
import pandas as pd
from pathlib import Path
from typing import Optional

from .client import Veox
from .datasets import DatasetLoader

def main():
    parser = argparse.ArgumentParser(description="Veox: The Incredible ML Client for DOUG")
    parser.add_argument("--api", default="http://localhost:8090", help="DOUG API URL")
    parser.add_argument("--key", help="API Key")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # fit command
    fit_parser = subparsers.add_parser("fit", help="Run evolution on a dataset")
    fit_parser.add_argument("--csv", help="Path to CSV file")
    fit_parser.add_argument("--dataset", help="Built-in dataset name or DOUG dataset ID")
    fit_parser.add_argument("--target-column", help="Target column name (required for CSV)")
    fit_parser.add_argument("--task", default="binary", choices=["binary", "regression"], help="Task type")
    fit_parser.add_argument("--population", type=int, default=50, help="Population size")
    fit_parser.add_argument("--generations", type=int, default=10, help="Generations")
    fit_parser.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds")
    fit_parser.add_argument("--name", help="Job name")
    fit_parser.add_argument("--pull-code", action="store_true", help="Pull best pipeline code after completion")
    fit_parser.add_argument("--output", help="Output file for pulled code")

    # upload-data command
    upload_parser = subparsers.add_parser("upload-data", help="Upload a CSV dataset")
    upload_parser.add_argument("csv", help="Path to CSV file")
    upload_parser.add_argument("--target-column", required=True, help="Target column name")
    upload_parser.add_argument("--task", default="auto", help="Task type")
    upload_parser.add_argument("--name", help="Dataset name")

    # pull-code command
    pull_parser = subparsers.add_parser("pull-code", help="Pull pipeline code")
    pull_parser.add_argument("--job-id", help="Job ID")
    pull_parser.add_argument("--run-id", help="Run ID")
    pull_parser.add_argument("--output", "-o", help="Output file path")

    # list-datasets command
    list_parser = subparsers.add_parser("list-datasets", help="List built-in datasets")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        client = Veox(
            api_url=args.api,
            api_key=args.key,
            verbose=args.verbose,
            debug=args.debug
        )

        if args.command == "fit":
            if args.csv:
                df = pd.read_csv(args.csv)
                if not args.target_column:
                    print("❌ --target-column is required when using --csv")
                    sys.exit(1)
                
                client.fit(
                    data=df,
                    target_column=args.target_column,
                    task=args.task,
                    population=args.population,
                    generations=args.generations,
                    timeout=args.timeout,
                    name=args.name
                )
            elif args.dataset:
                # Check if it's a built-in dataset
                try:
                    loader = DatasetLoader()
                    X, y = loader.load_dataset(args.dataset)
                    print(f"📦 Loaded built-in dataset: {args.dataset}")
                    client.fit(
                        X=X,
                        y=y,
                        task=args.task,
                        population=args.population,
                        generations=args.generations,
                        timeout=args.timeout,
                        name=args.name
                    )
                except ValueError:
                    # Assume it's a DOUG dataset ID
                    client.fit(
                        dataset=args.dataset,
                        task=args.task,
                        population=args.population,
                        generations=args.generations,
                        timeout=args.timeout,
                        name=args.name
                    )
            else:
                print("❌ Must provide --csv or --dataset")
                sys.exit(1)

            if args.pull_code:
                code = client.pull_code(output_file=args.output)
                if not args.output:
                    print("\n📄 Best Pipeline Code:")
                    print("-" * 40)
                    print(code)
                    print("-" * 40)

        elif args.command == "upload-data":
            df = pd.read_csv(args.csv)
            dataset_id = client._upload_dataframe(
                data=df,
                target_column=args.target_column,
                task=args.task,
                name=args.name
            )
            print(f"Dataset uploaded: {dataset_id}")

        elif args.command == "pull-code":
            code = client.pull_code(
                job_id=args.job_id,
                run_id=args.run_id,
                output_file=args.output
            )
            if not args.output:
                print(code)

        elif args.command == "list-datasets":
            # List files in datasets directory
            import veox.datasets.binary
            import veox.datasets.regression
            import pkgutil
            
            print("📦 Built-in Datasets:")
            print("\nBinary Classification:")
            for _, name, _ in pkgutil.iter_modules(veox.datasets.binary.__path__):
                print(f"  - {name}")
            
            print("\nRegression:")
            for _, name, _ in pkgutil.iter_modules(veox.datasets.regression.__path__):
                print(f"  - {name}")

    except Exception as e:
        print(f"❌ Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
