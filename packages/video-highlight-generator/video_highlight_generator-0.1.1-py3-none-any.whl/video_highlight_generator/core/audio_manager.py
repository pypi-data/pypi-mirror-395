from moviepy.editor import AudioFileClip

class AudioManager:
    def __init__(self):
        pass

    def get_audio_duration(self, audio_path: str):
        try:
            clip = AudioFileClip(audio_path)
            duration = clip.duration
            clip.close()
            return duration
        except Exception as e:
            print(f"Error reading audio {audio_path}: {e}")
            return 0

    def trim_audio(self, input_path: str, output_path: str, start_time: float, end_time: float):
        try:
            clip = AudioFileClip(input_path)
            trimmed = clip.subclip(start_time, end_time)
            trimmed.write_audiofile(output_path)
            clip.close()
            return True
        except Exception as e:
            print(f"Error trimming audio: {e}")
            return False
