import os
import xml.etree.ElementTree as ET

voc_annotations = './Annotations'
yolo_labels = './labels'
image_sets_dir = './Main'

os.makedirs(yolo_labels, exist_ok=True)

def convert_annotation(xml_file, label_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(label_file, 'w') as out:
        for obj in root.findall('object'):
            cls_id = 0  # only one class: garbage
            xmlbox = obj.find('bndbox')
            xmin = float(xmlbox.find('xmin').text)
            ymin = float(xmlbox.find('ymin').text)
            xmax = float(xmlbox.find('xmax').text)
            ymax = float(xmlbox.find('ymax').text)


            x_center = (xmin + xmax) / 2.0 / w
            y_center = (ymin + ymax) / 2.0 / h
            width = (xmax - xmin) / w
            height = (ymax - ymin) / h

            out.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# /Users/abdullahasif/Documents/University/Sem_6/dl/proj/FloW_IMG/test/annotations/000001.xml to /Users/abdullahasif/Documents/University/Sem_6/dl/proj/FloW_IMG/test/annotations/000800.xml
# Create labels for all images in train/val files
for split in ['garbage_train.txt', 'garbage_val.txt']:
    with open(os.path.join(image_sets_dir, split)) as f:
        ids = f.read().strip().split()

    for image_id in ids:
        xml_path = os.path.join(voc_annotations, f"{image_id}.xml")
        label_path = os.path.join(yolo_labels, f"{image_id}.txt")
        convert_annotation(xml_path, label_path)
