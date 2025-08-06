from dotenv import load_dotenv
import os

load_dotenv()

# =====================
# VictoriaDB Config
# =====================
VICTORIADB_HOST = os.getenv("VICTORIADB_HOST")
VICTORIADB_PORT = os.getenv("VICTORIADB_PORT")

VICTORIADB_PUSH_ENDPOINT = os.getenv("VICTORIADB_PUSH_METRIC_ENDPOINT")

VICTORIADB_QUERY_ENDPOINT = os.getenv("VICTORIADB_QUERY_METRIC_ENDPOINT")

VICTORIADB_BULK_QUERY_ENDPOINT = os.getenv("VICTORIADB_BULK_QUERY_METRIC_ENDPOINT")


# =====================
# Bulk Push Config
# =====================
BULK_PUSH_BATCH_COUNT = int(os.getenv("BULK_PUSH_BATCH_COUNT"))
BULK_PUSH_BATCH_SIZE = int(os.getenv("BULK_PUSH_BATCH_SIZE"))


# =====================
# Bulk Query Config
# =====================
BULK_QUERY_STEP = os.getenv("BULK_QUERY_STEP")
