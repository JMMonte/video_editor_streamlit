# Advanced FFmpeg Video Converter

This Streamlit app provides a user-friendly interface for converting video files between different formats, adjusting video quality parameters such as bitrate, resolution, and frame rate. It utilizes a `VideoProcessor` class (defined elsewhere) to handle the actual video processing tasks.

## Features

- **File Upload:** Users can upload video files in formats such as MP4, MOV, AVI, MKV, and WEBM.
- **Video Properties Display:** After uploading, the app displays properties of the video including duration, resolution, frame rate, bit rate, and file size.
- **Conversion Options:** Users can select the output file format, adjust bitrate, choose output resolution (including an option to keep the original resolution), set frame rate, and specify CRF (Constant Rate Factor) for quality control.
- **.webm Reconversion:** The app has a feature to re-convert `.webm` files on their first load to ensure accurate property display and conversion.
- **Temporary File Handling:** Uploaded files are managed using temporary files to ensure that data is not permanently stored on the server.

## How It Works

1. **Uploading a Video:** Users start by uploading a video file. The app supports several popular video formats.
2. **Displaying Video Properties:** Once a video is uploaded, its properties are displayed to give users insights into the file's characteristics.
3. **Setting Conversion Parameters:** Users can then set various parameters for the conversion process, including output format, bitrate, resolution, frame rate, and CRF.
4. **Conversion:** With parameters set, users can initiate the conversion process. The app displays a spinner during conversion and provides a download link for the converted video upon completion.

## Usage

1. **Run the Streamlit App:** Ensure you have Streamlit installed and run the app using `streamlit run your_script.py`.
2. **Upload a Video File:** Click on the "Choose a video file" button and select a video from your device.
3. **Adjust Conversion Settings:** Use the provided options to customize the output according to your needs.
4. **Convert and Download:** Click on the "Convert" button and wait for the process to complete. Then, use the "Download converted video" button to save the converted file to your device.

## Dependencies

- Streamlit
- A custom `VideoProcessor` class for handling video processing tasks. Ensure this class is defined and accessible within your project.

## Note

This README assumes that the `VideoProcessor` class is defined in a separate module and is responsible for the actual video processing, including getting video properties and performing conversions. Make sure to implement or provide this class as per your project's requirements.
