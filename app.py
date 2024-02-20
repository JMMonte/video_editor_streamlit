import streamlit as st
import os
import tempfile
from video_processor import VideoProcessor  # Assuming VideoProcessor is defined elsewhere

# Constants for supported file types and standard resolutions
input_file_types = ['mp4', 'mov', 'avi', 'mkv', 'webm']
output_file_types = ['mp4', 'webm', 'mkv', 'avi']

if 'webm_converted' not in st.session_state:
    st.session_state.webm_converted = False

# Function to display video properties
def display_video_properties(properties):
    st.write(f"Duration: {properties['duration']} seconds")
    st.write(f"Resolution: {properties['width']}x{properties['height']}")
    st.write(f"Frame Rate: {properties['frame_rate']} FPS")
    bitrate = float(properties['bitrate_kbps'])
    st.write(f"Bit Rate: {bitrate:.2f} Kbps")
    file_size_mb = properties['file_size_bytes'] / (1024 * 1024)  # Convert bytes to megabytes
    st.write(f"File Size: {file_size_mb:.2f} MB")

# Function to get user inputs for conversion
def user_conversion_inputs():
    output_format = st.selectbox("Select output file format", output_file_types)
    new_bitrate = st.slider("Select bitrate value (Kbps)", 100, 4000, 1000)
    resolution_option = st.selectbox("Select output resolution", ["Original", "1920x1080", "1280x720"], index=0)
    frame_rate = st.number_input("Frame Rate (e.g., 30):", min_value=1, value=30, step=1)
    crf = st.slider("CRF (Quality): Lower is better, applicable to mp4/webm", 0, 51, 23)
    return output_format, new_bitrate, resolution_option, frame_rate, crf

# Main script execution
st.title('Advanced FFmpeg Video Converter')
uploaded_file = st.file_uploader("Choose a video file", type=input_file_types)

if uploaded_file is not None:
    # Use a context manager to automatically clean up the temp file
    with tempfile.NamedTemporaryFile(delete=True, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name

        video_processor = VideoProcessor(file_path)  # Create a VideoProcessor instance

        # Only convert .webm files on their first load
        if file_path.endswith('.webm') and not st.session_state.webm_converted:
            with st.spinner("Re-converting webm file for accurate properties..."):
                file_path = video_processor.convert_webm_to_self()
                video_processor = VideoProcessor(file_path)  # Refresh the instance
                st.session_state.webm_converted = True  # Mark the .webm file as converted

        properties = video_processor.get_properties()  # Get video properties

        if properties:
            display_video_properties(properties)  # Display video properties
            output_format, new_bitrate, resolution_option, frame_rate, crf = user_conversion_inputs()  # Get user inputs

            if st.button("Convert"):
                with st.spinner("Converting video..."):
                    output_file, error = video_processor.convert(output_format, new_bitrate, resolution_option, frame_rate, crf)  # Perform conversion
            
                # Display success message and download link if conversion is successful
                if output_file:
                    st.success("Video converted successfully.")
                    
                    with open(output_file, "rb") as file:
                        st.download_button("Download converted video", file, file_name=os.path.basename(output_file))
                        
                        # get video properties of new file
                        new_properties = VideoProcessor(output_file).get_properties()
                        if new_properties:
                            st.write("New video properties:")
                            display_video_properties(new_properties)
                else:
                    st.error(f"Error converting video: {error}")
