from typing import Any
from batata.aliases import err as erro, out
from yt_dlp import YoutubeDL
from batata.errors import ParamError
from pathlib import Path


def hook(step):
    if step['status'] == 'downloading':
        out(f'\nBaixando {step.get("filename")} — {step.get("_percent_str")}')
    elif step['status'] == 'finished':
        out('\nDownload finalizado! Convertendo')


VIDEO_OPT = {
    'format': 'bestaudio+bestvideo/best',
    'progress_hook': [hook],
    'remote_components': ['ejs:github'],
}

AUDIO_OPT = {
    'format': 'bestaudio/best',
    'progress_hook': [hook],
    'remote_components': ['ejs:github'],
}


class PyDown:
    def __init__(self, urls: list[str], video_path: str, mode: str = 'video') -> None:
        options: dict[str, Any] = {}

        match mode:
            case 'video':
                options = VIDEO_OPT.copy()
            case 'audio':
                options = AUDIO_OPT.copy()
            case _:
                raise ParamError(
                    message=f'\033[1;31mERRO! \033[1;36mParametro “mode” invalido!',
                    param='mode',
                    esperado='video | audio'
                )

        if video_path.startswith('~'):
            video_path = str(Path(video_path).expanduser())

        if video_path.endswith('/'):
            video_path = video_path[:-1]

        self.urls: list[str] = urls
        self.video_path: str = video_path
        self.options: dict[str, Any] = options
        self.options['outtmpl'] = f'{self.video_path}/%(title)s.%(ext)s'

    def baixar(self) -> None:
        # noinspection PyTypeChecker
        with YoutubeDL(self.options) as ydl:
            # noinspection PyNoneFunctionAssignment
            err = ydl.download(self.urls)

        if err is not None and err != 0:
            erro(f'Erro ao baixar video: {err}')
            return
