import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    filename="logs.txt",
    encoding="utf-8"
)
# Delete httpx and openai logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

log = logging.getLogger(__name__)