from PIL import Image

# https://pillow.readthedocs.io/en/stable/reference/Image.html#dither-modes
DITHER_METHODS = {
    "None": Image.Dither.NONE,
    "Floyd-Steinberg": Image.Dither.FLOYDSTEINBERG
}

#https://pillow.readthedocs.io/en/stable/reference/Image.html#quantization-methods
QUANTIZATION_METHODS = {
    "Median cut": Image.Quantize.MEDIANCUT,
    "Maximum coverage": Image.Quantize.MAXCOVERAGE,
    "Fast octree": Image.Quantize.FASTOCTREE,
    "libimagequant": Image.Quantize.LIBIMAGEQUANT
}


def downscale_image(image: Image, scale: int) -> Image:
    width, height = image.size
    downscaled_image = image.resize((int(width / scale), int(height / scale)), Image.NEAREST)
    return downscaled_image


def resize_image(image: Image, size) -> Image:
    width, height = size
    resized_image = image.resize((width, height), Image.NEAREST)
    return resized_image


def limit_colors(
        image,
        limit: int=16,
        palette=None,
        palette_colors: int=256,
        quantize: Image.Quantize=Image.Quantize.MEDIANCUT,
        dither: Image.Dither=Image.Dither.NONE,
        use_k_means: bool=False
    ):
    if use_k_means:
        k_means_value = limit
    else:
        k_means_value = 0

    if palette:
        palette_image = palette
        ppalette = palette.getcolors()
        if ppalette:
            color_palette = palette.quantize(colors=len(list(set(ppalette))))
        else:
            colors = len(palette_image.getcolors()) if palette_image.getcolors() else palette_colors
            color_palette = palette_image.quantize(colors, kmeans=colors)
    else:
        # we need to get palette from image, because
        # dither in quantize doesn't work without it
        # https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#Image.quantize
        color_palette = image.quantize(colors=limit, kmeans=k_means_value, method=quantize, dither=Image.Dither.NONE)

    new_image = image.quantize(palette=color_palette, dither=dither)

    return new_image


def convert_to_grayscale(image):
    new_image = image.convert("L")
    return new_image.convert("RGB")


def convert_to_black_and_white(image: Image, threshold: int=128, is_inversed: bool=False):
    if is_inversed:
        apply_threshold = lambda x : 255 if x < threshold else 0
    else:
        apply_threshold = lambda x : 255 if x > threshold else 0

    black_and_white_image = image.convert('L', dither=Image.Dither.NONE).point(apply_threshold, mode='1')
    return black_and_white_image.convert("RGB")
