from ..graph.node import Node
from ..graph.port import PortType, InputPort, OutputPort


class CodebaseAnalysis(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="CodebaseAnalysis",
            category="tools",
            task_name="tools.codebase_analysis",
            node_id=id,
            ports={
                "input_type": InputPort(
                    name="input_type",
                    port_type=PortType.SELECT,
                    value="file",
                    options=[
                        {"value": "file", "label": "file"},
                        {"value": "git_url", "label": "git_url"},
                    ],
                ),
                "codebase_file": InputPort(
                    name="codebase_file",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".zip"],
                    multiple=False,
                    condition="return fieldsData.input_type.value === 'file'",
                    condition_python=lambda ports: ports["input_type"].value == "file",
                ),
                "git_url": InputPort(
                    name="git_url",
                    port_type=PortType.INPUT,
                    value="",
                    condition="return fieldsData.input_type.value === 'git_url'",
                    condition_python=lambda ports: ports["input_type"].value == "git_url",
                ),
                "output_style": InputPort(
                    name="output_style",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "plain", "label": "Plain Text"},
                        {"value": "xml", "label": "XML"},
                        {"value": "markdown", "label": "Markdown"},
                    ],
                ),
                "show_line_numbers": InputPort(
                    name="show_line_numbers",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "remove_comments": InputPort(
                    name="remove_comments",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "remove_empty_lines": InputPort(
                    name="remove_empty_lines",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "ignore_patterns": InputPort(
                    name="ignore_patterns",
                    port_type=PortType.INPUT,
                    value=[],
                    multiple=True,
                ),
                "output": OutputPort(),
            },
        )


class TextTranslation(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="TextTranslation",
            category="tools",
            task_name="tools.text_translation",
            node_id=id,
            ports={
                "text": InputPort(
                    name="text",
                    port_type=PortType.INPUT,
                    value="",
                    field_type="textarea",
                ),
                "from_language": InputPort(
                    name="from_language",
                    port_type=PortType.SELECT,
                    value="auto",
                    options=[
                        {"value": "ar", "label": "ar"},
                        {"value": "de", "label": "de"},
                        {"value": "en", "label": "en"},
                        {"value": "es", "label": "es"},
                        {"value": "fr", "label": "fr"},
                        {"value": "hi", "label": "hi"},
                        {"value": "id", "label": "id"},
                        {"value": "it", "label": "it"},
                        {"value": "ja", "label": "ja"},
                        {"value": "ko", "label": "ko"},
                        {"value": "nl", "label": "nl"},
                        {"value": "pt", "label": "pt"},
                        {"value": "ru", "label": "ru"},
                        {"value": "th", "label": "th"},
                        {"value": "vi", "label": "vi"},
                        {"value": "zh-CHS", "label": "zh-CHS"},
                        {"value": "zh-CHT", "label": "zh-CHT"},
                        {"value": "auto", "label": "auto"},
                    ],
                ),
                "to_language": InputPort(
                    name="to_language",
                    port_type=PortType.SELECT,
                    value="en",
                    options=[
                        {"value": "ar", "label": "ar"},
                        {"value": "de", "label": "de"},
                        {"value": "en", "label": "en"},
                        {"value": "es", "label": "es"},
                        {"value": "fr", "label": "fr"},
                        {"value": "hi", "label": "hi"},
                        {"value": "id", "label": "id"},
                        {"value": "it", "label": "it"},
                        {"value": "ja", "label": "ja"},
                        {"value": "ko", "label": "ko"},
                        {"value": "nl", "label": "nl"},
                        {"value": "pt", "label": "pt"},
                        {"value": "ru", "label": "ru"},
                        {"value": "th", "label": "th"},
                        {"value": "vi", "label": "vi"},
                        {"value": "zh-CHS", "label": "zh-CHS"},
                        {"value": "zh-CHT", "label": "zh-CHT"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class TextSearch(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="TextSearch",
            category="tools",
            task_name="tools.text_search",
            node_id=id,
            ports={
                "search_text": InputPort(
                    name="search_text",
                    port_type=PortType.INPUT,
                    value="",
                ),
                "search_engine": InputPort(
                    name="search_engine",
                    port_type=PortType.SELECT,
                    value="bing",
                    options=[
                        {"value": "bing", "label": "bing"},
                        {"value": "bochaai", "label": "bochaai"},
                        {"value": "exa.ai", "label": "exa.ai"},
                        {"value": "jina.ai", "label": "jina.ai"},
                        {"value": "zhipuai", "label": "zhipuai"},
                        {"value": "duckduckgo", "label": "duckduckgo"},
                    ],
                ),
                "result_category": InputPort(
                    name="result_category",
                    port_type=PortType.SELECT,
                    value="all",
                    options=[
                        {"value": "all", "label": "all"},
                        {"value": "company", "label": "company"},
                        {"value": "research_paper", "label": "research_paper"},
                        {"value": "news", "label": "news"},
                        {"value": "pdf", "label": "pdf"},
                        {"value": "github", "label": "github"},
                        {"value": "personal_site", "label": "personal_site"},
                        {"value": "linkedin_profile", "label": "linkedin_profile"},
                        {"value": "financial_report", "label": "financial_report"},
                    ],
                    condition="return fieldsData.search_engine.value === 'exa.ai'",
                    condition_python=lambda ports: ports["search_engine"].value == "exa.ai",
                ),
                "count": InputPort(
                    name="count",
                    port_type=PortType.NUMBER,
                    value=10,
                ),
                "offset": InputPort(
                    name="offset",
                    port_type=PortType.NUMBER,
                    value=0,
                ),
                "freshness": InputPort(
                    name="freshness",
                    port_type=PortType.SELECT,
                    value="all",
                    options=[
                        {"value": "all", "label": "all"},
                        {"value": "day", "label": "day"},
                        {"value": "week", "label": "week"},
                        {"value": "month", "label": "month"},
                        {"value": "custom", "label": "custom"},
                    ],
                    condition="return fieldsData.search_engine.value === 'bing'",
                    condition_python=lambda ports: ports["search_engine"].value == "bing",
                ),
                "custom_freshness": InputPort(
                    name="custom_freshness",
                    port_type=PortType.INPUT,
                    value="",
                    condition="return fieldsData.freshness.value === 'custom'",
                    condition_python=lambda ports: ports["freshness"].value == "custom",
                ),
                "combine_result_in_text": InputPort(
                    name="combine_result_in_text",
                    port_type=PortType.CHECKBOX,
                    value=True,
                ),
                "max_snippet_length": InputPort(
                    name="max_snippet_length",
                    port_type=PortType.NUMBER,
                    value=300,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "text", "label": "text"},
                        {"value": "markdown", "label": "markdown"},
                    ],
                ),
                "output_page_title": OutputPort(
                    name="output_page_title",
                    port_type=PortType.LIST,
                    condition="!fieldsData.combine_result_in_text.value",
                    condition_python=lambda ports: not ports["combine_result_in_text"].value,
                ),
                "output_page_url": OutputPort(
                    name="output_page_url",
                    port_type=PortType.LIST,
                    condition="!fieldsData.combine_result_in_text.value",
                    condition_python=lambda ports: not ports["combine_result_in_text"].value,
                ),
                "output_page_snippet": OutputPort(
                    name="output_page_snippet",
                    port_type=PortType.LIST,
                    condition="!fieldsData.combine_result_in_text.value",
                    condition_python=lambda ports: not ports["combine_result_in_text"].value,
                ),
                "output_combined": OutputPort(
                    name="output_combined",
                    port_type=PortType.LIST,
                    condition="!fieldsData.combine_result_in_text.value",
                    condition_python=lambda ports: not ports["combine_result_in_text"].value,
                ),
            },
        )


class ProgrammingFunction(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ProgrammingFunction",
            category="tools",
            task_name="tools.programming_function",
            node_id=id,
            ports={
                "language": InputPort(
                    name="language",
                    port_type=PortType.SELECT,
                    value="python",
                    options=[
                        {"value": "python", "label": "Python"},
                    ],
                ),
                "code": InputPort(
                    name="code",
                    port_type=PortType.INPUT,
                    value="",
                    field_type="textarea",
                ),
                "use_oversea_node": InputPort(
                    name="use_oversea_node",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "list_input": InputPort(
                    name="list_input",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "instance_type": InputPort(
                    name="instance_type",
                    port_type=PortType.SELECT,
                    value="light",
                    options=[
                        {"value": "light", "label": "light"},
                        {"value": "large", "label": "large"},
                    ],
                ),
                "output": OutputPort(
                    name="output",
                    port_type=PortType.INPUT,
                    field_type="textarea",
                ),
                "console_msg": OutputPort(
                    name="console_msg",
                    port_type=PortType.INPUT,
                    field_type="textarea",
                ),
                "error_msg": OutputPort(
                    name="error_msg",
                    port_type=PortType.INPUT,
                    field_type="textarea",
                ),
                "files": OutputPort(
                    name="files",
                    port_type=PortType.INPUT,
                    field_type="textarea",
                ),
            },
            can_add_input_ports=True,
        )


class ImageSearch(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="ImageSearch",
            category="tools",
            task_name="tools.image_search",
            node_id=id,
            ports={
                "search_text": InputPort(
                    name="search_text",
                    port_type=PortType.INPUT,
                    value="",
                ),
                "search_engine": InputPort(
                    name="search_engine",
                    port_type=PortType.SELECT,
                    value="bing",
                    options=[
                        {"value": "bing", "label": "bing"},
                        {"value": "pexels", "label": "pexels"},
                        {"value": "unsplash", "label": "unsplash"},
                    ],
                ),
                "count": InputPort(
                    name="count",
                    port_type=PortType.NUMBER,
                    value=5,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="markdown",
                    options=[
                        {"value": "text", "label": "text"},
                        {"value": "markdown", "label": "markdown"},
                    ],
                ),
                "output": OutputPort(
                    name="output",
                    port_type=PortType.LIST,
                ),
            },
        )


class WorkflowInvoke(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="WorkflowInvoke",
            category="tools",
            task_name="tools.workflow_invoke",
            node_id=id,
            ports={
                "workflow_id": InputPort(
                    name="workflow_id",
                    port_type=PortType.INPUT,
                    value="",
                ),
            },
        )
