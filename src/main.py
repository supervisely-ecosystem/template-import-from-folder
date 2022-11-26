import os
import re
from pathlib import Path
from dotenv import load_dotenv
import requests
import supervisely as sly

# load ENV variables for debug
# has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    def process_file(self, workspace_id: int, path: str):
        name = Path(path).stem
        api = sly.Api.from_env()
        # project = api.project.create(workspace_id, name, change_name_if_conflict=True)
        # print(f"Project has been successfully created: id={project.id}, name={project.name}")
        # dataset = api.dataset.create(project.id, "dataset-01")
        # print(f"Dataset has been successfully created: id={dataset.id}, name={dataset.name}")

        with open(path) as file:
            for line in file:
                image_url = line.strip()

                # download image
                response = requests.get(image_url)

                # get image name from response
                d = response.headers["content-disposition"]
                img_name = re.findall("filename=(.+)", d)[0]
                img_data = response.content
                with open(img_name, "wb") as file:
                    file.write(img_data)


app = MyImport()
app.run()
