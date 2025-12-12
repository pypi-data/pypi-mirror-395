__version__ = "0.1.2"

# Expose the FastAPI app at package level for `uvicorn "sohyloha.main:app"`
from .main import app  # noqa: F401
