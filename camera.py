from jetbot import Camera, bgr8_to_jpeg
import traitlets
import ipywidgets.widgets as widgets

camera = Camera.instance(width=224, height=224)
image = widgets.Image(format='jpeg', width=224, hight=1)

camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)
