Author -
Md Istiak Tanvir (eruddro@gmail.com)
Asma Akter (asmaul9377@gmail.com)


Overview -

image-sharpner is a lightweight and efficient image enhancement library designed to improve edge clarity, restore fine textures, and enhance visual details through an adaptive multi-frequency sharpening technique.
The package supports both grayscale and color images and works seamlessly with popular computer vision pipelines.

Key Features -

1. Adaptive multi-frequency sharpening to enhance details without amplifying noise
2. Preserves natural textures and avoids halo artifacts
3. Works with underwater, low-light, and blurred images
4. Fast, NumPy-based implementation compatible with OpenCV
5. Easy integration into machine learning, deep learning, and image-processing workflows

Why Use This Package?
Traditional sharpening filters often overshoot edges, create ringing artifacts, or boost noise in smooth regions.


Installation -

pip install image-sharpner

Usage Example -

from image_prep  import image_sharpner



#Insert Image path -

image_sharpner('abc.jpg')





Supported Image Types -
jpg/png/jpeg/webmp

Compatibility -
Python 3.7+
NumPy
OpenCV


License - MIT License