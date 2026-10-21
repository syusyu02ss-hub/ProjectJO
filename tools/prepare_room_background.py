"""Create the approved Full HD room asset without regenerating its contents."""
from pathlib import Path

from PIL import Image


def main():
    project = Path(__file__).resolve().parents[1]
    source = project / "game/images/room_cold.png"
    target = project / "game/images/room_cold_fhd.png"
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite: {target}")
    with Image.open(source) as image:
        # Match the game's previous full-frame mapping: no crop or new detail.
        result = image.resize((1920, 1080), Image.Resampling.LANCZOS)
        metadata = {}
        if image.info.get("icc_profile"):
            metadata["icc_profile"] = image.info["icc_profile"]
        result.save(target, **metadata)
    with Image.open(target) as saved:
        assert saved.size == (1920, 1080)
        saved.verify()
    print(f"Created {target} (1920x1080, Lanczos, original preserved)")


if __name__ == "__main__":
    main()
