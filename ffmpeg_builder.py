class FFmpegCommandBuilder:
    def __init__(self):
        self.codec_options = {
            'mp4': ('libx264', 'aac'),
            'webm': ('libvpx', 'libvorbis'),
            'mkv': ('libx264', 'aac'),
            'avi': ('mpeg4', 'libmp3lame'),
        }

    def construct_command(self, input_file, output_file, output_format, bitrate, resolution=None, frame_rate=None, crf=None):
        vcodec, acodec = self.codec_options.get(output_format, ('libx264', 'aac'))
        command = ['ffmpeg', '-y', '-i', input_file, '-vcodec', vcodec, '-acodec', acodec, '-b:v', f'{bitrate}k']

        if crf is not None:
            command.extend(['-crf', str(crf)])
        if resolution and resolution.lower() != "original":
            command.extend(['-s', resolution])
        if frame_rate is not None:
            command.extend(['-r', str(frame_rate)])
        command.append(output_file)
        return command