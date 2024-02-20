from ffmpeg_builder import FFmpegCommandBuilder
import os
import tempfile
import json
from utility import Utility
import streamlit as st

class VideoProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert_webm_to_self(self):
        """Converts a WebM file to itself with re-encoding to fix header issues and codec compatibility."""
        converted_file_path = f"{self.file_path}_converted.webm"
        command = [
            'ffmpeg', '-y', '-i', self.file_path,
            '-c:v', 'libvpx-vp9',  # Re-encode video stream to VP9
            '-c:a', 'libopus',  # Re-encode audio stream to Opus
            converted_file_path
        ]
        returncode, output, error = Utility.run_subprocess(command)
        if returncode == 0:
            print("Conversion successful:", converted_file_path)  # Debugging output
            return converted_file_path
        else:
            print("Conversion failed:", error)  # Debugging output
            return self.file_path  # Return original path if conversion failed

    def get_properties(self):

        # Use ffprobe to get video properties in JSON format
        cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate,bit_rate:format=duration',
            '-print_format', 'json', self.file_path
        ]

        returncode, output, _ = Utility.run_subprocess(cmd)
        if returncode == 0 and output:
            try:
                data = json.loads(output)
                width = height = frame_rate = duration = bitrate_kbps = 0  # Initialize all variables to default values

                if 'streams' in data and len(data['streams']) > 0:
                    stream = data['streams'][0]
                    width = stream.get('width', 0)
                    height = stream.get('height', 0)
                    frame_rate_str = stream.get('r_frame_rate', '0/1')
                    numerator, denominator = map(int, frame_rate_str.split('/'))
                    frame_rate = numerator / denominator if denominator else 0

                if 'format' in data:
                    duration = float(data['format'].get('duration', 0))

                else:
                    duration = 0

                if 'streams' in data and len(data['streams']) > 0:
                    stream = data['streams'][0]
                    width = stream.get('width', 0)
                    height = stream.get('height', 0)
                    frame_rate_str = stream.get('r_frame_rate', '0/1')
                    numerator, denominator = map(int, frame_rate_str.split('/'))
                    frame_rate = numerator / denominator if denominator else 0

                # Calculate bitrate using the file size and duration
                file_size_bytes = os.path.getsize(self.file_path)
                if duration > 0:  # Ensure duration is non-zero to avoid division by zero
                    bitrate_kbps = (file_size_bytes * 8) / (1024 * duration)  # Convert bytes to kilobits and divide by duration in seconds
                else:
                    bitrate_kbps = 0  # Default value if duration is zero or not available

                properties = {
                    'duration': duration,
                    'width': width,
                    'height': height,
                    'frame_rate': frame_rate,
                    'bitrate_kbps': bitrate_kbps,
                    'file_size_bytes': file_size_bytes,
                }
                return properties
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from ffprobe output: {e}")
                return None
        return None

    def convert(self, output_format, new_bitrate, resolution, frame_rate, crf):
        output_file_suffix = f".{output_format}"
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=output_file_suffix).name
        builder = FFmpegCommandBuilder()
        command = builder.construct_command(self.file_path, output_file, output_format, new_bitrate, resolution, frame_rate, crf)
        returncode, _, error = Utility.run_subprocess(command)
        if returncode == 0:
            return output_file, None
        return None, error