"""Assemble an uncompiled Windows demo using the installed Ren'Py SDK.

Fallback when the SDK launcher cannot run in the automation environment.
This is NOT a replacement for lint or a Windows launch test.
Only allowlisted game files are included; local saves and stale bytecode are not.
"""
from pathlib import Path
import argparse
import hashlib
import shutil
import zipfile
from windows_icon import embed_icon


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    sdk = args.sdk.resolve()
    output = args.output.resolve()
    # Never clean/overwrite an earlier release or the working tree.
    output.mkdir(parents=True, exist_ok=False)
    name = "평온의방_데모_v0.2.1_Windows"
    package = output / name
    package.mkdir()

    def copy(source, relative):
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    # Match the launch layout used by Ren'Py's Distributor.add_windows_files.
    copy(sdk / "lib/py3-windows-x86_64/renpy.exe", "평온의 방.exe")
    copy(sdk / "renpy.py", "평온의 방.py")
    for folder in ("renpy", "lib/python3.12", "lib/py3-windows-x86_64"):
        for source in sorted((sdk / folder).rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(sdk)
            if any(part.startswith(".") for part in relative.parts):
                continue
            if source.suffix in (".pyx", ".pxd", ".pxi", ".log"):
                continue
            if folder == "lib/py3-windows-x86_64" and source.name == "renpy.exe":
                continue
            copy(source, relative)
    copy(sdk / "LICENSE.txt", "renpy/LICENSE.txt")
    embed_icon(package / "평온의 방.exe", project / "icon.ico")
    embed_icon(package / "lib/py3-windows-x86_64/pythonw.exe", project / "icon.ico")

    for filename in ("script.rpy", "corridor_demo.rpy", "screens.rpy", "state.rpy", "options.rpy"):
        copy(project / "game" / filename, Path("game") / filename)
    asset_types = {".png", ".jpg", ".jpeg", ".webp", ".wav", ".ogg", ".mp3", ".ttf", ".otf", ".txt"}
    for folder in ("images", "audio", "fonts"):
        for source in sorted((project / "game" / folder).rglob("*")):
            if source.is_file() and source.suffix.lower() in asset_types:
                copy(source, source.relative_to(project))
    for filename in ("DEMO-README.md", "CREDITS.md"):
        copy(project / filename, filename)

    # The official distributor creates this marker too. It disables developer
    # mode before options/screens initialize (see 00compat and 00library).
    (package / "game/script_version.txt").write_text("(8, 5, 3)", encoding="utf-8")
    archive = output / (name + ".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for source in sorted(package.rglob("*")):
            if source.is_file():
                z.write(source, Path(name) / source.relative_to(package))

    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None, "ZIP integrity failure"
        entries = [Path(n).relative_to(name).as_posix() for n in z.namelist()]
        assert "평온의 방.exe" in entries
        assert "평온의 방.py" in entries
        assert "game/images/app_icon.png" in entries
        assert "game/images/room_cold_fhd.png" in entries
        assert "lib/py3-windows-x86_64/pythonw.exe" in entries
        assert "game/script_version.txt" in entries
        assert not any(n.startswith(("game/saves/", "game/cache/", "docs/", "tools/", ".git/"))
                       or n.startswith("game/tests.") for n in entries)
        assert not any(n.startswith("game/") and n.endswith(".rpyc") for n in entries)
        assert "game/fonts/NanumGothic-OFL.txt" in entries
        assert "game/fonts/NanumPenScript-OFL.txt" in entries
    digest = hashlib.file_digest(archive.open("rb"), "sha256").hexdigest()
    (output / (archive.name + ".sha256")).write_text(
        digest + "  " + archive.name + "\n", encoding="utf-8"
    )
    print(f"Package: {archive}")
    print(f"ZIP verified: {len(entries)} files, {archive.stat().st_size:,} bytes")
    print(f"SHA256: {digest}")
    print("Runtime launch/lint still required. Game scripts compile on first launch.")


if __name__ == "__main__":
    main()
