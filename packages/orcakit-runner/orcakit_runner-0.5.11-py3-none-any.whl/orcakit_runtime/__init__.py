import importlib.util
import os
import sys

import structlog

logger = structlog.stdlib.get_logger(__name__)

try:
    RUNTIME_EDITION = os.environ["ORCAKIT_RUNTIME_EDITION"]
    RUNTIME_PACKAGE = f"orcakit_runtime_{RUNTIME_EDITION}"
except KeyError:
    raise ValueError(
        "ORCAKIT_RUNTIME_EDITION environment variable is not set."
        " Expected ORCAKIT_RUNTIME_EDITION to be set to one of:\n"
        " - inmem\n"
        " - postgres\n"
        " - community\n"
    ) from None
if importlib.util.find_spec(RUNTIME_PACKAGE):
    backend = importlib.import_module(RUNTIME_PACKAGE)
    logger.info(f"Using {RUNTIME_PACKAGE}")
else:
    raise ImportError(
        "Orcakit runtime backend not found. Please install with "
        f'`pip install "orcakit-runtime-{RUNTIME_EDITION}"`'
    ) from None

# All runtime backends share the same API
for module_name in (
    "checkpoint",
    "database",
    "lifespan",
    "ops",
    "retry",
    "store",
    "metrics",
):
    sys.modules["orcakit_runtime." + module_name] = getattr(backend, module_name)
