This package is a collection of utilities that I find myself using across the various projects I've worked on in the past. Some have been extracted from packages, some from blog posts / stack overflow solutions, and some my own. Wherever possible, I have cited the source. Please do let me know if I missed out

Enable math like operations for joining PIL Images

```python
from upyog.image import *

img1 = Image.open(...)
img2 = Image.open(...)

horizontal_join = img1 | img2
vertical_join = img1 // img2

```
To do this over a list of images, use:

```
img_join_horizontal(img_list)
img_join_vertical(img_list)
```
