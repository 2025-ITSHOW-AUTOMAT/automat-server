import os

def clean_temp_dir(temp_dir: str = "uploads/temp", keep: int = 3):
    files = sorted(
        [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)],
        key=os.path.getctime
    )
    for file_path in files[:-keep]:
        os.remove(file_path)
