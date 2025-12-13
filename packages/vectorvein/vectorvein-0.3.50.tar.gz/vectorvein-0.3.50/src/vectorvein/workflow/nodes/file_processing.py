from ..graph.node import Node
from ..graph.port import PortType, InputPort, OutputPort


class FileLoader(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="FileLoader",
            category="file_processing",
            task_name="file_processing.file_loader",
            node_id=id,
            ports={
                "files": InputPort(
                    name="files",
                    port_type=PortType.FILE,
                    value=[],
                    multiple=True,
                    show=True,
                ),
                "parse_quality": InputPort(
                    name="parse_quality",
                    port_type=PortType.SELECT,
                    value="default",
                    options=[
                        {"value": "default", "label": "default"},
                        {"value": "high", "label": "high"},
                    ],
                ),
                "remove_image": InputPort(
                    name="remove_image",
                    port_type=PortType.CHECKBOX,
                    value=True,
                    condition="return fieldsData.parse_quality.value === 'default'",
                    condition_python=lambda ports: ports["parse_quality"].value == "default",
                ),
                "remove_url_and_email": InputPort(
                    name="remove_url_and_email",
                    port_type=PortType.CHECKBOX,
                    value=True,
                    condition="return fieldsData.parse_quality.value === 'default'",
                    condition_python=lambda ports: ports["parse_quality"].value == "default",
                ),
                "parse_table": InputPort(
                    name="parse_table",
                    port_type=PortType.CHECKBOX,
                    value=True,
                    condition="return fieldsData.parse_quality.value === 'high'",
                    condition_python=lambda ports: ports["parse_quality"].value == "high",
                ),
                "parse_formula": InputPort(
                    name="parse_formula",
                    port_type=PortType.CHECKBOX,
                    value=False,
                    condition="return fieldsData.parse_quality.value === 'high'",
                    condition_python=lambda ports: ports["parse_quality"].value == "high",
                ),
                "multiple": InputPort(
                    name="multiple",
                    port_type=PortType.CHECKBOX,
                    value=True,
                ),
                "output": OutputPort(),
            },
        )


class FileUpload(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="FileUpload",
            category="file_processing",
            task_name="file_processing.file_upload",
            node_id=id,
            ports={
                "files": InputPort(
                    name="files",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=["*/*"],
                    multiple=True,
                    show=True,
                ),
                "unzip_files": InputPort(
                    name="unzip_files",
                    port_type=PortType.CHECKBOX,
                    value=False,
                ),
                "unzip_output_format": InputPort(
                    name="unzip_output_format",
                    port_type=PortType.SELECT,
                    value="list",
                    options=[
                        {"value": "list", "label": "list"},
                        {"value": "dict", "label": "dict"},
                    ],
                    condition="return fieldsData.unzip_files.value",
                    condition_python=lambda ports: ports["unzip_files"].value,
                ),
                "allowed_file_types": InputPort(
                    name="allowed_file_types",
                    port_type=PortType.INPUT,
                    value="*/*",
                ),
                "multiple": InputPort(
                    name="multiple",
                    port_type=PortType.CHECKBOX,
                    value=True,
                ),
                "output": OutputPort(),
            },
        )
