# Tufts Dental Dataset to COCO

The original dataset is available from [Tufts Official](https://tdd.ece.tufts.edu/).

This repository aims to convert the **Tufts** annotation `JSON` file into **COCO** format `JSON` file.

> [!WARNING]  
> in the tufts dataset, the tooth is named as "title",
> And it belongs to the list:\
> `label_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
'32', 'A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'R', 'S', 'T', 'N', 'Q', 'P', 'E', 'F', 'O']`\
> I don't know why the teeth are named this way, as other articles usually follow the FDI method for tooth naming. Additionally, the total number of human teeth, including wisdom teeth, is only 32, so I'm unsure what the 'A', 'B', 'C', and so on letters signify. I am still awaiting assistance and clarification from the respective authors.

The original JSON file is under the directory Segmentation：`teeth_bbox.json`and`teeth_polygon.json`.
```
|--Tufts_dental_dataset
    |-- Expert
    |-- Student
    |-- Radiographs
    |-- Segmentation
        |-- maxillomandibular
        |-- teeth_mask
        |-- teeth_bbox.json
        |-- teeth_polygon.json
```
If you find it helpful, please consider giving it a star🌟.

Discussions are welcome !

# It is worth noting that the bounding box is different
```
tufts bbox：[x_min, y_min, x_max, y_max]
coco bbox ：[x_min, y_min, width, height]
```

## COCO annotation format
```json
{
    "info": {
        "description": "COCO 2017 Dataset","url": "http://cocodataset.org","version": "1.0","year": 2017,"contributor": "COCO Consortium","date_created": "2017/09/01"
    },
    "licenses": [
        {"url": "http://creativecommons.org/licenses/by/2.0/","id": 4,"name": "Attribution License"}
    ],
    "images": [
        {"id": 242287, "license": 4, "coco_url": "http://images.cocodataset.org/val2017/xxxxxxxxxxxx.jpg", "flickr_url": "http://farm3.staticflickr.com/2626/xxxxxxxxxxxx.jpg", "width": 426, "height": 640, "file_name": "xxxxxxxxx.jpg", "date_captured": "2013-11-15 02:41:42"},
        {"id": 245915, "license": 4, "coco_url": "http://images.cocodataset.org/val2017/nnnnnnnnnnnn.jpg", "flickr_url": "http://farm1.staticflickr.com/88/xxxxxxxxxxxx.jpg", "width": 640, "height": 480, "file_name": "nnnnnnnnnn.jpg", "date_captured": "2013-11-18 02:53:27"}
    ],
    "annotations": [
        {"id": 125686, "category_id": 0, "iscrowd": 0, "segmentation": [[164.81, 417.51,......167.55, 410.64]], "image_id": 242287, "area": 42061.80340000001, "bbox": [19.23, 383.18, 314.5, 244.46]},
        {"id": 1409619, "category_id": 0, "iscrowd": 0, "segmentation": [[376.81, 238.8,........382.74, 241.17]], "image_id": 245915, "area": 3556.2197000000015, "bbox": [399, 251, 155, 101]},
        {"id": 1410165, "category_id": 1, "iscrowd": 0, "segmentation": [[486.34, 239.01,..........495.95, 244.39]], "image_id": 245915, "area": 1775.8932499999994, "bbox": [86, 65, 220, 334]}
    ],
    "categories": [
        {"supercategory": "speaker","id": 0,"name": "echo"},
        {"supercategory": "speaker","id": 1,"name": "echo dot"}
    ]
}
``` 

# install  cocoapi 
install the cocoapi to visualization the annotation
```
# install pycocotools
cd ~/github
git clone https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI
python setup.py build_ext install
```

# prepare dataset
```
mkdir -p datasets/coco
ln -s /path_to_coco_dataset/annotations datasets/coco/annotations
ln -s /path_to_coco_dataset/train datasets/coco/train
```

or just make the dataset directory tree like this:
```
|--coco
    |-- test
    |-- val
    |-- train
        |-- 1.png
        |-- 2.png
        ...
    |-- annotations
        |-- teeth_bbox.json
        |-- teeth_polygon.json
        |-- train.json
        |-- val.json
        |-- test.json
```
