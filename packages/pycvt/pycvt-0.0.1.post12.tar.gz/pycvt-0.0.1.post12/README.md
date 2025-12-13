# pycvt



## Install

```
pip install pycvt --upgrade
```

## dev

``` 
uv sync
```


## API List

- [draw_bounding_boxes](pycvt/vision/plot_boxes.py)
  > Draw bounding boxes on an image. 
  > Supports both single and multiple boxes, with options for labels and colors.

- [getcolor](pycvt/clolors/colors.py)
  > get a color by key


- **yolo annotations**
  - [load_yolo_annotations](./pycvt/annotations/yolo.py)
    > Load YOLO format annotations from a file.
  - [save_yolo_annotations](./pycvt/annotations/yolo.py)
    > Save annotations in YOLO format to a file.