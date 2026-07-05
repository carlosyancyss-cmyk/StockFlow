from pathlib import Path
import os

PROJECT_DIR = Path(__file__).resolve().parent

IS_ANDROID = (
    "ANDROID_STORAGE" in os.environ
    or os.path.exists("/system")
)

if IS_ANDROID:

    APP_DATA_DIR = PROJECT_DIR

    DOWNLOADS_DIR = APP_DATA_DIR / "downloads"

else:

    APP_DATA_DIR = Path(
        os.getenv("STOCKFLOW_DATA_DIR")
        or (Path.home() / ".stockflow")
    )

    DOWNLOADS_DIR = Path.home() / "Downloads"

print("=" * 50)
print("APP_PATHS")
print("PROJECT_DIR:", PROJECT_DIR)
print("IS_ANDROID:", IS_ANDROID)
print("APP_DATA_DIR:", APP_DATA_DIR)
print("DOWNLOADS_DIR:", DOWNLOADS_DIR)
print("=" * 50)

APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

REPORTS_DIR = DOWNLOADS_DIR / "StockFlow" / "Relatorios"
BACKUPS_DIR = DOWNLOADS_DIR / "StockFlow" / "Backups"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = APP_DATA_DIR / "stockflow.db"

LOGO_PATHS = [
    PROJECT_DIR / "assets" / "logo.png",
    Path("assets") / "logo.png",
]