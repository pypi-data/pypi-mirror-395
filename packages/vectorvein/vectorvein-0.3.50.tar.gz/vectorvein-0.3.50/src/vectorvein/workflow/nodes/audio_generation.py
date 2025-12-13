from ..graph.node import Node
from ..graph.port import PortType, InputPort, OutputPort


class MinimaxMusicGeneration(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="MinimaxMusicGeneration",
            category="audio_generation",
            task_name="audio_generation.minimax_music_generation",
            node_id=id,
            ports={
                "audio_file": InputPort(
                    name="audio_file",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".wav", ".mp3"],
                    multiple=True,
                ),
                "purpose": InputPort(
                    name="purpose",
                    port_type=PortType.SELECT,
                    value="song",
                    options=[
                        {"value": "song", "label": "song"},
                        {"value": "voice", "label": "voice"},
                        {"value": "instrumental", "label": "instrumental"},
                    ],
                ),
                "lyrics": InputPort(
                    name="lyrics",
                    port_type=PortType.TEXTAREA,
                    value="",
                    max_length=200,
                ),
                "model": InputPort(
                    name="model",
                    port_type=PortType.SELECT,
                    value="music-01",
                    options=[{"value": "music-01", "label": "music-01"}],
                ),
                "sample_rate": InputPort(
                    name="sample_rate",
                    port_type=PortType.SELECT,
                    value=44100,
                    options=[
                        {"value": 16000, "label": "16000"},
                        {"value": 24000, "label": "24000"},
                        {"value": 32000, "label": "32000"},
                        {"value": 44100, "label": "44100"},
                    ],
                ),
                "bitrate": InputPort(
                    name="bitrate",
                    port_type=PortType.SELECT,
                    value=256000,
                    options=[
                        {"value": 32000, "label": "32000"},
                        {"value": 64000, "label": "64000"},
                        {"value": 128000, "label": "128000"},
                        {"value": 256000, "label": "256000"},
                    ],
                ),
                "format": InputPort(
                    name="format",
                    port_type=PortType.SELECT,
                    value="mp3",
                    options=[
                        {"value": "mp3", "label": "mp3"},
                        {"value": "wav", "label": "wav"},
                        {"value": "pcm", "label": "pcm"},
                    ],
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class MusicGeneration(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="MusicGeneration",
            category="audio_generation",
            task_name="audio_generation.music_generation",
            node_id=id,
            ports={
                "text": InputPort(
                    name="text",
                    port_type=PortType.TEXTAREA,
                    value="",
                    max_length=50,
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class SoundEffects(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="SoundEffects",
            category="audio_generation",
            task_name="audio_generation.sound_effects",
            node_id=id,
            ports={
                "text": InputPort(
                    name="text",
                    port_type=PortType.TEXTAREA,
                    value="",
                    max_length=50,
                    multiple=True,
                ),
                "video": InputPort(
                    name="video",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".mp4", ".mov", ".webm", ".m4v", ".gif"],
                    multiple=True,
                ),
                "length": InputPort(
                    name="length",
                    port_type=PortType.NUMBER,
                    value=5,
                    min=1,
                    max=60,
                ),
                "output_type": OutputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class Tts(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="Tts",
            category="audio_generation",
            task_name="audio_generation.tts",
            node_id=id,
            ports={
                "text": InputPort(
                    name="text",
                    port_type=PortType.TEXTAREA,
                    value="",
                    multiple=True,
                ),
                "model": InputPort(
                    name="model",
                    port_type=PortType.SELECT,
                    value="cosyvoice-v2",
                    options=[
                        {"value": "cosyvoice-v2", "label": "cosyvoice-v2"},
                        {"value": "minimax-speech-02-hd", "label": "minimax-speech-02-hd"},
                        {"value": "minimax-speech-02-turbo", "label": "minimax-speech-02-turbo"},
                    ],
                ),
                "voice": InputPort(
                    name="voice",
                    port_type=PortType.SELECT,
                    value="longxiaochun_v2",
                    options=[],
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )


class VoiceClone(Node):
    def __init__(self, id: str | None = None):
        super().__init__(
            node_type="VoiceClone",
            category="audio_generation",
            task_name="audio_generation.voice_clone",
            node_id=id,
            ports={
                "text": InputPort(
                    name="text",
                    port_type=PortType.TEXTAREA,
                    value="",
                ),
                "voice_audio": InputPort(
                    name="voice_audio",
                    port_type=PortType.FILE,
                    value=[],
                    support_file_types=[".wav", ".mp3", ".m4a", ".ogg"],
                ),
                "output_type": InputPort(
                    name="output_type",
                    port_type=PortType.SELECT,
                    value="only_link",
                    options=[
                        {"value": "only_link", "label": "only_link"},
                        {"value": "html", "label": "html"},
                    ],
                ),
                "output": OutputPort(),
            },
        )
