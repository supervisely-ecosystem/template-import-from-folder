<div align="center" markdown>

<img src=""/>

# Import from Folder

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Run">How to Run</a> •
  <a href="#Input-Data-Structure">Input Data Structure</a> •
  <a href="#Demo">Demo</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/template-import-from-folder)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/template-import-from-folder)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/template-import-from-folder.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/template-import-from-folder.png)](https://supervise.ly)

</div>

# Overview

Template import from folder app is designed for **developers** and can be used as a starting point for creating an application for importing your data to Supervisely.

# How to Develop

## Preparation

**Step 1.** Prepare `~/supervisely.env` file with credentials. [Learn more here.](https://developer.supervise.ly/getting-started/basics-of-authentication#how-to-use-in-python)

**Step 2.** Clone [repository](https://github.com/supervisely-ecosystem/template-import-from-folder) with source code and create [Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
git clone https://github.com/supervisely-ecosystem/template-import-from-folder
cd template-import-from-folder
./create_venv.sh
```

**Step 3.** Open repository directory in Visual Studio Code.

```bash
code -r .
```

**Step 4.** Open `local.env` file and input your values here

```python
CONTEXT_TEAMID=8            # ⬅️ change it
CONTEXT_WORKSPACEID=349     # ⬅️ change it
# CONTEXT_PROJECTID=14488   # ⬅️ specify when importing to existing project
# CONTEXT_DATASETID=52322   # ⬅️ specify when importing to existing dataset
FOLDER="data/"              # ⬅️ change it
SLY_APP_DATA_DIR="results/" # ⬅️ change it
```

## How to debug this template

### Debug options

`launch.json` has 2 script launch options:
  1. Debug: local folder
  2. Advanced debug: team files folder

**Option 1.** Debug: local folder

Template import from folder app comes with a sample images in `data` directory.

```bash
.
└── data
    ├── cat_1.jpg
    ├── cat_2.jpg
    └── cat_3.jpg
```

You can place your own images there or use this sample. You can change the folder (`FOLDER`) in the `local.env` file to any other suitable location on your computer's hard drive.

**Option 2.** Advanced debug: team files folder

This option is a simulation of a real production import app. To use advanced debug, upload an image folder to team files, copy the path of that folder in team files, and then paste it to `local.env` - `FOLDER`.

<img src=""/>

### Writing an import script

#### Import libraries

```python
import os
from dotenv import load_dotenv
import supervisely as sly
```

#### Load environment variables

```python
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
```

#### Create an Import class inherited from sly.app.Import

Class `sly.app.Import` will handle downloading of the directory to the location specified in `local.env`.
You just need to write a script to import your data to Supervisely instance.

```python
class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        # create api object to communicate with Supervisely Server
        api = sly.Api.from_env()

        # list images in the downloaded directory
        images_names = []
        images_paths = []
        for file in os.listdir(context.path):
            file_path = os.path.join(context.path, file)
            images_names.append(file)
            images_paths.append(file_path)

        # process images and upload them by paths
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
```

#### Initialize an app object from created class and run the app

```python
app = MyImport()
app.run()
```

# How To Import App to Ecosystem [Enterprise Edition only]

**Step 1.** Go to Ecosystem page and click on `private apps`

<img src="https://user-images.githubusercontent.com/48913536/172667770-880d2c2b-2827-4fc1-ac84-1f5c6827eb66.png" style="width:80%;"/>

**Step 2.** Click `+ Add private app` button

<img src="https://user-images.githubusercontent.com/48913536/172667780-6e87d2f7-3f68-40bd-a70f-f897568f2ffb.png" style="width:80%;"/>

**Step 3.** Copy and paste repository url and generated [github/gitlab personal token](https://docs.supervise.ly/enterprise-edition/advanced-tuning/private-apps) to modal window

<img src="https://user-images.githubusercontent.com/48913536/172667782-b5678b3d-0950-4638-bd66-abae8b8a6719.png" style="width:50%;"/>

# How to Run

App can be launched from ecosystem or folder in team files.

<details>
<summary open>Run from team files</summary>
<br>

Run the application from the context menu of the folder (right mouse button) on Team Files page
  
<img src=""/>

</details>

<details>
<summary>Run from ecosystem</summary>
<br>
Click `Run application` button on the right side of the app page. Modal window will be opened.
  
<img src="">

1. If you want to upload project folder from your computer, choose `Drag & Drop` option. You can upload the project folder to drag-and-drop field or you can click on the drag-and-drop field and choose project from your computer in opened window.
  
<img src=""/>

2. If you want to import project from Team Files, choose `Team Files` option and choose folder to import in the modal window.
  
<img src=""/>

</details>
