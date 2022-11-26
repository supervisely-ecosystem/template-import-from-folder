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
    def process(self, workspace_id: int, path: str, is_directory: bool):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # create project with the same name as input file
        project_name = Path(path).stem
        project = api.project.get_or_create(workspace_id, project_name)
        print(f"Working project: id={project.id}, name={project.name}")

        dataset = api.dataset.create(project.id, "dataset", change_name_if_conflict=True)
        print(f"Created dataset: id={dataset.id}, name={dataset.name}")

        names = set()
        with open(path) as file:
            # process text file and remove empty lines
            lines = []
            for line in file:
                normalized_line = line.strip()
                if normalized_line != "":
                    lines.append(normalized_line)

            progress = sly.Progress("Processing urls", total_cnt=len(lines))
            for image_url in lines:
                try:
                    # download image
                    response = requests.get(image_url)

                    # get image name from response
                    d = response.headers["content-disposition"]
                    img_name = re.findall("filename=(.+)", d)[0]
                    img_path = os.path.join("data", img_name)

                    # save image
                    img_data = response.content
                    with open(img_path, "wb") as file:
                        file.write(img_data)

                    # check if image with the same name already exists in our new dataset
                    if img_name in names:
                        img_name = sly.generate_free_name(
                            used_names=names, possible_name=img_name, with_ext=True
                        )

                    # upload image into dataset on Supervisely server
                    info = api.image.upload_path(dataset.id, img_name, img_path)
                    sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")
                    names.add(img_name)

                    # remove local file after upload
                    os.remove(img_path)
                except Exception as e:
                    sly.logger.warn(
                        "Can not process url, skipped", extra={"url": image_url, "reason": repr(e)}
                    )
                finally:
                    progress.iter_done_report()

        return project.id


app = MyImport()
app.run()
