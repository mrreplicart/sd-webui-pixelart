import gradio as gr

import modules.scripts as scripts
from modules import images
from modules.shared import opts
from modules.ui_components import InputAccordion

from sd_webui_pixelart.utils import DITHER_METHODS, QUANTIZATION_METHODS, downscale_image, limit_colors, resize_image, convert_to_black_and_white, convert_to_grayscale

class Script(scripts.Script):
    def title(self):
        return "Pixel art"


    def show(self, is_img2img):
        return scripts.AlwaysVisible


    def ui(self, is_img2img):
        quantization_methods = ['Median cut', 'Maximum coverage', 'Fast octree']
        dither_methods = ['None', 'Floyd-Steinberg']

        with InputAccordion(False, label="Pixel art") as enabled:
            with gr.Column():
                with gr.Row():
                    downscale = gr.Slider(label="Downscale", minimum=1, maximum=32, step=2, value=8)
                    need_rescale = gr.Checkbox(label="Rescale to original size", value=True)
                with gr.Tabs():
                    with gr.TabItem("Color"):
                        enable_color_limit = gr.Checkbox(label="Enable", value=False)
                        number_of_colors = gr.Slider(label="Palette Size", minimum=1, maximum=256, step=1, value=16)
                        quantization_method = gr.Radio(choices=quantization_methods, value=quantization_methods[0], label='Colors quantization method')
                        dither_method = gr.Radio(choices=dither_methods, value=dither_methods[0], label='Colors dither method')
                        use_k_means = gr.Checkbox(label="Enable k-means for color quantization", value=True)
                    with gr.TabItem("Grayscale"):
                        is_grayscale = gr.Checkbox(label="Enable", value=False)
                        number_of_shades = gr.Slider(label="Palette Size", minimum=1, maximum=256, step=1, value=16)
                        quantization_method_grayscale = gr.Radio(choices=quantization_methods, value=quantization_methods[0], label='Colors quantization method')
                        dither_method_grayscale = gr.Radio(choices=dither_methods, value=dither_methods[0], label='Colors dither method')
                        use_k_means_grayscale = gr.Checkbox(label="Enable k-means for color quantization", value=True)
                    with gr.TabItem("Black and white"):
                        with gr.Row():
                            is_black_and_white = gr.Checkbox(label="Enable", value=False)
                            is_inversed_black_and_white = gr.Checkbox(label="Inverse", value=False)
                        with gr.Row():
                            black_and_white_threshold = gr.Slider(label="Threshold", minimum=1, maximum=256, step=1, value=128)
                    with gr.TabItem("Custom color palette"):
                        use_color_palette = gr.Checkbox(label="Enable", value=False)
                        palette_image=gr.Image(label="Color palette image", type="pil")
                        palette_colors = gr.Slider(label="Palette Size (only for complex images)", minimum=1, maximum=256, step=1, value=16)
                        dither_method_palette = gr.Radio(choices=dither_methods, value=dither_methods[0], label='Colors dither method')

        return [enabled, downscale, need_rescale, enable_color_limit, number_of_colors, quantization_method, dither_method, use_k_means, is_grayscale, number_of_shades, quantization_method_grayscale, dither_method_grayscale, use_k_means_grayscale, is_black_and_white, is_inversed_black_and_white, black_and_white_threshold, use_color_palette, palette_image, palette_colors, dither_method_palette]

    def postprocess(
        self,
        p,
        processed,
        enabled,

        downscale,
        need_rescale,

        enable_color_limit,
        number_of_colors,
        quantization_method,
        dither_method,
        use_k_means,

        is_grayscale,
        number_of_shades,
        quantization_method_grayscale,
        dither_method_grayscale,
        use_k_means_grayscale,

        is_black_and_white,
        is_inversed_black_and_white,
        black_and_white_threshold,

        use_color_palette,
        palette_image,
        palette_colors,
        dither_method_palette
    ):
        if not enabled:
            return

        dither = DITHER_METHODS[dither_method]
        quantize = QUANTIZATION_METHODS[quantization_method]
        dither_grayscale = DITHER_METHODS[dither_method_grayscale]
        quantize_grayscale = QUANTIZATION_METHODS[quantization_method_grayscale]
        dither_palette = DITHER_METHODS[dither_method_palette]

        def process_image(original_image):
            original_width, original_height = original_image.size

            if original_image.mode != "RGB":
                new_image = original_image.convert("RGB")
            else:
                new_image = original_image

            new_image = downscale_image(new_image, downscale)

            if use_color_palette:
                new_image = limit_colors(
                    image=new_image,
                    palette=palette_image,
                    palette_colors=palette_colors,
                    dither=dither_palette
                )

            if is_black_and_white:
                new_image = convert_to_black_and_white(new_image, black_and_white_threshold, is_inversed_black_and_white)

            if is_grayscale:
                new_image = convert_to_grayscale(new_image)
                new_image = limit_colors(
                    image=new_image,
                    limit=int(number_of_shades),
                    quantize=quantize_grayscale,
                    dither=dither_grayscale,
                    use_k_means=use_k_means_grayscale
                )

            if enable_color_limit:
                new_image = limit_colors(
                    image=new_image,
                    limit=int(number_of_colors),
                    quantize=quantize,
                    dither=dither,
                    use_k_means=use_k_means
                )

            if need_rescale:
                new_image = resize_image(new_image, (original_width, original_height))

            return new_image.convert('RGBA')

        for i in range(len(processed.images)):
            pixel_image = process_image(processed.images[i])
            processed.images.append(pixel_image)

            images.save_image(pixel_image, p.outpath_samples, "pixel",
            processed.seed + i, processed.prompt, opts.samples_format, info= processed.info, p=p)

        return processed
