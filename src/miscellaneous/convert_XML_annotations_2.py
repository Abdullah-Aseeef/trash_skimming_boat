import os
import xml.etree.ElementTree as ET

# paths (adjust as needed):
voc_annotations = '/Users/abdullahasif/Documents/University/Sem_6/dl/proj/FloW_IMG/test/annotations'
yolo_labels     = '/Users/abdullahasif/Documents/University/Sem_6/dl/proj/FloW_IMG/test/labels'

os.makedirs(yolo_labels, exist_ok=True)

def convert_annotation(xml_file, label_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(label_file, 'w') as out:
        for obj in root.findall('object'):
            cls_id = 0  # single class (garbage)
            bb = obj.find('bndbox')
            xmin = float(bb.find('xmin').text)
            ymin = float(bb.find('ymin').text)
            xmax = float(bb.find('xmax').text)
            ymax = float(bb.find('ymax').text)

            # normalize
            x_center = (xmin + xmax) / 2.0 / w
            y_center = (ymin + ymax) / 2.0 / h
            width    = (xmax - xmin) / w
            height   = (ymax - ymin) / h

            out.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# iterate over every XML in the annotations folder
for fname in os.listdir(voc_annotations):
    if not fname.lower().endswith('.xml'):
        continue

    xml_path   = os.path.join(voc_annotations, fname)
    label_name = os.path.splitext(fname)[0] + '.txt'
    label_path = os.path.join(yolo_labels, label_name)

    convert_annotation(xml_path, label_path)
    print(f"Converted {fname} → {label_name}")
