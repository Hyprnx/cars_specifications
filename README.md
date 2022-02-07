# CARS SPECIFICATION
<div id="top"></div>
<br>

This repo contains the source code for crawler and crawled data of cars specifications from 
[autodata](auto-data.net). The data has roughly 45k cars from round 1980 to late 2021. To be more specific, head to
[cars_specs.json](car_specifications/car_specifications/resources/cars_specs.json). The data is raw, so you can do 
anything you want with it.

<p align="right">(<a href="#top">back to top</a>)</p>
<br>

# Getting started

Open Terminal / cmd and do the following:
## Create and activate virtual environment
### Create
 ```sh
  python -m venv <envname>
  ```

### Activate

- On Mac:
  ```sh
  source <envname>/bin/activate
  ```
- On Windows:
  ```sh
  <envname>\Scripts\activate
  ```

<p align="right">(<a href="#top">back to top</a>)</p>
<br>

## Install requirements.txt
  ```sh
  pip install -r requirement.txt
  ```
<p align="right">(<a href="#top">back to top</a>)</p>

<p align="right">(<a href="#top">back to top</a>)</p>
<br>

## Running
This repo contains 1 (one) Python script that you can/should modify, head to 
[autodata.py](car_specifications/car_specifications/spiders/autodata.py) and run. If you are familiar with Scrapy,
you can modify other settings, middleware or pipelines as you wish (not recommended). 

# Contact us
[To Duc Anh](mailto:toducanh2001@gmail.com)
If you use this dataset, please give me a star and cite this repo. Thanks!

Project Link: [Cars Specification](https://github.com/Hyprnx/cars_specifications)