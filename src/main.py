import os
from dotenv import load_dotenv
import supervisely as sly

# load ENV variables for debug
# has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


def main():
    print("123")


if __name__ == "__main__":
    main()
