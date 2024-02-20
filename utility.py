import subprocess

class Utility:
    @staticmethod
    def run_subprocess(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        return process.returncode, output, error

    @staticmethod
    def calculate_new_file_size(bitrate_kbps, duration_seconds):
        return (bitrate_kbps * duration_seconds) / (8 * 1024)  # Calculate in MB