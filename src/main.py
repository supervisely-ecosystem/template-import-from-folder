import os
from dotenv import load_dotenv
import supervisely as sly

# load ENV variables for debug
# has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    pass


app = MyImport()
app.run()
