from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
#from moviepy.config import change_settings
import os

#change_settings({"IMAGEMAGICK_BINARY": "/path/to/convert"})

def join_video_and_audio(video_path, audio_path, output_path, new_resolution=(1080, 1920), text="Your Text Here", text_position=(0, 0.05)):
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the desired resolution
    video_clip = video_clip.resize(new_resolution)

    # Set audio for the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Add text to the video
    txt_clip = TextClip(text, fontsize=40, color='white', bg_color='black')
    txt_clip = txt_clip.set_position(text_position).set_duration(video_clip.duration)
    video_clip = video_clip.set_audio(audio_clip).set_duration(audio_clip.duration).overlay_x=0

    # Composite the video with the text
    video_clip = CompositeVideoClip([video_clip, txt_clip])

    # Write the video to the output file
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Remove the temporary video and audio files
    os.remove(video_path)
    os.remove(audio_path)