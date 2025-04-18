import os


def check_dir(path: str) -> None:
      if not os.path.exists(path):
            os.makedirs(path)