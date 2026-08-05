"""
Unit tests for data exporter.
"""

import os
import json
import tempfile
from src.utils.exporter import export_json_data


def test_export_json_data():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock export call
        success = export_json_data(output_dir=temp_dir)
        assert success is True
        assert os.path.exists(os.path.join(temp_dir, "fii_dii.json"))
        assert os.path.exists(os.path.join(temp_dir, "dividends.json"))

        with open(os.path.join(temp_dir, "fii_dii.json"), "r") as f:
            data = json.load(f)
            assert "updated_at" in data
            assert "daily" in data
            assert "stocks" in data
