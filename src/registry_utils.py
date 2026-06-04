import os
from datetime import datetime


def get_model_storage_path(base_dir="models"):
    """Generates a structured, production-grade timestamped path for saving model artifacts.

    Example output structure: models/v_20260604_123045/
    """
    # 1. Generate a clean timestamp string using datetime.now().strftime()
    # Format suggestion: "v_%Y%m%d_%H%M%S"
    timestamp = datetime.now().strftime("v_%Y%m%d_%H%M%S")

    # 2. Combine the base_dir and the timestamp folder name using os.path.join
    model_path = os.path.join(base_dir, timestamp)

    # 3. Create the directory safely if it does not exist using os.makedirs
    os.makedirs(model_path, exist_ok=True)

    print(f"Production storage allocated at: {model_path}")
    return model_path
