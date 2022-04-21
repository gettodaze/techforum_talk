from pathlib import Path
import shutil
from PIL import Image

input_path = Path("input")
output_path = Path("output/images_0")
output_path.mkdir(exist_ok=True, parents=True)

for path in input_path.iterdir():
    if path.suffix != ".jpg":
        continue

    Image.open(path).show()

    new_name = input(f"Current name: {path.stem}.\nNew name? ")
    new_path = output_path / f"{new_name}{path.suffix}"

    shutil.copyfile(path, new_path)
    print(f"Copied {path} to {new_path}. ")
