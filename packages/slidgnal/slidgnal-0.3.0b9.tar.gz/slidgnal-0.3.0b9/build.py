# build script for the signal extension module (or just libsignal_ffi)
import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

SRC_PATH = Path(".") / "slidgnal"
LIBSIGNAL_VERSION = "v0.86.4"


class BuildError(BaseException):
    pass


def main():
    build_libsignal(SRC_PATH / "vendor" / "libsignal_ffi.a")
    build_go()


def build_libsignal(dest: Path, version: str = LIBSIGNAL_VERSION, force=False) -> None:
    os.environ["LIBRARY_PATH"] = (
        f"{dest.parent.absolute()}:{os.getenv('LIBRARY_PATH', '')}"
    )
    if dest.exists() and not force:
        # no need to always rebuild it, especially during development
        print("libsignal found, not building it")
        return

    try:
        url = f"https://slidge.im/bin/{get_libsignal_filename(version)}"
        print(f"Attempting to download prebuilt libsignal at {url}")
        urllib.request.urlretrieve(url, filename=dest)
    except Exception as e:
        print(f"Could not download prebuilt libsignal: {e}, attempting to build it…")
    else:
        print("Libsignal was successfully fetched, hooray!")
        return

    if not shutil.which("cargo"):
        raise BuildError(
            "Cannot find the cargo executable in $PATH. "
            "Make you sure install cargo, via your package manager or https://rustup.rs/"
        )
    os.environ["RUSTFLAGS"] = "-Ctarget-feature=-crt-static"
    os.environ["RUSTC_WRAPPER"] = ""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        subprocess.check_call(
            [
                "git",
                "clone",
                "--single-branch",
                "--branch",
                version,
                "https://github.com/signalapp/libsignal.git",
                ".",
            ],
            cwd=tmp_dir,
        )
        try:
            subprocess.check_call(
                ["cargo", "build", "-p", "libsignal-ffi", "--release"], cwd=tmp_dir
            )
        except subprocess.CalledProcessError as e:
            raise BuildError(
                "Building libsignal failed. Make sure you have the required "
                "dependencies installed. In debian, that would be: "
                "build-essential ca-certificates cmake protobuf-compiler libclang-dev"
            ) from e
        shutil.move(tmp_dir / "target/release/libsignal_ffi.a", dest)


def build_go():
    current_sum = ""
    for p in sorted(list(SRC_PATH.glob("**/*.go"))):
        p_rel = p.relative_to(SRC_PATH)
        if p_rel.parents[0].name == "generated":
            continue
        h = hashlib.sha512(p.read_text().encode()).hexdigest()
        current_sum += f"{p_rel}: {h}\n"
    known_sum_path = SRC_PATH / ".gopy.sum"
    previous_sum = known_sum_path.read_text() if known_sum_path.exists() else None
    if current_sum == previous_sum:
        known_sum_path.write_text(current_sum)
        print("Go files have not changed, no need to build")
        return

    if not shutil.which("go"):
        raise RuntimeError(
            "Cannot find the go executable in $PATH. "
            "Make you sure install golang, via your package manager or https://go.dev/dl/"
        )

    os.environ["PATH"] = os.path.expanduser("~/go/bin") + ":" + os.environ["PATH"]
    subprocess.run(["go", "install", "github.com/go-python/gopy@master"], check=True)
    subprocess.run(
        ["go", "install", "golang.org/x/tools/cmd/goimports@latest"], check=True
    )

    print("Building go parts…")
    subprocess.run(
        [
            "gopy",
            "build",
            "-output=generated",
            "-no-make=true",
            ".",
        ],
        cwd=SRC_PATH,
        check=True,
    )
    known_sum_path.write_text(current_sum)


def get_libsignal_filename(version: str = LIBSIGNAL_VERSION) -> str:
    return f"libsignal_ffi-{platform.system()}-{platform.machine()}-{version}.a"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--only-libsignal", action="store_true", dest="only_libsignal")
    args = parser.parse_args()
    if args.only_libsignal:
        build_libsignal(Path(".") / get_libsignal_filename(), force=True)
    else:
        main()
