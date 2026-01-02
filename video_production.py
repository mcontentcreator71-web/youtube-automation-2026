"""
YouTube Video Production Script for The AI Ledger
This script handles video creation, voiceover, visuals, and captions
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Video Production Libraries (install with pip)
try:
    from gtts import gTTS
    from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
    try:
        from moviepy.config import check_ffmpeg
    except ImportError:
        # check_ffmpeg not available in this moviepy version, skip check
        check_ffmpeg = None
    import whisper
    from PIL import Image
    import requests
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Install with: pip install gtts moviepy openai-whisper pillow requests")
    sys.exit(1)


class VideoProducer:
    def __init__(self, output_dir="./videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_voiceover(self, script, language='en', output_file=None):
        """Generate voiceover using Google Text-to-Speech"""
        if output_file is None:
            output_file = self.output_dir / f"audio_{self.timestamp}.mp3"
        
        try:
            tts = gTTS(text=script, lang=language, slow=False)
            tts.save(str(output_file))
            return str(output_file)
        except Exception as e:
            print(f"Error generating voiceover: {e}")
            return None
    
    def generate_captions(self, audio_file, output_file=None):
        """Generate captions using OpenAI Whisper"""
        if output_file is None:
            output_file = self.output_dir / f"captions_{self.timestamp}.srt"
        
        try:
            model = whisper.load_model("base")
            result = model.transcribe(str(audio_file))
            
            # Convert to SRT format
            srt_content = self._convert_to_srt(result["segments"])
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            return str(output_file)
        except Exception as e:
            print(f"Error generating captions: {e}")
            return None
    
    def _convert_to_srt(self, segments):
        """Convert Whisper segments to SRT format"""
        srt = ""
        for i, segment in enumerate(segments, 1):
            start = self._format_timestamp(segment['start'])
            end = self._format_timestamp(segment['end'])
            text = segment['text'].strip()
            srt += f"{i}\n{start} --> {end}\n{text}\n\n"
        return srt
    
    def _format_timestamp(self, seconds):
        """Format seconds to SRT timestamp (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def create_video(self, audio_file, image_prompts, video_type="longform", output_file=None):
        """Create video with visuals and voiceover
        
        Args:
            audio_file: Path to audio file
            image_prompts: List of image prompts for scenes
            video_type: "shorts" (30-40s) or "longform" (15-20min)
            output_file: Output video file path
        """
        if output_file is None:
            video_suffix = "shorts" if video_type == "shorts" else "longform"
            output_file = self.output_dir / f"video_{video_suffix}_{self.timestamp}.mp4"
        
        try:
            # Load audio
            audio = AudioFileClip(str(audio_file))
            duration = audio.duration
            
            # Video settings based on type
            if video_type == "shorts":
                # Shorts: Vertical format, 30-40 seconds
                video_size = (1080, 1920)  # Vertical
                max_duration = 40  # Maximum 40 seconds
                fps = 30  # Higher FPS for Shorts
                fontsize = 60  # Larger text for mobile
            else:
                # Long-form: Horizontal format, 15-20 minutes
                video_size = (1920, 1080)  # Horizontal
                min_duration = 900  # Minimum 15 minutes
                max_duration = 1200  # Maximum 20 minutes
                fps = 24  # Standard FPS
                fontsize = 50  # Standard text size
            
            # Validate duration
            if video_type == "shorts" and duration > max_duration:
                print(f"Warning: Audio duration ({duration}s) exceeds Shorts limit ({max_duration}s)")
                # Trim audio if needed
                audio = audio.subclip(0, max_duration)
                duration = max_duration
            elif video_type == "longform" and duration < min_duration:
                print(f"Warning: Audio duration ({duration}s) is below Long-form minimum ({min_duration}s)")
            
            # For now, use placeholder images or stock footage
            # In production, you'd generate images using Stable Diffusion or fetch from APIs
            clips = []
            
            # Create video clips from images
            num_images = min(len(image_prompts), 10)  # Limit images
            clip_duration = duration / num_images if num_images > 0 else duration
            
            for i, prompt in enumerate(image_prompts[:num_images]):
                # Placeholder: Create a simple text clip
                # Replace this with actual image generation/fetching
                clip = TextClip(
                    prompt[:50],  # Truncate for display
                    fontsize=fontsize,
                    color='white',
                    size=video_size,
                    method='caption'
                ).set_duration(min(clip_duration, 10))
                
                clips.append(clip)
            
            # Concatenate clips
            if clips:
                video = concatenate_videoclips(clips, method="compose")
            else:
                # Fallback: single screen
                video = TextClip("The AI Ledger", fontsize=72, color='white', size=video_size).set_duration(duration)
            
            # Set audio
            final_video = video.set_audio(audio)
            
            # Add captions overlay (simplified - full implementation would parse SRT)
            # For production, use add_subtitles method with SRT file
            
            # Export
            final_video.write_videofile(
                str(output_file),
                fps=fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            return str(output_file)
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
    
    def process_video_request(self, data):
        """Main processing function for video production
        
        Handles both Shorts (30-40s) and Long-form (15-20min) videos
        """
        try:
            title = data.get('title', 'AI News Update')
            video_type = data.get('videoType', 'longform')
            
            # Select appropriate script based on video type
            if video_type == 'shorts':
                script = data.get('shortScript', '')
                target_duration = '30-40 seconds'
            else:
                script = data.get('longScript', '')
                target_duration = '15-20 minutes'
            
            image_prompts = data.get('imagePrompts', [])
            
            if not script:
                return {
                    'error': f'No {video_type} script provided',
                    'status': 'failed'
                }
            
            # Generate voiceover
            audio_file = self.generate_voiceover(script)
            if not audio_file:
                return {'error': 'Failed to generate voiceover', 'status': 'failed'}
            
            # Generate captions
            srt_file = self.generate_captions(audio_file)
            
            # Create video with appropriate settings
            video_file = self.create_video(audio_file, image_prompts, video_type)
            if not video_file:
                return {'error': 'Failed to create video', 'status': 'failed'}
            
            return {
                'status': 'success',
                'videoFilePath': video_file,
                'audioFilePath': audio_file,
                'srtFilePath': srt_file,
                'title': title,
                'videoType': video_type,
                'targetDuration': target_duration
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }


if __name__ == "__main__":
    # Read input from stdin (n8n will pass JSON)
    try:
        input_data = json.load(sys.stdin)
        producer = VideoProducer()
        result = producer.process_video_request(input_data)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({'error': str(e), 'status': 'failed'}))


