# sd-webui-pixelart
![Cover](examples/cover.png)
Extension for [Automatic1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that pixelize images.

## Installation
1. Go to "Extensions" tab
2. Switch to "Install from url"
3. Paste `https://github.com/mrreplicart/sd-webui-pixelart` to the "URL for extension's git repository" field and click "Install" button
4. After installation is complete, go to "Installed" tab and click "Apply and restart UI"

## Usage
This extension can be found both in txt2img/img2img and extras.
If you would like to process image right after generation you can use "Pixel art" script in txt2img/img2img. Or you can click "Send to extras" button and play with settings and process your images in extras tab.

Check "Enable" in script section and also check "Enable" for exact tab (color, grayscale, black and white or custom palette)  
**Downscale** - image downscale factor, for example 512x512 image with downscale set to 2 become 256x256.  
**Rescale to original size** - rescales image back to original size after downscale and color correction.  

### Color
![Color tab interface](examples/color_tab.png)

**Palette Size** - number of colors

<details>
  <summary>Palette size examples</summary>

  ![Color limit example 1](examples/color_human.png)
  ![Color limit example 2](examples/color_item.png)
  ![Color limit example 3](examples/color_landscape.png)
</details>

**Colors quantization method** - different algorithms to get colors from image

<details>
  <summary>Quantization examples</summary>

  ![Quantization example 1](examples/quantization_human.png)
  ![Quantization example 2](examples/quantization_item.png)
  ![Quantization example 3](examples/quantization_landscape.png)
</details>

**Colors dither method** - different methods to represent colors with limited color palette

<details>
  <summary>Dither examples</summary>

  ![Dither example 1](examples/dither_human.png)
  ![Dither example 2](examples/dither_item.png)
  ![Dither example 3](examples/dither_landscape.png)
</details>

**Enable k-means for color quantization** - in most cases picks better colors

<details>
  <summary>K-means examples</summary>

  ![K-means example 1](examples/kmeans_human.png)
  ![K-means example 2](examples/kmeans_item.png)
  ![K-means example 3](examples/kmeans_landscape.png)
</details>


### Grayscale
![Grayscale tab interface](examples/grayscale_tab.png)
Same as color tab, but instead of colors we work with shades of gray

<details>
  <summary>Grayscale examples</summary>

  ![Grayscale example 1](examples/grayscale_human.png)
  ![Grayscale example 2](examples/grayscale_item.png)
  ![Grayscale example 3](examples/grayscale_landscape.png)
</details>

### Black and white
![Black and white tab interface](examples/bw_tab.png)
Simple black and white mode

**Threshold** - value that determens when we paint pixel black or white
**Inverse** - inverse colors

<details>
  <summary>Black and white</summary>

  ![Black and white example 1](examples/bw_human.png)
  ![Black and white example 2](examples/bw_item.png)
  ![Black and white example 3](examples/bw_landscape.png)
</details>

### Custom color palette
![Custom color palette tab interface](examples/custom_palette_tab.png)
This mode allows to paint image with colors from another image. If palette included in image, like palettes from [lospec]([url](https://lospec.com/palette-list)), script will automatically apply it, overwise you can select palette size manually with **Palette Size (only for complex images)** slider.

https://github.com/mrreplicart/sd-webui-pixelart/assets/137555918/2ab3be33-3229-4eeb-8d01-65c231398e0d

<details>
  <summary>Custom palette examples</summary>

  ![Custom color palette example 1](examples/custom_palette_human.png)
  ![Custom color palette example 2](examples/custom_palette_item.png)
  ![Custom color palette example 3](examples/custom_palette_landscape.png)
</details>
