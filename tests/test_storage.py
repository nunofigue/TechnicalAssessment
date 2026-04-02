import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from storage import Storage


def test_store_csv_local(tmp_path):
    # Create sample DataFrame
    df = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["a", "b"]
    })

    # Temporary file path
    file_path = tmp_path / "test_output.csv"

    storage = Storage()
    storage.store_csv(df, str(file_path))

    # Check if file was created
    assert file_path.exists()

    # Check if data is correct
    loaded_df = pd.read_csv(file_path)
    assert len(loaded_df) == 2
    assert loaded_df["col1"].tolist() == [1, 2]
    assert loaded_df["col2"].tolist() == ["a", "b"]