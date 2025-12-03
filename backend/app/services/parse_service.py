"""Parse service for processing NSE files"""

import csv
import zipfile
from pathlib import Path

from app.services.utils import log_message


class ParseService:
    """Service for parsing and normalizing NSE data files"""

    def __init__(self):
        pass

    def _extract_zip(self, zip_path: Path, extract_to: Path) -> bool:
        """Extract a zip file"""
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            log_message(f"Extracted: {zip_path.name}")
            return True
        except Exception as e:
            log_message(f"Error extracting {zip_path.name}: {e!s}")
            return False

    def _parse_csv(self, csv_path: Path) -> int:
        """Parse a CSV file and return row count"""
        try:
            with open(csv_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                return sum(1 for row in reader) - 1  # Exclude header
        except Exception as e:
            log_message(f"Error parsing CSV {csv_path.name}: {e!s}")
            return 0

    def _normalize_csv(self, input_csv: Path, output_csv: Path) -> int:
        """Normalize CSV file (basic normalization - can be extended)"""
        try:
            row_count = 0
            with open(input_csv, encoding="utf-8") as infile:
                reader = csv.reader(infile)
                header = next(reader)  # Skip header

                with open(output_csv, "w", encoding="utf-8", newline="") as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)  # Write header

                    for row in reader:
                        # Basic normalization: strip whitespace, handle empty values
                        normalized_row = [cell.strip() if cell else "" for cell in row]
                        writer.writerow(normalized_row)
                        row_count += 1

            return row_count
        except Exception as e:
            log_message(f"Error normalizing CSV {input_csv.name}: {e!s}")
            return 0

    async def parse_files(self, raw_path: str, output_path: str) -> dict[str, int]:
        """Parse raw NSE files and generate normalized CSV files
        Returns dict with table names and row counts
        """
        results = {}

        raw_path_obj = Path(raw_path)
        output_path_obj = Path(output_path)
        output_path_obj.mkdir(parents=True, exist_ok=True)

        # Create temp extraction directory
        temp_extract = output_path_obj / "temp_extract"
        temp_extract.mkdir(exist_ok=True)

        # Process all zip files
        zip_files = list(raw_path_obj.glob("*.zip"))
        log_message(f"Found {len(zip_files)} zip files to process")

        for zip_file in zip_files:
            # Extract zip
            extract_dir = temp_extract / zip_file.stem
            extract_dir.mkdir(exist_ok=True)

            if not self._extract_zip(zip_file, extract_dir):
                continue

            # Process extracted CSV files
            csv_files = list(extract_dir.glob("*.csv"))
            for csv_file in csv_files:
                # Normalize CSV
                normalized_name = f"{zip_file.stem}_{csv_file.name}"
                normalized_path = output_path_obj / normalized_name

                row_count = self._normalize_csv(csv_file, normalized_path)
                table_name = normalized_name.replace(".csv", "")
                results[table_name] = row_count
                log_message(f"Normalized {table_name}: {row_count} rows")

        # Process DAT files
        dat_files = list(raw_path_obj.glob("*.DAT"))
        log_message(f"Found {len(dat_files)} DAT files to process")

        for dat_file in dat_files:
            # For DAT files, we'll just copy them for now
            # You can add specific parsing logic here
            output_dat = output_path_obj / dat_file.name
            try:
                import shutil

                shutil.copy2(dat_file, output_dat)
                results[dat_file.stem] = 1  # Placeholder count
                log_message(f"Copied DAT file: {dat_file.name}")
            except Exception as e:
                log_message(f"Error copying DAT file {dat_file.name}: {e!s}")

        # Cleanup temp directory
        try:
            import shutil

            shutil.rmtree(temp_extract)
        except Exception:
            # If cleanup fails, it's non-fatal for parsing results
            pass

        log_message(f"Parsing completed. Processed {len(results)} files.")
        return results
