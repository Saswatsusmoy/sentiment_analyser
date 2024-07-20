# backend/run.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import create_app

from app.utils.helpers import ensure_upload_folder_exists

app = create_app()

ensure_upload_folder_exists(app)

if __name__ == '__main__':
    app.run(debug=True)



