from pathlib import Path
from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
  name: str
  audio_ext: typing.Literal[".wav", ".mp3", ".wma"]
  output_dir: str
class Outputs(typing.TypedDict):
  audio_path: str
  srt_file: str
#endregion

def main(params: Inputs, context: Context) -> Outputs:
  name = params["name"]
  audio_ext = params["audio_ext"]
  output_dir = Path(params["output_dir"])
  return {
    "audio_path": str(output_dir / f"{name}{audio_ext}"),
    "srt_file": str(output_dir / f"{name}.srt"),
  }
