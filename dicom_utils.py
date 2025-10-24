import pydicom
import imageio.v2 as imageio
import numpy as np
from pathlib import Path

def extract(fpath):
  ds = pydicom.dcmread(fpath)
  print(f"File: {fpath} | Frames: {ds.get('NumberOfFrames', 1)}")

  frames = ds.pixel_array
  if frames.ndim == 2:
      frames = np.expand_dims(frames, axis=0)

  fpath = Path(fpath)
  fname = fpath.stem
  fparentname = fpath.parent.name
  out_path = Path("frame_output") / fparentname / f"{fname}_frames"
  out_path.mkdir(parents=True, exist_ok=True)

  for i, frame in enumerate(frames):
      out_file = out_path / f"{fname}_{i:03d}.png"
      imageio.imwrite(out_file, frame)
  
  print(f"{len(frames)} frame dari {fpath.name} berhasil disimpan di: {out_path}")
  
def to_video(fpath, fps=10):
  ds = pydicom.dcmread(fpath)
  print(f"File: {fpath} | Frames: {ds.get('NumberOfFrames', 1)}")

  frames = ds.pixel_array   # shape: (n_frames, height, width)
  if frames.ndim == 2:
      frames = np.expand_dims(frames, axis=0)  # jadi (1, H, W)

  fpath = Path(fpath)
  fname = fpath.stem
  fparentname = fpath.parent.name
  out_path = Path("video_output") / fparentname
  out_path.mkdir(parents=True, exist_ok=True)
  out_file = out_path / f"{fname}.mp4"

  with imageio.get_writer(out_file, fps=fps) as writer:
      for frame in frames:
          # Kalau grayscale, convert ke 3 channel biar kompatibel dengan video
          if frame.ndim == 2:
              frame_rgb = np.stack([frame]*3, axis=-1)  # (H, W, 3)
          else:
              frame_rgb = frame
          writer.append_data(frame_rgb)

  print(f"{len(frames)} frame dari {fpath.name} berhasil disimpan di: {out_file}")
