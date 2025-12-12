import os
import csv
from io import StringIO
import openpyxl

TEXT_EXT = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".html", ".css",
    ".java", ".go", ".rs", ".cpp", ".c", ".cs", ".kt", ".swift",
    ".yml", ".yaml", ".toml", ".md", ".txt", ".env", ".ini", ".cfg"
}

CSV_EXT = {".csv"}
EXCEL_EXT = {".xlsx", ".xls"}


def is_binary_file(file_path, chunk_size=1024):
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(chunk_size)
            if b"\x00" in chunk:
                return True
    except:
        return True
    return False


def read_csv_preview(file_path, max_rows=5):
    output = StringIO()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                output.write(",".join(row) + "\n")
        output.write("<<FIRST 5 ROWS ONLY>>\n")
    except Exception as e:
        return f"<<CSV READ ERROR: {e}>>"
    return output.getvalue()


def read_excel_preview(file_path, max_rows=5):
    """
    Excel dosyasının ilk 5 satırını regex/LMM dostu
    text tablo formatında döndürür.
    """
    output = StringIO()

    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb.active

        rows = []
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i >= max_rows:
                break
            rows.append(list(row))

        # Kolonları stringe çevir (None → boş)
        rows = [[("" if v is None else str(v)) for v in r] for r in rows]

        # Tablo formatı üretelim
        for idx, row in enumerate(rows):
            formatted = " | ".join(row)
            output.write(f"[EXCEL ROW {idx + 1}] {formatted}\n")

        output.write("<<FIRST 5 ROWS ONLY>>\n")

    except Exception as e:
        return f"<<EXCEL READ ERROR: {e}>>"

    return output.getvalue()


def read_file_content(file_path):
    _, ext = os.path.splitext(file_path)

    if ext in CSV_EXT:
        return read_csv_preview(file_path)

    if ext in EXCEL_EXT:
        return read_excel_preview(file_path)

    if ext in TEXT_EXT:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except:
            return "<<TEXT READ ERROR>>"

    # Binary?
    if is_binary_file(file_path):
        return "<<BINARY FILE - SKIPPED>>"

    # Otherwise treat as text
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return "<<UNREADABLE FILE>>"
