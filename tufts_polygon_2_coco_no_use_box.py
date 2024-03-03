import json
import numpy as np
from PIL import Image, ImageDraw


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

title_arr = []#count the title in the tufts json,which is used as the label_names

print('Open label JSON')

with open(json_name) as json_file:
    labelbox_data = json.load(json_file)

images = []
annotations = []

img_id = 0
ann_id = 0

def getbbox(points):
    global img_shape
    polygons = points
    mask = polygons_to_mask(img_shape, polygons)
    return mask2box(mask)

def mask2box(mask):
    '''not use the bbox in the json 
    or there is no bbox in the json
    '''    
    index = np.argwhere(mask == 1)
    rows = index[:, 0]
    clos = index[:, 1]

    left_top_r = np.min(rows)  # y
    left_top_c = np.min(clos)  # x

    right_bottom_r = np.max(rows)
    right_bottom_c = np.max(clos)

    return [
        left_top_c,
        left_top_r,
        right_bottom_c - left_top_c,
        right_bottom_r - left_top_r,
    ]

def polygons_to_mask(img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

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
    for poly in data_row['Label']['objects']:
        annotation = {}

        # title_in_tufts = poly["title"]  #only used during counting the label title
        # if title_in_tufts not in title_arr:
        #     title_arr.append(title_in_tufts)

        points = []
        seg = []
        for pnt in poly['polygons']:
            for x_y in pnt:
                points.append([x_y[0], x_y[1]])
                seg.append(x_y[0])
                seg.append(x_y[1])

        contour = np.array(points)
        x = contour[:, 0]
        y = contour[:, 1]
        
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        annotation["segmentation"] = [seg]
        annotation["iscrowd"] = 0
        annotation["area"] = area
        annotation["image_id"] = img_id

        annotation["bbox"] = list(map(float, getbbox(points)))

        cat_id = label_names.index(poly['title'])

        annotation["category_id"] = cat_id 
        annotation["id"] = ann_id

        annotations.append(annotation)
        ann_id +=1

    img_id+=1

print('Create new JSON structure')

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
path_newjson = "tufts_polygon_2_coco_no_use_box.json"
with open(path_newjson, 'w') as outfile:
    json.dump(coco_struc, outfile)

print('coco JSON exported')

