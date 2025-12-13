from ..graph.node import Node
from ..graph.port import PortType, InputPort, OutputPort


class AudioEditing(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="AudioEditing",
            category="media_editing",
            task_name="media_editing.audio_editing",
            node_id=id,
            ports={
                "input_audio": InputPort(
                    name="input_audio",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".mp3", ".wav", ".ogg", ".m4a"],
                    multiple=True,
                    show=True,
                ),
                "audio_processing_logic": InputPort(
                    name="audio_processing_logic",
                    port_type=PortType.SELECT,
                    value="process_each",
                    options=[
                        {"value": "process_each", "label": "process_each"},
                        {"value": "mix", "label": "mix"},
                        {"value": "concat", "label": "concat"},
                    ],
                ),
                "trim": InputPort(
                    name="trim",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "trim_method": InputPort(
                    name="trim_method",
                    port_type=PortType.SELECT,
                    value="start_duration",
                    options=[
                        {"value": "start_duration", "label": "start_duration"},
                        {"value": "end_duration", "label": "end_duration"},
                        {"value": "start_end_time", "label": "start_end_time"},
                    ],
                    condition="return fieldsData.trim.value",
                    condition_python=lambda ports: ports["trim"].value,
                ),
                "trim_length": InputPort(
                    name="trim_length",
                    port_type=PortType.NUMBER,
                    value=0,
                    condition="return fieldsData.trim.value && (fieldsData.trim_method.value === 'start_duration' || fieldsData.trim_method.value === 'end_duration')",
                    condition_python=lambda ports: ports["trim"].value and (ports["trim_method"].value == "start_duration" or ports["trim_method"].value == "end_duration"),
                ),
                "trim_start_time": InputPort(
                    name="trim_start_time",
                    port_type=PortType.INPUT,
                    value="00:00:00",
                    condition="return fieldsData.trim.value && fieldsData.trim_method.value === 'start_end_time'",
                    condition_python=lambda ports: ports["trim"].value and ports["trim_method"].value == "start_end_time",
                ),
                "trim_end_time": InputPort(
                    name="trim_end_time",
                    port_type=PortType.INPUT,
                    value="00:01:00",
                    condition="return fieldsData.trim.value && fieldsData.trim_method.value === 'start_end_time'",
                    condition_python=lambda ports: ports["trim"].value and ports["trim_method"].value == "start_end_time",
                ),
                "adjust_volume": InputPort(
                    name="adjust_volume",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "volume_adjustment_ratio": InputPort(
                    name="volume_adjustment_ratio",
                    port_type=PortType.NUMBER,
                    value=1.0,
                    condition="return fieldsData.adjust_volume.value",
                    condition_python=lambda ports: ports["adjust_volume"].value,
                ),
                "fade_in_out": InputPort(
                    name="fade_in_out",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "fade_in_out_duration": InputPort(
                    name="fade_in_out_duration",
                    port_type=PortType.NUMBER,
                    value=1,
                    condition="return fieldsData.fade_in_out.value",
                    condition_python=lambda ports: ports["fade_in_out"].value,
                ),
                "adjust_speed": InputPort(
                    name="adjust_speed",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "speed_adjustment_method": InputPort(
                    name="speed_adjustment_method",
                    port_type=PortType.SELECT,
                    value="specified_speed",
                    options=[
                        {"value": "specified_speed", "label": "specified_speed"},
                        {"value": "specified_final_length", "label": "specified_final_length"},
                    ],
                    condition="return fieldsData.adjust_speed.value",
                    condition_python=lambda ports: ports["adjust_speed"].value,
                ),
                "specified_speed": InputPort(
                    name="specified_speed",
                    port_type=PortType.NUMBER,
                    value=1.0,
                    condition="return fieldsData.adjust_speed.value && fieldsData.speed_adjustment_method.value === 'specified_speed'",
                    condition_python=lambda ports: ports["adjust_speed"].value and ports["speed_adjustment_method"].value == "specified_speed",
                ),
                "specified_final_length": InputPort(
                    name="specified_final_length",
                    port_type=PortType.NUMBER,
                    value=10,
                    condition="return fieldsData.adjust_speed.value && fieldsData.speed_adjustment_method.value === 'specified_final_length'",
                    condition_python=lambda ports: ports["adjust_speed"].value and ports["speed_adjustment_method"].value == "specified_final_length",
                ),
                "adjust_channels": InputPort(
                    name="adjust_channels",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "channel_adjustment_method": InputPort(
                    name="channel_adjustment_method",
                    port_type=PortType.SELECT,
                    value="stereo_to_mono",
                    options=[
                        {"value": "stereo_to_mono", "label": "stereo_to_mono"},
                        {"value": "mono_to_stereo", "label": "mono_to_stereo"},
                    ],
                    condition="return fieldsData.adjust_channels.value",
                    condition_python=lambda ports: ports["adjust_channels"].value,
                ),
                "output_audio_format": InputPort(
                    name="output_audio_format",
                    port_type=PortType.SELECT,
                    value="mp3",
                    options=[
                        {"value": "mp3", "label": "mp3"},
                        {"value": "wav", "label": "wav"},
                        {"value": "m4a", "label": "m4a"},
                    ],
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class ImageBackgroundRemoval(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ImageBackgroundRemoval",
            category="media_editing",
            task_name="media_editing.image_background_removal",
            node_id=id,
            ports={
                "input_image": InputPort(
                    name="input_image",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    multiple=True,
                    show=True,
                ),
                "remove_background_method": InputPort(
                    name="remove_background_method",
                    port_type=PortType.SELECT,
                    value="accurate",
                    options=[
                        {"value": "fast", "label": "fast"},
                        {"value": "accurate", "label": "accurate"},
                        {"value": "portrait", "label": "portrait"},
                        {"value": "birefnet", "label": "birefnet"},
                    ],
                ),
                "transparent_background": InputPort(
                    name="transparent_background",
                    port_type=PortType.CHECKBOX,
                    value=True,
                ),
                "background_color": InputPort(
                    name="background_color",
                    port_type=PortType.INPUT,
                    value="#ffffff",
                    condition="return !fieldsData.transparent_background.value",
                    condition_python=lambda ports: not ports["transparent_background"].value,
                ),
                "crop_to_subject": InputPort(
                    name="crop_to_subject",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class ImageEditing(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ImageEditing",
            category="media_editing",
            task_name="media_editing.image_editing",
            node_id=id,
            ports={
                "input_image": InputPort(
                    name="input_image",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    multiple=True,
                    show=True,
                ),
                "crop": InputPort(
                    name="crop",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "crop_method": InputPort(
                    name="crop_method",
                    port_type=PortType.SELECT,
                    value="proportional",
                    options=[
                        {"value": "proportional", "label": "proportional"},
                        {"value": "fixed", "label": "fixed"},
                    ],
                    condition="return fieldsData.crop.value",
                    condition_python=lambda ports: ports["crop"].value,
                ),
                "crop_position": InputPort(
                    name="crop_position",
                    port_type=PortType.SELECT,
                    value="center",
                    options=[
                        {"value": "center", "label": "center"},
                        {"value": "top_left", "label": "top_left"},
                        {"value": "top", "label": "top"},
                        {"value": "top_right", "label": "top_right"},
                        {"value": "right", "label": "right"},
                        {"value": "bottom_right", "label": "bottom_right"},
                        {"value": "bottom", "label": "bottom"},
                        {"value": "bottom_left", "label": "bottom_left"},
                        {"value": "left", "label": "left"},
                        {"value": "absolute", "label": "absolute"},
                    ],
                    condition="return fieldsData.crop.value",
                    condition_python=lambda ports: ports["crop"].value,
                ),
                "crop_x": InputPort(
                    name="crop_x",
                    port_type=PortType.NUMBER,
                    value=1,
                    condition="return fieldsData.crop_position.value == 'absolute' && fieldsData.crop.value",
                    condition_python=lambda ports: ports["crop_position"].value == "absolute" and ports["crop"].value,
                ),
                "crop_y": InputPort(
                    name="crop_y",
                    port_type=PortType.NUMBER,
                    value=1,
                    condition="return fieldsData.crop_position.value == 'absolute' && fieldsData.crop.value",
                    condition_python=lambda ports: ports["crop_position"].value == "absolute" and ports["crop"].value,
                ),
                "crop_width": InputPort(
                    name="crop_width",
                    port_type=PortType.NUMBER,
                    value=300,
                    condition="return fieldsData.crop.value && fieldsData.crop_method.value == 'fixed'",
                    condition_python=lambda ports: ports["crop"].value and ports["crop_method"].value == "fixed",
                ),
                "crop_height": InputPort(
                    name="crop_height",
                    port_type=PortType.NUMBER,
                    value=300,
                    condition="return fieldsData.crop.value && fieldsData.crop_method.value == 'fixed'",
                    condition_python=lambda ports: ports["crop"].value and ports["crop_method"].value == "fixed",
                ),
                "crop_width_ratio": InputPort(
                    name="crop_width_ratio",
                    port_type=PortType.NUMBER,
                    value=1,
                    condition="return fieldsData.crop.value && fieldsData.crop_method.value == 'proportional'",
                    condition_python=lambda ports: ports["crop"].value and ports["crop_method"].value == "proportional",
                ),
                "crop_height_ratio": InputPort(
                    name="crop_height_ratio",
                    port_type=PortType.NUMBER,
                    value=1,
                    condition="return fieldsData.crop.value && fieldsData.crop_method.value == 'proportional'",
                    condition_python=lambda ports: ports["crop"].value and ports["crop_method"].value == "proportional",
                ),
                "scale": InputPort(
                    name="scale",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "scale_method": InputPort(
                    name="scale_method",
                    port_type=PortType.SELECT,
                    value="proportional_scale",
                    options=[
                        {"value": "proportional_scale", "label": "proportional_scale"},
                        {"value": "fixed_width_height", "label": "fixed_width_height"},
                    ],
                    condition="return fieldsData.scale.value",
                    condition_python=lambda ports: ports["scale"].value,
                ),
                "scale_ratio": InputPort(
                    name="scale_ratio",
                    port_type=PortType.NUMBER,
                    value=1,
                    condition="return fieldsData.scale.value && fieldsData.scale_method.value == 'proportional_scale'",
                    condition_python=lambda ports: ports["scale"].value and ports["scale_method"].value == "proportional_scale",
                ),
                "scale_width": InputPort(
                    name="scale_width",
                    port_type=PortType.NUMBER,
                    value=0,
                    condition="return fieldsData.scale.value && fieldsData.scale_method.value == 'fixed_width_height'",
                    condition_python=lambda ports: ports["scale"].value and ports["scale_method"].value == "fixed_width_height",
                ),
                "scale_height": InputPort(
                    name="scale_height",
                    port_type=PortType.NUMBER,
                    value=0,
                    condition="return fieldsData.scale.value && fieldsData.scale_method.value == 'fixed_width_height'",
                    condition_python=lambda ports: ports["scale"].value and ports["scale_method"].value == "fixed_width_height",
                ),
                "compress": InputPort(
                    name="compress",
                    port_type=PortType.NUMBER,
                    value=100,
                ),
                "rotate": InputPort(
                    name="rotate",
                    port_type=PortType.NUMBER,
                    value=0,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class ImageSegmentation(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ImageSegmentation",
            category="media_editing",
            task_name="media_editing.image_segmentation",
            node_id=id,
            ports={
                "input_image": InputPort(
                    name="input_image",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    multiple=True,
                    show=True,
                ),
                "selection_method": InputPort(
                    name="selection_method",
                    port_type=PortType.SELECT,
                    value="prompt",
                    options=[
                        {"value": "prompt", "label": "prompt"},
                        {"value": "coordinates", "label": "coordinates"},
                    ],
                ),
                "prompt": InputPort(
                    name="prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                    condition="return fieldsData.selection_method.value === 'prompt'",
                    condition_python=lambda ports: ports["selection_method"].value == "prompt",
                ),
                "coordinates": InputPort(
                    name="coordinates",
                    port_type=PortType.TEXTAREA,
                    value="",
                    condition="return fieldsData.selection_method.value === 'coordinates'",
                    condition_python=lambda ports: ports["selection_method"].value == "coordinates",
                ),
                "remove_coordinates": InputPort(
                    name="remove_coordinates",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "overlay_mask": InputPort(
                    name="overlay_mask",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class ImageWatermark(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ImageWatermark",
            category="media_editing",
            task_name="media_editing.image_watermark",
            node_id=id,
            ports={
                "input_image": InputPort(
                    name="input_image",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    multiple=True,
                    show=True,
                ),
                "image_or_text": InputPort(
                    name="image_or_text",
                    port_type=PortType.SELECT,
                    value="text",
                    options=[
                        {"value": "text", "label": "text"},
                        {"value": "image", "label": "image"},
                    ],
                ),
                "watermark_image": InputPort(
                    name="watermark_image",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="return fieldsData.image_or_text.value == 'image'",
                    condition_python=lambda ports: ports["image_or_text"].value == "image",
                ),
                "watermark_image_width_ratio": InputPort(
                    name="watermark_image_width_ratio",
                    port_type=PortType.NUMBER,
                    value=0.3,
                    condition="return fieldsData.image_or_text.value == 'image'",
                    condition_python=lambda ports: ports["image_or_text"].value == "image",
                ),
                "watermark_image_height_ratio": InputPort(
                    name="watermark_image_height_ratio",
                    port_type=PortType.NUMBER,
                    value=0,
                    condition="return fieldsData.image_or_text.value == 'image'",
                    condition_python=lambda ports: ports["image_or_text"].value == "image",
                ),
                "watermark_text": InputPort(
                    name="watermark_text",
                    port_type=PortType.TEXTAREA,
                    value="",
                    condition="return fieldsData.image_or_text.value == 'text'",
                    condition_python=lambda ports: ports["image_or_text"].value == "text",
                ),
                "watermark_text_font": InputPort(
                    name="watermark_text_font",
                    port_type=PortType.SELECT,
                    value="source_han_sans_sc",
                    options=[
                        {"value": "source_han_sans_sc", "label": "source_han_sans_sc"},
                        {"value": "source_han_sans_tc", "label": "source_han_sans_tc"},
                        {"value": "source_han_sans_jp", "label": "source_han_sans_jp"},
                        {"value": "source_han_sans_kr", "label": "source_han_sans_kr"},
                        {"value": "you_she_biao_ti_hei", "label": "you_she_biao_ti_hei"},
                        {"value": "zi_hun_bian_tao_ti", "label": "zi_hun_bian_tao_ti"},
                        {"value": "ckt_king_kong", "label": "ckt_king_kong"},
                        {"value": "douyin_sans", "label": "douyin_sans"},
                        {"value": "alimama_dong_fang_da_kai", "label": "alimama_dong_fang_da_kai"},
                        {"value": "inter", "label": "inter"},
                        {"value": "custom", "label": "custom"},
                    ],
                    condition="return fieldsData.image_or_text.value == 'text'",
                    condition_python=lambda ports: ports["image_or_text"].value == "text",
                ),
                "watermark_text_font_custom": InputPort(
                    name="watermark_text_font_custom",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".otf", ".ttf", ".ttc", ".otc"],
                    condition="return fieldsData.image_or_text.value == 'text' && fieldsData.watermark_text_font.value == 'custom'",
                    condition_python=lambda ports: ports["image_or_text"].value == "text" and ports["watermark_text_font"].value == "custom",
                ),
                "watermark_text_font_size": InputPort(
                    name="watermark_text_font_size",
                    port_type=PortType.NUMBER,
                    value=20,
                    condition="return fieldsData.image_or_text.value == 'text'",
                    condition_python=lambda ports: ports["image_or_text"].value == "text",
                ),
                "watermark_text_font_color": InputPort(
                    name="watermark_text_font_color",
                    port_type=PortType.INPUT,
                    value="#ffffff",
                    condition="return fieldsData.image_or_text.value == 'text'",
                    condition_python=lambda ports: ports["image_or_text"].value == "text",
                ),
                "opacity": InputPort(
                    name="opacity",
                    port_type=PortType.NUMBER,
                    value=0.8,
                ),
                "position": InputPort(
                    name="position",
                    port_type=PortType.SELECT,
                    value="bottom_right",
                    options=[
                        {"value": "center", "label": "center"},
                        {"value": "top_left", "label": "top_left"},
                        {"value": "top", "label": "top"},
                        {"value": "top_right", "label": "top_right"},
                        {"value": "right", "label": "right"},
                        {"value": "bottom_right", "label": "bottom_right"},
                        {"value": "bottom", "label": "bottom"},
                        {"value": "bottom_left", "label": "bottom_left"},
                        {"value": "left", "label": "left"},
                    ],
                ),
                "vertical_gap": InputPort(
                    name="vertical_gap",
                    port_type=PortType.NUMBER,
                    value=10,
                ),
                "horizontal_gap": InputPort(
                    name="horizontal_gap",
                    port_type=PortType.NUMBER,
                    value=10,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class VideoEditing(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="VideoEditing",
            category="media_editing",
            task_name="media_editing.video_editing",
            node_id=id,
            ports={
                "input_video": InputPort(
                    name="input_video",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=["video/*"],
                    multiple=True,
                    show=True,
                ),
                "video_processing_logic": InputPort(
                    name="video_processing_logic",
                    port_type=PortType.SELECT,
                    value="process_each",
                    options=[
                        {"value": "process_each", "label": "process_each"},
                        {"value": "merge", "label": "merge"},
                    ],
                ),
                "trim_video": InputPort(
                    name="trim_video",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "trim_start_time": InputPort(
                    name="trim_start_time",
                    port_type=PortType.INPUT,
                    value="00:00:00",
                    condition="return fieldsData.trim_video.value",
                    condition_python=lambda ports: ports["trim_video"].value,
                ),
                "trim_end_time": InputPort(
                    name="trim_end_time",
                    port_type=PortType.INPUT,
                    value="00:01:00",
                    condition="return fieldsData.trim_video.value",
                    condition_python=lambda ports: ports["trim_video"].value,
                ),
                "rotate_video": InputPort(
                    name="rotate_video",
                    port_type=PortType.SELECT,
                    value=0,
                    options=[
                        {"value": 0, "label": "0"},
                        {"value": 90, "label": "90"},
                        {"value": 180, "label": "180"},
                        {"value": 270, "label": "270"},
                    ],
                ),
                "add_watermark": InputPort(
                    name="add_watermark",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "watermark_text": InputPort(
                    name="watermark_text",
                    port_type=PortType.INPUT,
                    value="",
                    condition="return fieldsData.add_watermark.value",
                    condition_python=lambda ports: ports["add_watermark"].value,
                ),
                "output_video_format": InputPort(
                    name="output_video_format",
                    port_type=PortType.SELECT,
                    value="mp4",
                    options=[
                        {"value": "mp4", "label": "mp4"},
                        {"value": "avi", "label": "avi"},
                        {"value": "mov", "label": "mov"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class VideoScreenshot(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="VideoScreenshot",
            category="media_editing",
            task_name="media_editing.video_screenshot",
            node_id=id,
            ports={
                "input_video": InputPort(
                    name="input_video",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=["video/*"],
                    multiple=True,
                    show=True,
                ),
                "screenshot_method": InputPort(
                    name="screenshot_method",
                    port_type=PortType.SELECT,
                    value="interval",
                    options=[
                        {"value": "interval", "label": "interval"},
                        {"value": "timestamps", "label": "timestamps"},
                    ],
                ),
                "screenshot_interval": InputPort(
                    name="screenshot_interval",
                    port_type=PortType.NUMBER,
                    value=10,
                    condition="return fieldsData.screenshot_method.value === 'interval'",
                    condition_python=lambda ports: ports["screenshot_method"].value == "interval",
                ),
                "screenshot_timestamps": InputPort(
                    name="screenshot_timestamps",
                    port_type=PortType.INPUT,
                    value="",
                    condition="return fieldsData.screenshot_method.value === 'timestamps'",
                    condition_python=lambda ports: ports["screenshot_method"].value == "timestamps",
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class FfmpegProcess(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="FfmpegProcess",
            category="media_editing",
            task_name="media_editing.ffmpeg_process",
            node_id=id,
            ports={
                "input_files": InputPort(
                    name="input_files",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[
                        ".mp4",
                        ".avi",
                        ".mov",
                        ".mkv",
                        ".mp3",
                        ".wav",
                        ".ogg",
                        ".m4a",
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".gif",
                        ".bmp",
                        ".webp",
                        ".webm",
                        ".flv",
                        ".wmv",
                        ".3gp",
                    ],
                    multiple=True,
                    required=True,
                    show=True,
                ),
                "ffmpeg_command": InputPort(
                    name="ffmpeg_command",
                    port_type=PortType.TEXTAREA,
                    value="",
                    required=True,
                    show=False,
                    has_tooltip=True,
                ),
                "output_filename": InputPort(
                    name="output_filename",
                    port_type=PortType.INPUT,
                    value="output.mp4",
                    required=False,
                    show=False,
                    has_tooltip=True,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "markdown", "label": "markdown"},
                        {"value": "html", "label": "html"},
                    ],
                    required=False,
                    show=False,
                    group="default",
                ),
                "output": OutputPort(
                    name="output",
                    required=True,
                    show=False,
                ),
                "output_error": OutputPort(
                    name="output_error",
                    required=True,
                    show=False,
                    has_tooltip=True,
                ),
            },
        )
