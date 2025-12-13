from ..graph.node import Node
from ..graph.port import PortType, InputPort, OutputPort


class ClaudeVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ClaudeVision",
            category="media_processing",
            task_name="media_processing.claude_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="claude-sonnet-4-20250514",
                    options=[
                        {"value": "claude-opus-4-20250514-thinking", "label": "claude-opus-4-20250514-thinking"},
                        {"value": "claude-opus-4-20250514", "label": "claude-opus-4-20250514"},
                        {"value": "claude-sonnet-4-20250514-thinking", "label": "claude-sonnet-4-20250514-thinking"},
                        {"value": "claude-sonnet-4-20250514", "label": "claude-sonnet-4-20250514"},
                        {"value": "claude-3-7-sonnet-thinking", "label": "claude-3-7-sonnet-thinking"},
                        {"value": "claude-3-7-sonnet", "label": "claude-3-7-sonnet"},
                        {"value": "claude-3-5-sonnet", "label": "claude-3-5-sonnet"},
                        {"value": "claude-3-opus", "label": "claude-3-opus"},
                        {"value": "claude-3-sonnet", "label": "claude-3-sonnet"},
                        {"value": "claude-3-haiku", "label": "claude-3-haiku"},
                    ],
                ),
                "multiple_input": InputPort(
                    name="multiple_input",
                    port_type=PortType.CHECKBOX,
                    value=False,
                    has_tooltip=True,
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
                "reasoning_content": OutputPort(
                    name="reasoning_content",
                    port_type=PortType.TEXTAREA,
                    condition="fields_data.get('llm_model', '').endswith('-thinking')",
                    condition_python=lambda ports: ports["llm_model"].value.endswith("-thinking"),
                ),
            },
        )


class DeepseekVl(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="DeepseekVl",
            category="media_processing",
            task_name="media_processing.deepseek_vl",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="deepseek-vl2",
                    options=[
                        {"value": "deepseek-vl2", "label": "deepseek-vl2"},
                    ],
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )


class GeminiVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="GeminiVision",
            category="media_processing",
            task_name="media_processing.gemini_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="gemini-2.5-pro",
                    options=[
                        {"label": "gemini-2.5-pro", "value": "gemini-2.5-pro"},
                        {"label": "gemini-2.5-flash", "value": "gemini-2.5-flash"},
                    ],
                ),
                "multiple_input": InputPort(
                    name="multiple_input",
                    port_type=PortType.CHECKBOX,
                    value=False,
                    has_tooltip=True,
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )


class GlmVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="GlmVision",
            category="media_processing",
            task_name="media_processing.glm_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="glm-4v-plus",
                    options=[
                        {"value": "glm-4v", "label": "glm-4v"},
                        {"value": "glm-4v-plus", "label": "glm-4v-plus"},
                        {"value": "glm-4v-flash", "label": "glm-4v-flash"},
                    ],
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )


class GptVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="GptVision",
            category="media_processing",
            task_name="media_processing.gpt_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="gpt-4o",
                    options=[
                        {"value": "gpt-4o", "label": "gpt-4o"},
                        {"value": "gpt-4o-mini", "label": "gpt-4o-mini"},
                        {"value": "o4-mini", "label": "o4-mini"},
                        {"value": "o4-mini-high", "label": "o4-mini-high"},
                        {"value": "gpt-4.1", "label": "gpt-4.1"},
                    ],
                ),
                "multiple_input": InputPort(
                    name="multiple_input",
                    port_type=PortType.CHECKBOX,
                    value=False,
                    has_tooltip=True,
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "detail_type": InputPort(
                    name="detail_type",
                    port_type=PortType.SELECT,
                    value="auto",
                    options=[
                        {"value": "auto", "label": "auto"},
                        {"value": "low", "label": "low"},
                        {"value": "high", "label": "high"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class InternVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="InternVision",
            category="media_processing",
            task_name="media_processing.intern_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="internvl2-26b",
                    options=[
                        {"value": "internvl2-26b", "label": "internvl2-26b"},
                        {"value": "internvl2-8b", "label": "internvl2-8b"},
                    ],
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )


class Ocr(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="Ocr",
            category="media_processing",
            task_name="media_processing.ocr",
            node_id=id,
            ports={
                "ocr_type": InputPort(
                    name="ocr_type",
                    port_type=PortType.SELECT,
                    value="general",
                    options=[
                        {"value": "general", "label": "general"},
                        {"value": "table", "label": "table"},
                        {"value": "business_license", "label": "business_license"},
                    ],
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output_table": OutputPort(
                    name="output_table",
                    condition="fields_data.get('ocr_type') == 'table'",
                    condition_python=lambda ports: ports["ocr_type"].value == "table",
                    has_tooltip=True,
                ),
                "output_content": OutputPort(
                    name="output_content",
                    condition="fields_data.get('ocr_type') in ['general', 'business_license']",
                    condition_python=lambda ports: ports["ocr_type"].value in ["general", "business_license"],
                ),
                "output_words_info": OutputPort(
                    name="output_words_info",
                    value=[],
                    condition="fields_data.get('ocr_type') in ['general', 'business_license']",
                    condition_python=lambda ports: ports["ocr_type"].value in ["general", "business_license"],
                    has_tooltip=True,
                ),
            },
        )


class QwenVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="QwenVision",
            category="media_processing",
            task_name="media_processing.qwen_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="qwen2.5-vl-72b-instruct",
                    options=[
                        {"value": "qvq-72b-preview", "label": "qvq-72b-preview"},
                        {"value": "qwen2.5-vl-72b-instruct", "label": "qwen2.5-vl-72b-instruct"},
                        {"value": "qwen2.5-vl-7b-instruct", "label": "qwen2.5-vl-7b-instruct"},
                        {"value": "qwen2.5-vl-3b-instruct", "label": "qwen2.5-vl-3b-instruct"},
                        {"value": "qwen2-vl-72b-instruct", "label": "qwen2-vl-72b-instruct"},
                        {"value": "qwen2-vl-7b-instruct", "label": "qwen2-vl-7b-instruct"},
                        {"value": "qwen-vl-max", "label": "qwen-vl-max"},
                        {"value": "qwen-vl-plus", "label": "qwen-vl-plus"},
                    ],
                ),
                "multiple_input": InputPort(
                    name="multiple_input",
                    port_type=PortType.CHECKBOX,
                    value=False,
                    has_tooltip=True,
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )


class SpeechRecognition(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="SpeechRecognition",
            category="media_processing",
            task_name="media_processing.speech_recognition",
            node_id=id,
            ports={
                "files_or_urls": InputPort(
                    name="files_or_urls",
                    port_type=PortType.RADIO,
                    value="files",
                    options=[
                        {"value": "files", "label": "files"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "files": InputPort(
                    name="files",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".wav", ".mp3", ".mp4", ".m4a", ".wma", ".aac", ".ogg", ".amr", ".flac"],
                    condition="fields_data.get('files_or_urls') == 'files'",
                    condition_python=lambda ports: ports["files_or_urls"].value == "files",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('files_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["files_or_urls"].value == "urls",
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="text",
                    options=[
                        {"value": "text", "label": "text"},
                        {"value": "list", "label": "list"},
                        {"value": "srt", "label": "srt"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class YiVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="YiVision",
            category="media_processing",
            task_name="media_processing.yi_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="yi-vision-v2",
                    options=[
                        {"value": "yi-vision-v2", "label": "yi-vision-v2"},
                    ],
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )


class MoonshotVision(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="MoonshotVision",
            category="media_processing",
            task_name="media_processing.moonshot_vision",
            node_id=id,
            ports={
                "text_prompt": InputPort(
                    name="text_prompt",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "llm_model": InputPort(
                    name="llm_model",
                    port_type=PortType.SELECT,
                    value="moonshot-v1-8k-vision-preview",
                    options=[
                        {"value": "moonshot-v1-8k-vision-preview", "label": "moonshot-v1-8k-vision-preview"},
                        {"value": "moonshot-v1-32k-vision-preview", "label": "moonshot-v1-32k-vision-preview"},
                        {"value": "moonshot-v1-128k-vision-preview", "label": "moonshot-v1-128k-vision-preview"},
                    ],
                ),
                "images_or_urls": InputPort(
                    name="images_or_urls",
                    port_type=PortType.RADIO,
                    value="images",
                    options=[
                        {"value": "images", "label": "images"},
                        {"value": "urls", "label": "urls"},
                    ],
                ),
                "images": InputPort(
                    name="images",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    support_file_types=[".jpg", ".jpeg", ".png", ".webp"],
                    condition="fields_data.get('images_or_urls') == 'images'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "images",
                    show=True,
                ),
                "urls": InputPort(
                    name="urls",
                    port_type=PortType.TEXT,
                    value="",
                    condition="fields_data.get('images_or_urls') == 'urls'",
                    condition_python=lambda ports: ports["images_or_urls"].value == "urls",
                ),
                "output": OutputPort(),
            },
        )
