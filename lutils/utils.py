import os


# check if path exists, create dir if not
def check_dir(path: str) -> None:
      if not os.path.exists(path):
            os.makedirs(path)