import sys
import time
from src.extract import main as extract_main
from src.load import main as load_main
from src.transform import run_transformations
from src.data_quality import run_data_quality_checks


def run_pipeline():
    start_time = time.time()
    print("🚀 Starting FPL ELT Data Pipeline...\n")

    try:
        # Step 1: Extract
        print("--- [1/4] EXTRACTING RAW DATA ---")
        extract_main()

        # Step 2: Load
        print("\n--- [2/4] LOADING TO STAGING ---")
        load_main()

        # Step 3: Transform
        print("\n--- [3/4] TRANSFORMING TO STAR SCHEMA ---")
        run_transformations()

        # Step 4: Data Quality Checks
        print("\n--- [4/4] RUNNING DATA QUALITY ASSERTIONS ---")
        run_data_quality_checks()

        elapsed = round(time.time() - start_time, 2)
        print(f"\n🎉 Pipeline executed successfully in {elapsed}s!")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()