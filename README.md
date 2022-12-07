<div align="center" markdown>

<img src="https://user-images.githubusercontent.com/48913536/206165736-f69b6b92-dd82-45d7-84d7-9812f2e84e63.png"/>

# Import from Folder

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Develop">How to Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/template-import-from-folder)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/template-import-from-folder)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/template-import-from-folder.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/template-import-from-folder.png)](https://supervise.ly)

</div>

# Overview

This template is designed as a starting point for developers to create custom import apps for Supervisely platform.
Template app in it's current state will upload image files in the given directory to selected project or dataset.

Describe the type of data your app is importing e.g: images, videos, COCO, PascalVoc or any other data format.

Describe an input folder structure using examples.

**Example:**

```text
data
├── image_1.jpg
├── image_2.jpg
└── image_3.jpg
```

Insert a link to demo data for users.

# How to Run

App can be launched from ecosystem, project, dataset, or folder in team files.

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

<details>
<summary open>Run from Project or Dataset</summary>
<br>

Run the application from the context menu of the folder (right mouse button) on Team Files page
  
<img src=""/>

</details>

<details>
<summary open>Run from team files</summary>
<br>

Run the application from the context menu of the folder (right mouse button) on Team Files page
  
<img src=""/>

</details>
