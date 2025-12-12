from pathlib import Path

BUNDLED_TRUSTEDLIBS_DIR = Path(__file__).parent.parent / "python_analyzer" / "trustedlibs" / "lib_files"

FILE_URL_PATHS = [
    "/trustedlibs/trusted_file_hashes.csv",
    "/trustedlibs/untrusted_file_hashes.csv",
]

METADATA_URL_PATH = "/trustedlibs/metadata.json"

DEFAULT_TRUSTEDLIBS_URL = "https://cdn.appinspect.splunk.com"
