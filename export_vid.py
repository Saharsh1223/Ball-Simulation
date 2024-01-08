from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

def join_video_and_audio(video_path, audio_path, output_path, new_resolution=(1080, 1920), text1="A Ball but every time it\nbounces, it gets bigger.", text1_position=(0.5, 0.18), text2="@SaharshDev", text2_position=(0.5, 0.75)):
    
    font_path="roboto-mono.ttf"
    
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the desired resolution
    video_clip = video_clip.resize(new_resolution)

    # Set audio for the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Add the first text to the video
    txt_clip1 = TextClip(text1, fontsize=60, color='white', bg_color='black', font=font_path)

    # Calculate the y-axis position for the first text in pixels
    y_position_pixels1 = int(text1_position[1] * video_clip.size[1])

    # Set the position of the first text relative to the center
    txt_clip1 = txt_clip1.set_position(('center', y_position_pixels1), relative=False).set_duration(video_clip.duration)

    # Add the second text to the video
    txt_clip2 = TextClip(text2, fontsize=40, color='white', bg_color='black', font=font_path)

    # Calculate the y-axis position for the second text in pixels
    y_position_pixels2 = int(text2_position[1] * video_clip.size[1])

    # Set the position of the second text relative to the center
    txt_clip2 = txt_clip2.set_position(('center', y_position_pixels2), relative=False).set_duration(video_clip.duration).set_opacity(0.5)

    
    # Composite the video with both texts
    video_clip = CompositeVideoClip([video_clip, txt_clip1, txt_clip2])

    # Write the video to the output file
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Remove the temporary video and audio files
    os.remove(video_path)
    os.remove(audio_path)