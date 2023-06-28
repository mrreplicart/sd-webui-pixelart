import gradio as gr
from PIL import features

from modules import scripts_postprocessing
from modules.shared import opts

from sd_webui_pixelart.utils import DITHER_METHODS, QUANTIZATION_METHODS, downscale_image, limit_colors, resize_image, convert_to_grayscale, convert_to_black_and_white


class ScriptPostprocessingUpscale(scripts_postprocessing.ScriptPostprocessing):
    name = "Pixel art"
    order = 20005
    model = None

    def ui(self):
        quantization_methods = ['Median cut', 'Maximum coverage', 'Fast octree']
        dither_methods = ['None', 'Floyd-Steinberg']

        if features.check_feature("libimagequant"):
            quantization_methods.insert(0, "libimagequant")

        with gr.Blocks():
            with gr.Accordion(label="Pixel art", open=False):
                enabled = gr.Checkbox(label="Enable", value=False)
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
                            black_and_white = gr.Checkbox(label="Enable", value=False)
                            inversed_black_and_white = gr.Checkbox(label="Inverse", value=False)
                        with gr.Row():
                            black_and_white_threshold = gr.Slider(label="Threshold", minimum=1, maximum=256, step=1, value=128)
                    with gr.TabItem("Custom color palette"):
                        use_color_palette = gr.Checkbox(label="Enable", value=False)
                        palette_image=gr.Image(label="Color palette image", type="pil")
                        palette_colors = gr.Slider(label="Palette Size (only for complex images)", minimum=1, maximum=256, step=1, value=16)
                        dither_method_palette = gr.Radio(choices=dither_methods, value=dither_methods[0], label='Colors dither method')

        return {
            "enabled": enabled,

            "downscale": downscale,
            "need_rescale": need_rescale,

            "enable_color_limit": enable_color_limit,
            "number_of_colors": number_of_colors,
            "quantization_method": quantization_method,
            "dither_method": dither_method,
            "use_k_means": use_k_means,

            "is_grayscale": is_grayscale,
            "number_of_shades": number_of_shades,
            "quantization_method_grayscale": quantization_method_grayscale,
            "dither_method_grayscale": dither_method_grayscale,
            "use_k_means_grayscale": use_k_means_grayscale,

            "use_color_palette": use_color_palette,
            "palette_image": palette_image,
            "palette_colors": palette_colors,
            "dither_method_palette": dither_method_palette,

            "black_and_white": black_and_white,
            "inversed_black_and_white": inversed_black_and_white,
            "black_and_white_threshold": black_and_white_threshold,
        }


    def process(
            self,
            pp: scripts_postprocessing.PostprocessedImage,

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

            use_color_palette,
            palette_image,
            palette_colors,
            dither_method_palette,

            black_and_white,
            inversed_black_and_white,
            black_and_white_threshold
        ):
        dither = DITHER_METHODS[dither_method]
        quantize = QUANTIZATION_METHODS[quantization_method]
        dither_grayscale = DITHER_METHODS[dither_method_grayscale]
        quantize_grayscale = QUANTIZATION_METHODS[quantization_method_grayscale]
        dither_palette = DITHER_METHODS[dither_method_palette]

        if not enabled:
            return

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

            if black_and_white:
                new_image = convert_to_black_and_white(new_image, black_and_white_threshold, inversed_black_and_white)

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

        pp.image = process_image(pp.image)
