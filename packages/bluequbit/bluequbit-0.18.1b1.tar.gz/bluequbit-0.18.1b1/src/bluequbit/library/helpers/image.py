import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def load_image(image_path):
    """
    Load an image from the specified path using PIL

    Parameters:
        image_path (str): Path to the image file

    Returns:
        numpy.ndarray: The loaded image as a numpy array
    """
    pil_image = Image.open(image_path)
    return np.array(pil_image)


def convert_to_grayscale(image):
    """
    Convert an image to grayscale using PIL

    Parameters:
        image (numpy.ndarray): Input RGB image as numpy array

    Returns:
        numpy.ndarray: Grayscale version of the input image
    """
    pil_image = Image.fromarray(np.uint8(image))

    if pil_image.mode != "L":
        pil_image = pil_image.convert("L")

    return np.array(pil_image)


def reshape_image(image, target_height, target_width, keep_aspect_ratio=True):
    """
    Reshape an image to target dimensions using PIL

    Parameters:
        image (numpy.ndarray): Input image as numpy array
        target_height (int): Target height
        target_width (int): Target width
        keep_aspect_ratio (bool): Whether to maintain aspect ratio

    Returns:
        numpy.ndarray: Reshaped image
    """
    pil_image = Image.fromarray(np.uint8(image))

    if keep_aspect_ratio:
        img_width, img_height = pil_image.size
        r = min(target_height / img_height, target_width / img_width)

        new_height = int(img_height * r)
        new_width = int(img_width * r)

        resized = pil_image.resize((new_width, new_height), Image.LANCZOS)

        if pil_image.mode == "L":
            new_image = Image.new("L", (target_width, target_height), 0)
        else:
            new_image = Image.new("RGB", (target_width, target_height), (0, 0, 0))

        y_offset = (target_height - new_height) // 2
        x_offset = (target_width - new_width) // 2

        new_image.paste(resized, (x_offset, y_offset))
        return np.array(new_image)
    resized = pil_image.resize((target_width, target_height), Image.LANCZOS)
    return np.array(resized)


def normalize_image(image):
    """
    Normalize image pixel values to range [0, 1]

    Parameters:
        image (numpy.ndarray): Input image

    Returns:
        numpy.ndarray: Normalized image
    """
    return image.astype(np.float32) / 255.0


def display_image(image, title="Image"):
    """
    Display an image using matplotlib

    Parameters:
        image (numpy.ndarray): Image to display
        title (str): Title for the plot
    """
    if len(image.shape) == 3:
        plt.imshow(image)
    else:
        plt.imshow(image, cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.show()
