import os
from dotenv import load_dotenv
import supervisely as sly
import magic

# load ENV variables for debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # list all image files in directory
        mime = magic.Magic(mime=True)
        
        images_names = []
        images_paths = []
        for file in os.listdir(context.path):
            file_path = os.path.join(context.path, file)
            mime_type = mime.from_file(file_path)
            if mime_type.startswith("image"):
                images_names.append(file)
                images_paths.append(file_path)
            else:
                # remove file if it's not an image
                os.remove(file_path)        

        # process text file and remove empty lines
        progress = sly.Progress("Processing images", total_cnt=len(images_names))
        for img_name, img_path in zip(images_names, images_paths):
            try:
                # upload image by path
                api.image.upload_path(dataset_id=context.dataset_id, name=img_name, path=img_path)

                # remove local file after upload
                os.remove(img_path)
            except Exception as e:
                sly.logger.warn("Skip image", extra={"name": img_name, "reason": repr(e)})
            finally:
                progress.iter_done_report()

        return context.project_id


app = MyImport()
app.run()
