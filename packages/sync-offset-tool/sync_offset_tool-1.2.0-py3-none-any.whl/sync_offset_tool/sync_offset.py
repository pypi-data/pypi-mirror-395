#!/usr/bin/env python3
import subprocess
import numpy as np
import json
import signal
import multiprocessing as mp
from scipy.signal import correlate
import argparse
import sys

__version__ = "1.2.0"   # patched version

# --- Styling helpers ---
def warn_line(message):
    return f"\033[93m⚠️ {message}\033[0m"

def error_line(message):
    return f"\033[91m❌ {message}\033[0m"

_worker_proc = None

def _install_sigint_handler():
    def _handle_sigint(sig, frame):
        global _worker_proc
        if _worker_proc is not None and _worker_proc.is_alive():
            try:
                _worker_proc.terminate()
            except Exception:
                pass
        raise KeyboardInterrupt()
    signal.signal(signal.SIGINT, _handle_sigint)

def get_track_index(mkvfile, lang="eng"):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index:stream_tags=language",
        "-of", "json", mkvfile
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    for stream in data.get("streams", []):
        if stream.get("tags", {}).get("language", "").lower() == lang.lower():
            return stream["index"]
    raise RuntimeError(f"No {lang} audio track found in {mkvfile}")

def extract_pcm_to_array(mkvfile, track_index, sr=48000, duration=120, start=0):
    cmd = [
        "ffmpeg", "-ss", str(start), "-i", mkvfile,
        "-map", f"0:{track_index}", "-ac", "1", "-ar", str(sr),
        "-af", f"atrim=0:{duration}", "-f", "f32le", "pipe:1"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    data = np.frombuffer(proc.stdout, dtype=np.float32)
    print(f"Extracted {len(data)} samples from {mkvfile}")
    return data

def get_runtime(mkvfile):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        mkvfile
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    seconds = float(result.stdout.strip())
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"

def get_fps(mkvfile):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        mkvfile
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    rate = result.stdout.strip()
    if "/" in rate:
        num, denom = rate.split("/")
        fps = float(num) / float(denom)
    else:
        fps = float(rate)
    return f"{fps:.3f} fps"

def get_container_delay(mkvfile, lang="eng"):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", f"a:m:language:{lang}",
        "-show_entries", "stream=start_time",
        "-of", "default=noprint_wrappers=1:nokey=1",
        mkvfile
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    val = result.stdout.strip()
    if val:
        return float(val) * 1000.0
    return 0.0

def _direct_worker(sig1, sig2, sr, out_queue):
    corr = correlate(sig1, sig2, mode="full", method="direct")
    lag = np.argmax(corr) - (len(sig2) - 1)
    delay_ms = lag / sr * 1000
    peak_corr = corr[np.argmax(corr)] / len(sig1)
    out_queue.put((delay_ms, peak_corr))

def compute_offset(sig1, sig2, sr, method="fft", duration=120):
    sig1 = (sig1 - np.mean(sig1)) / (np.std(sig1) + 1e-9)
    sig2 = (sig2 - np.mean(sig2)) / (np.std(sig2) + 1e-9)
    min_len = min(len(sig1), len(sig2))
    sig1, sig2 = sig1[:min_len], sig2[:min_len]

    if method == "direct":
        if duration > 60:
            ans = input(warn_line(f"Direct correlation on {duration}s slice may be very slow. Continue? [y/N]: "))
            if ans.strip().lower() != "y":
                print(error_line("Aborted by user."))
                sys.exit(1)

        out_queue = mp.Queue()
        global _worker_proc
        _worker_proc = mp.Process(target=_direct_worker, args=(sig1, sig2, sr, out_queue), daemon=True)
        _worker_proc.start()
        try:
            while True:
                try:
                    result = out_queue.get(timeout=0.2)
                    break
                except Exception:
                    if not _worker_proc.is_alive():
                        raise RuntimeError("Direct correlation worker exited unexpectedly.")
            return result
        except KeyboardInterrupt:
            print(error_line("Interrupted by user (Ctrl+C). Terminating direct worker."))
            try:
                if _worker_proc.is_alive():
                    _worker_proc.terminate()
            except Exception:
                pass
            _worker_proc.join(timeout=1.0)
            _worker_proc = None
            sys.exit(1)
        finally:
            if _worker_proc is not None:
                _worker_proc.join(timeout=1.0)
                _worker_proc = None
    else:
        corr = correlate(sig1, sig2, mode="full", method="fft")
        lag = np.argmax(corr) - (len(sig2) - 1)
        delay_ms = lag / sr * 1000
        peak_corr = corr[np.argmax(corr)] / len(sig1)
        return delay_ms, peak_corr

def parse_args():
    parser = argparse.ArgumentParser(description="Measure audio sync offsets between two MKV files")
    parser.add_argument("original", help="Reference MKV file")
    parser.add_argument("async_file", help="File suspected of being out of sync")
    parser.add_argument("lang1", nargs="?", default="eng", help="Language code for original track (default: eng)")
    parser.add_argument("lang2", nargs="?", default="eng", help="Language code for async track (default: eng)")
    parser.add_argument("duration", nargs="?", type=int, default=120, help="Slice length to analyze in seconds (default: 120)")
    parser.add_argument("start", nargs="?", type=int, default=0, help="Offset into the file to start slice (default: 0)")
    parser.add_argument("method", nargs="?", choices=["fft", "direct"], default="fft", help="Correlation method (default: fft)")
    return parser.parse_args()

def main():
    _install_sigint_handler()

    # Handle --version manually before argparse
    if "--version" in sys.argv:
        print(f"sync_offset.py {__version__}")
        return

    args = parse_args()
    sr = 48000

    try:
        orig_index = get_track_index(args.original, args.lang1)
        async_index = get_track_index(args.async_file, args.lang2)

        orig_data = extract_pcm_to_array(args.original, orig_index, sr, args.duration, args.start)
        async_data = extract_pcm_to_array(args.async_file, async_index, sr, args.duration, args.start)

        orig_runtime = get_runtime(args.original)
        async_runtime = get_runtime(args.async_file)
        orig_fps = get_fps(args.original)
        async_fps = get_fps(args.async_file)

        print(f"Runtime (original): {orig_runtime} | FPS: {orig_fps}")
        print(f"Runtime (async):    {async_runtime} | FPS: {async_fps}")

        orig_delay_ms = get_container_delay(args.original, args.lang1)
        async_delay_ms = get_container_delay(args.async_file, args.lang2)

        print(f"Container delay (original track): {orig_delay_ms:.2f} ms")
        print(f"Container delay (async track):    {async_delay_ms:.2f} ms")

        offset_ms, peak_corr = compute_offset(orig_data, async_data, sr, args.method, args.duration)
        print(f"Best alignment offset (raw): {offset_ms:.2f} ms")
        print(f"Peak correlation strength: {peak_corr:.4f}")

        effective_offset_ms = offset_ms + (async_delay_ms - orig_delay_ms)
        print(f"Effective offset (including container delays): {effective_offset_ms:.2f} ms")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        import traceback
        print(error_line(f"Unexpected error: {e}"))
        traceback.print_exc()

if __name__ == "__main__":
    try:
        mp.set_start_method("fork")
    except RuntimeError:
        pass
    main()

