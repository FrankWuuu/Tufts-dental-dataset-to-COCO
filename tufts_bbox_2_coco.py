import json
import numpy as np

# This part is not evaluated coz I only need the segmentation annotation

img_shape = [840, 1615] #height, widht
# label_names = [str(i) for i in range(1,50)] 
# this label_names coulb be also named different. but you should also change the 'name' in the category

'''
label_names same as 'title' in JSON file
I count them first then convert json to coco json
'''
label_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
'32', 'A', 'B', 'C', 'D', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'R', 'S', 'T', 'N', 'Q', 'P', 'E', 'F', 'O']

categories = [{
            "id": 0,
            "name": "_background_",
            "supercategory": "none"
        },
        ]
for label_name in label_names:
    category = {"id":label_names.index(label_name)+1,"name":label_name,"supercategory": "none"}
    categories.append(category)

print(categories)

json_name = 'E:/files/data/teeth_Tufts/Segmentation/teeth_polygon.json'

print('Open label JSON')

title_arr = []#count the title in the tufts json,which is used as the label_names

with open(json_name) as json_file:
    labelbox_data = json.load(json_file)

images = []
annotations = []

img_id = 0
ann_id = 0


print('Create info from JSON')

for data_row in labelbox_data:

    image = {}
    image['id'] = img_id
    image['license'] = 1
    image['file_name'] = data_row['External ID']
    image['height'] = img_shape[0]
    image['widht'] = img_shape[1]
    # image['date_caputred'] = data_row['Created At']

    images.append(image)

    #Append polygonoms
    for object in data_row['Label']['objects']:
        annotation = {}

        # convert the pascal bbox to coco bbox
        x_min, y_min, x_max, y_max = object["bounding box"] 
        width = x_max - x_min
        height = y_max - y_min
        bbox = [x_min, y_min, width, height]

        area = height*width

        annotation["segmentation"] = None
        annotation["iscrowd"] = 0
        annotation["area"] = area
        annotation["image_id"] = img_id

        annotation["bbox"] = bbox

        cat_id = label_names.index(object['title'])

        annotation["category_id"] = cat_id 
        annotation["id"] = ann_id

        annotations.append(annotation)
        ann_id +=1

    img_id+=1

print(title_arr)


coco_struc= {
    'info': {
        'year': '2024', 
        'version': '1',
        "contributor": "Frankwu2029",
        }, 
    'licenses': [{
        "id": 1,
        "url": None,
        "name": "Public"
        }],
    "categories": categories,
    'images': images,
    'annotations': annotations
    }

print('Export JSON')
path_newjson = "coco_ins_demo_out333.json"
with open(path_newjson, 'w') as outfile:
    json.dump(coco_struc, outfile)

print('coco JSON exported')

