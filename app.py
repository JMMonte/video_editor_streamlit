import streamlit as st
import subprocess
import os
import tempfile

# Supported input and output file types
input_file_types = ['mp4', 'mov', 'avi', 'mkv', 'webm']
output_file_types = ['mp4', 'webm', 'mkv', 'avi']

def get_video_properties(file_path):
    """Get the duration in seconds and calculate average bitrate if necessary."""
    # Get duration
    duration_cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path,
    ]
    duration_result = subprocess.run(duration_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration_str = duration_result.stdout.strip()
    
    # Check if duration is 'N/A' or not present
    if not duration_str or duration_str == 'N/A':
        duration = 0.0  # Assign a default value or handle the error as needed
    else:
        duration = float(duration_str)

    # Attempt to get bitrate directly
    bitrate_cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', file_path,
    ]
    bitrate_result = subprocess.run(bitrate_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    bitrate_str = bitrate_result.stdout.strip()
    
    # Calculate average bitrate if direct bitrate is 'N/A' or missing
    if not bitrate_str or bitrate_str == 'N/A' or duration == 0.0:
        if duration > 0:
            file_size_bytes = os.path.getsize(file_path)
            # Calculate bitrate in kbps
            bitrate_kbps = (file_size_bytes * 8) / (1024 * duration)
        else:
            bitrate_kbps = 0.0  # Handle as needed if duration is 0
    else:
        bitrate_kbps = float(bitrate_str) / 1000

    return duration, bitrate_kbps

def get_webm_properties(file_path):
    """Get properties for a .webm file, attempting to handle cases where ffprobe might not return expected values."""
    # Attempt to get duration
    duration_cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path,
    ]
    duration_result = subprocess.run(duration_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration_str = duration_result.stdout.strip()
    duration = float(duration_str) if duration_str not in ['N/A', ''] else 0.0

    # Get file size in Kilobytes (KB)
    file_size_bytes = os.path.getsize(file_path)
    file_size_kb = file_size_bytes / 1024.0

    # Estimate bitrate if duration is available
    if duration > 0:
        bitrate_kbps = (file_size_kb * 8) / duration
    else:
        bitrate_kbps = 0.0

    return duration, bitrate_kbps

def calculate_new_file_size(bitrate_kbps, duration_seconds):
    return (bitrate_kbps * duration_seconds) / (8 * 1024)

def construct_ffmpeg_command(input_file, output_file, bitrate, output_format):
    codec_options = {
        'mp4': ('libx264', 'aac'),
        'webm': ('libvpx', 'libvorbis'),
        'mkv': ('libx264', 'aac'),
        'avi': ('mpeg4', 'libmp3lame'),
    }
    vcodec, acodec = codec_options.get(output_format, ('libx264', 'aac'))
    return [
        'ffmpeg', '-i', input_file, '-vcodec', vcodec, '-b:v', f'{bitrate}k',
        '-acodec', acodec, output_file
    ]

# Streamlit app interface
st.title('Advanced FFmpeg Video Converter')

uploaded_file = st.file_uploader("Choose a video file", type=input_file_types)
output_format = st.selectbox("Select output file format", output_file_types)
new_bitrate = st.slider("Select bitrate value (Kbps)", 100, 4000, 1000)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name

    if os.path.splitext(file_path)[-1][1:] == 'webm':
        duration, average_bitrate = get_webm_properties(file_path)
    else:
        duration, average_bitrate = get_video_properties(file_path)
    st.write(f"Average Bitrate: {average_bitrate:.2f} kbps")
    st.write(f"Duration: {duration:.2f} seconds")

    estimated_file_size = calculate_new_file_size(new_bitrate, duration)
    st.write(f"Estimated new file size: {estimated_file_size:.2f} MB")

    if st.button("Convert"):
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}").name
        command = construct_ffmpeg_command(file_path, output_file, new_bitrate, output_format)
        process = subprocess.run(command, capture_output=True, text=True)
        
        if process.returncode == 0:
            st.success("Video converted successfully")
            with open(output_file, "rb") as file:
                st.download_button("Download converted video", file, file_name=os.path.basename(output_file))
        else:
            st.error("Error converting video")
            st.code(process.stderr)
