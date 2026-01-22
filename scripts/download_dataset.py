import os
import urllib.request

BASE_URL = "https://physionet.org/files/challenge-2016/1.0.0/"
FILES = [
    "training-a.tar.gz",
    "training-b.tar.gz",
]


def main() -> None:
    os.makedirs("backend/data/physionet", exist_ok=True)
    for filename in FILES:
        url = f"{BASE_URL}{filename}"
        destination = os.path.join("backend/data/physionet", filename)
        if os.path.exists(destination):
            print(f"Already downloaded: {destination}")
            continue
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, destination)
    print("Download complete. Extract the tar.gz files to use for optional training.")


if __name__ == "__main__":
    main()
