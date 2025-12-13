# Sync Offset Tool

A command‑line utility to measure audio sync offsets between two MKV files. It extracts audio tracks, cross‑correlates them, and reports the best alignment offset in milliseconds.
As of v1.2.0, the tool also detects and reports **MKV container audio delays** and calculates the **effective offset** including those delays.

## Features
- 🎵 Audio extraction: Uses ffmpeg to pull raw PCM samples directly from MKV audio tracks.
- ⚡ Fast correlation: Defaults to FFT‑based cross‑correlation for speed.
- 🧮 Direct correlation option: More precise but slower.
- ⏱ Runtime reporting: Displays the exact runtime of both MKV files (hh:mm:ss.mmm).
- 🎬 FPS reporting: Displays the frames per second of the primary video stream in both files.
- ⏳ Container delay detection: Reports per‑track MKV audio delay metadata (start_time).
- 📐 Effective offset reporting: Combines raw correlation offset with container delays for a net sync difference.
- 📌 Version reporting: `--version` option shows the current tool version.

## Requirements
- Python 3.8+
- NumPy
- SciPy
- FFmpeg installed and available in your PATH

## Usage
```bash
./sync_offset.py original.mkv async.mkv [lang1] [lang2] [duration_seconds] [start_seconds] [method]
```

Arguments:
- `original.mkv` — reference file
- `async.mkv` — file suspected of being out of sync
- `lang1` — language code for original track (default: eng)
- `lang2` — language code for async track (default: eng)
- `duration_seconds` — slice length to analyze (default: 120)
- `start_seconds` — offset into the file to start slice (default: 0)
- `method` — correlation method: fft (default) or direct

Options:
- `--version` — display the tool’s version string

## Examples
Run FFT correlation on a 120‑second slice from the start, English vs English (default):
```bash
./sync_offset.py movie1.mkv movie2.mkv
```

Analyze a German audio track against an English one for 90 s:
```bash
./sync_offset.py movie1.mkv movie2.mkv deu eng 90
```

Run FFT correlation on a long 300‑second slice starting at 600 s:
```bash
./sync_offset.py movie1.mkv movie2.mkv eng eng 300 600 fft
```

Compare 10‑second slices starting at 320 s using direct correlation:
```bash
./sync_offset.py movie1.mkv movie2.mkv eng eng 10 320 direct
```

Show version:
```bash
./sync_offset.py --version
```

## Output
- Runtime (original): hh:mm:ss.mmm | FPS: xx.xxx fps
- Runtime (async):    hh:mm:ss.mmm | FPS: xx.xxx fps
- Container delay (original track): Reported in milliseconds.
- Container delay (async track): Reported in milliseconds.
- Best alignment offset (raw): Correlation‑based offset in milliseconds.
- Peak correlation strength: Value between 0 and 1 indicating match quality.
- Effective offset (including container delays): Net sync difference after accounting for MKV metadata delays.

### Interpreting correlation strength
- **> 0.80** → Excellent match, high confidence in the offset measurement
- **0.50 – 0.80** → Moderate match, offset is usable but less certain
- **< 0.50** → Weak match, results may be unreliable (consider shorter slices or different segments)

## Tips for Better Results
- Choose slices with **dialogue, sharp sounds, or clear audio events** — they produce stronger correlations than background noise or music alone.
- Use **shorter slices (10–60 s)** if correlation strength is weak; smaller segments often align more clearly.
- Try analyzing **different parts of the file** (e.g., start, middle, end) to confirm consistency of offsets.

## Notes
- Use FFT mode for long slices — it’s much faster.
- Use Direct mode only for short slices or when you need maximum precision.
- The script will refuse to run direct mode on slices >60 s without confirmation.
- On interruption, the worker process is terminated immediately — no orphan processes left behind.
- Container delays are reported directly from MKV metadata and may explain sync differences even before correlation.

## Troubleshooting
- No audio track found: Check the language codes (eng, deu, fra, etc.) with ffprobe.
- FFmpeg errors: Ensure ffmpeg and ffprobe are installed and accessible in your PATH.
- Negative offsets: A negative offset means the async file is ahead of the original.
- Performance: Direct mode is O(n²). For slices longer than ~30 s, prefer FFT mode.
- Effective offset mismatch: If raw offset and container delays differ, the MKV metadata may already compensate for sync.

## License
MIT License
