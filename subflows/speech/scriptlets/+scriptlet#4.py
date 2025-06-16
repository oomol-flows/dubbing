import os

def main(params: dict):
  text: str = params["text"]
  file_name: str = params["file_name"]
  output_dir: str = params["output_dir"]

  return {
    "text": text,
    "audio_file": os.path.join(output_dir, f"{file_name}.wav"),
    "srt_file_name": f"{file_name}.srt",
  }
