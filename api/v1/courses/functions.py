import os

from django.conf import settings

from pydub import AudioSegment

from courses.models import *
from general.functions import get_auto_id


def assign_next_topic(next_topic_id, student_profile):
    if(daily_audio_topic := DailyAudioTopic.objects.filter(pk=next_topic_id)).exists():
        daily_audio_topic = daily_audio_topic.latest("date_added")

        if not StudentDailyAudioTopic.objects.filter(daily_audio_topic=daily_audio_topic, student_profile=student_profile).exists():
            
            student_topic = StudentDailyAudioTopic.objects.create(
                auto_id = get_auto_id(StudentDailyAudioTopic),
                daily_audio_topic = daily_audio_topic,
                student_profile = student_profile,
                is_processed = True
            )
        else:
            return "Failed"

    elif(daily_video_topic := DailyVideoTopic.objects.filter(pk=next_topic_id)).exists():
        daily_video_topic = daily_video_topic.latest("date_added")
        if not StudentDailyVideoTopic.objects.filter(daily_video_topic=daily_video_topic, student_profile=student_profile).exists():
            
            student_topic = StudentDailyVideoTopic.objects.create(
                auto_id = get_auto_id(StudentDailyVideoTopic),
                daily_video_topic = daily_video_topic,
                student_profile = student_profile,
                is_processed = True
            )
        else:
            return "Failed"


    elif(daily_text_topic := DailyTextTopic.objects.filter(pk=next_topic_id)).exists():
        daily_text_topic = daily_text_topic.latest("date_added")

        if not StudentDailyTextTopic.objects.filter(daily_text_topic=daily_text_topic, student_profile=student_profile).exists():
            student_topic = StudentDailyTextTopic.objects.create(
                auto_id = get_auto_id(StudentDailyTextTopic),
                daily_text_topic = daily_text_topic,
                student_profile = student_profile,
                is_processed = True
            )
        else:
            return "Failed"


    elif(daily_image_topic := DailyImageTopic.objects.filter(pk=next_topic_id)).exists():
        daily_image_topic = daily_image_topic.latest("date_added")

        if not StudentDailyImageTopic.objects.filter(daily_image_topic=daily_image_topic, student_profile=student_profile).exists():
            student_topic = StudentDailyImageTopic.objects.create(
                auto_id = get_auto_id(StudentDailyImageTopic),
                daily_image_topic = daily_image_topic,
                student_profile = student_profile,
                is_processed = True
            )
        else:
            return "Failed"
    
    return True


def convert_to_mp3(uploaded_file):
    try:
        # Generate a temporary file path for the uploaded file
        temp_file_path = os.path.join("/tmp", uploaded_file.name)
        
        # Save the uploaded file to the temporary path
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
        
        # Load the input audio file
        audio = AudioSegment.from_file(temp_file_path)
        
        # Define the output MP3 file name
        base_filename = os.path.splitext(uploaded_file.name)[0]
        # output_mp3_file = os.path.join(settings.MEDIA_ROOT, f"{base_filename}.mp3")
        output_mp3_file = f"{base_filename}.mp3"
        
        # Convert the audio to MP3 format
        audio.export(output_mp3_file, format="mp3")
        
        print(f"Conversion successful: {uploaded_file.name} -> {output_mp3_file}")
        
        # Clean up the temporary file
        os.remove(temp_file_path)
        return output_mp3_file
    except Exception as e:
        print(f"Conversion failed: {str(e)}")



       
