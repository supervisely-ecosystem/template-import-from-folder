import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import supervisely as sly

# load ENV variables for debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    def process(self, workspace_id: int, path: str, is_directory: bool):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # create project with the same name as input file and empty dataset in it
        project_name = Path(path).stem
        project = api.project.get_or_create(workspace_id, project_name)
        print(f"Working project: id={project.id}, name={project.name}")
        dataset = api.dataset.create(project.id, "dataset", change_name_if_conflict=True)
        print(f"Created dataset: id={dataset.id}, name={dataset.name}")

        # read input file, remove empty lines + leading & trailing whitespaces
        with open(path) as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        # process text file and remove empty lines
        progress = sly.Progress("Processing urls", total_cnt=len(lines))
        for index, img_url in enumerate(lines):
            try:
                img_ext = Path(img_url).suffix
                img_name = f"{index:03d}{img_ext}"
                img_path = os.path.join(os.getcwd(), "data", img_name)

                # download image
                response = requests.get(img_url)
                with open(img_path, "wb") as file:
                    file.write(response.content)

                # upload image into dataset on Supervisely server
                info = api.image.upload_path(dataset.id, img_name, img_path)
                sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")

                # remove local file after upload
                os.remove(img_path)
            except Exception as e:
                sly.logger.warn("Skip image", extra={"url": img_url, "reason": repr(e)})
            finally:
                progress.iter_done_report()

        return project.id


app = MyImport()
app.run()
