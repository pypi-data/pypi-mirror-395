from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips, vfx, CompositeVideoClip, VideoClip
# from moviepy.audio.fx.all import audio_loop # Removed in v2?
# Try to import audio_loop from where it might be, or use method
try:
    from moviepy.audio.fx.audio_loop import audio_loop
except ImportError:
    try:
        from moviepy.audio.fx.loop import loop as audio_loop
    except ImportError:
        # Fallback or maybe it's a method now
        audio_loop = None
import os
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np

import proglog

class CallbackLogger(proglog.ProgressBarLogger):
    def __init__(self, callback=None):
        super().__init__()
        self.progress_func = callback

    def bars_callback(self, bar, attr, value, old_value=None):
        if self.progress_func:
            # bar is usually 't' for time
            percentage = (value / self.bars[bar]['total']) * 100
            self.progress_func(percentage)

    def log(self, message):
        pass # Optional: log messages

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags
import time

def get_image_date(image_path):
    try:
        image = Image.open(image_path)
        exif = image._getexif()
        if exif:
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                if decoded == 'DateTimeOriginal' or decoded == 'DateTime':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        pass
        
    # Fallback to file modification time
    timestamp = os.path.getmtime(image_path)
    return datetime.fromtimestamp(timestamp)

class VideoGenerator:
    def __init__(self):
        pass

    def generate_video(self, images, audio_path, output_path, resolution=(1920, 1080), audio_start=0.0, audio_end=None, image_duration=3.0, title_text="", ken_burns_effect=False, progress_callback=None):
        try:
            clips = []
            
            # Prepare font for title if needed
            title_font = None
            date_font = None
            
            try:
                # Try to load a default font
                font_paths = [
                    "C:/Windows/Fonts/arial.ttf", # Windows
                    "C:/Windows/Fonts/seguiemj.ttf", # Windows
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", # Linux
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", # Linux
                    "/System/Library/Fonts/Helvetica.ttc", # macOS
                ]
                
                font_path = None
                for path in font_paths:
                    if os.path.exists(path):
                        font_path = path
                        break
                
                if font_path:
                    print(f"Loading font from: {font_path}")
                    title_font = ImageFont.truetype(font_path, 100)
                    date_font = ImageFont.truetype(font_path, 70)
                else:
                    print("Warning: Custom fonts not found, using default (tiny) font.")
                    title_font = ImageFont.load_default()
                    date_font = ImageFont.load_default()
            except Exception as e:
                print(f"Error loading font: {e}")
                title_font = ImageFont.load_default()
                date_font = ImageFont.load_default()

            for i, img_entry in enumerate(images):
                # Handle dict or string
                if isinstance(img_entry, dict):
                    img_path = img_entry['path']
                    faces = img_entry.get('faces', [])
                else:
                    img_path = img_entry
                    faces = []

                # Create clip, resize to fit resolution (maintaining aspect ratio), and center on black background
                # Use custom duration
                duration_per_image = float(image_duration)
                
                # Get date string
                img_date = get_image_date(img_path)
                date_str = img_date.strftime("%B %d, %Y")
                
                # Open image
                pil_img = Image.open(img_path).convert("RGBA")
                w, h = pil_img.size
                target_w, target_h = resolution
                
                if ken_burns_effect:
                    # KEN BURNS LOGIC
                    # Calculate Focus Point (0.0 - 1.0)
                    focus_x, focus_y = 0.5, 0.3 # Default: Top-Center
                    
                    if faces:
                        # Calculate centroid of faces
                        sum_x = 0
                        sum_y = 0
                        count = 0
                        for face in faces:
                            box = face.get('box')
                            if box:
                                # box is [x1, y1, x2, y2]
                                cx = (box[0] + box[2]) / 2
                                cy = (box[1] + box[3]) / 2
                                sum_x += cx
                                sum_y += cy
                                count += 1
                        
                        if count > 0:
                            focus_x = (sum_x / count) / w
                            focus_y = (sum_y / count) / h
                            # Clamp
                            focus_x = max(0.0, min(1.0, focus_x))
                            focus_y = max(0.0, min(1.0, focus_y))

                    # Resize logic for Ken Burns (Cover)
                    scale = max(target_w / w, target_h / h)
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    
                    pil_img_resized = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                    # Crop to aspect ratio first (centered on focus point?)
                    # If we just resize to cover, we might lose the focus point if we crop blindly.
                    # But _apply_ken_burns handles the movement.
                    # We should pass the 'cover' resized image to _apply_ken_burns.
                    # But wait, _apply_ken_burns resizes it AGAIN.
                    # Let's optimize:
                    # Pass the original image (or slightly downscaled if huge) to _apply_ken_burns?
                    # No, let's stick to the pattern:
                    # 1. Resize to 'Cover' (this ensures we have enough pixels to fill screen)
                    # 2. Pass this to _apply_ken_burns.
                    # 3. _apply_ken_burns will zoom in FURTHER (1.2x etc).
                    
                    # However, if we resize to cover, we might crop out the face if the aspect ratio is very different.
                    # Example: Portrait image (9:16) on Landscape video (16:9).
                    # 'Cover' will crop top/bottom or left/right.
                    # For Portrait on Landscape: Width matches, Height is huge. We crop top/bottom.
                    # We must ensure the crop includes the face.
                    
                    # Let's do a smart crop to 'Cover' resolution first, centered on focus point.
                    
                    # Target dimensions
                    tw, th = target_w, target_h
                    
                    # Current dimensions
                    cw, ch = new_w, new_h
                    
                    # We need to crop (cw, ch) to (tw, th)
                    # Focus point in (cw, ch)
                    fx_px = focus_x * cw
                    fy_px = focus_y * ch
                    
                    # Top-left of crop
                    left = fx_px - tw / 2
                    top = fy_px - th / 2
                    
                    # Clamp
                    left = max(0, min(left, cw - tw))
                    top = max(0, min(top, ch - th))
                    
                    pil_img_smart_cropped = pil_img_resized.crop((left, top, left + tw, top + th))
                    
                    # Now we have an image exactly size of resolution, centered on face.
                    # Now apply Ken Burns (zoom/pan) on this.
                    # Note: Since we cropped tightly, we can only Zoom IN.
                    # If we want to Zoom OUT, we needed more context.
                    # But Zoom IN is safe.
                    
                    img_clip = ImageClip(np.array(pil_img_smart_cropped.convert("RGB"))).with_duration(duration_per_image)
                    
                    # Apply Effect (Zoom In/Out relative to center of THIS cropped image)
                    # Since we centered on face, the center of this image IS the face (roughly).
                    # So we can just zoom in/out of center.
                    kb_clip = self._apply_ken_burns(img_clip, target_w, target_h, focus_point=(0.5, 0.5))
                    
                    # Create Text Layer
                    txt_img = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
                    d = ImageDraw.Draw(txt_img)
                    
                    # Draw Title (only on first image)
                    if i == 0 and title_text:
                        print(f"Drawing title: {title_text}")
                        bbox = d.textbbox((0, 0), title_text, font=title_font)
                        text_w = bbox[2] - bbox[0]
                        text_h = bbox[3] - bbox[1]
                        x = (target_w - text_w) / 2
                        y = target_h - text_h - 100
                        d.text((x+2, y+2), title_text, font=title_font, fill=(0, 0, 0, 200))
                        d.text((x, y), title_text, font=title_font, fill=(255, 255, 255, 255))
                        
                    # Draw Date
                    bbox = d.textbbox((0, 0), date_str, font=date_font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                    x = target_w - text_w - 30
                    y = target_h - text_h - 30
                    d.text((x+2, y+2), date_str, font=date_font, fill=(0, 0, 0, 200))
                    d.text((x, y), date_str, font=date_font, fill=(255, 255, 255, 255))
                    
                    txt_clip = ImageClip(np.array(txt_img)).with_duration(duration_per_image)
                    
                    # Composite
                    clip = CompositeVideoClip([kb_clip, txt_clip])
                    
                else:
                    # STATIC LOGIC (Original)
                    # Scale to fit (contain)
                    scale = min(target_w / w, target_h / h)
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                    # Create text layer
                    txt_img = Image.new("RGBA", pil_img.size, (255, 255, 255, 0))
                    d = ImageDraw.Draw(txt_img)
                    
                    # Update dimensions
                    w, h = pil_img.size
                    
                    # Draw Title (only on first image)
                    if i == 0:
                        print(f"Processing first image. Title text: '{title_text}'")
                        if title_text:
                            print(f"Drawing title: {title_text}")
                            bbox = d.textbbox((0, 0), title_text, font=title_font)
                            text_w = bbox[2] - bbox[0]
                            text_h = bbox[3] - bbox[1]
                            
                            x = (w - text_w) / 2
                            y = h - text_h - 100 # 100px padding from bottom
                            
                            # Draw shadow
                            d.text((x+2, y+2), title_text, font=title_font, fill=(0, 0, 0, 200))
                            # Draw text
                            d.text((x, y), title_text, font=title_font, fill=(255, 255, 255, 255))
                    
                    # Draw Date (on all images)
                    bbox = d.textbbox((0, 0), date_str, font=date_font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                    
                    x = w - text_w - 30
                    y = h - text_h - 30
                    
                    # Draw shadow
                    d.text((x+2, y+2), date_str, font=date_font, fill=(0, 0, 0, 200))
                    # Draw text
                    d.text((x, y), date_str, font=date_font, fill=(255, 255, 255, 255))
                    
                    out = Image.alpha_composite(pil_img, txt_img)
                    clip = ImageClip(np.array(out.convert("RGB"))).with_duration(duration_per_image)
                    
                    # Center (MoviePy handles positioning if clip is smaller than screen, 
                    # but we usually want to fill or fit. Here we fit.)
                    clip = clip.with_position("center")
                
                # Apply fade in/out for smooth transitions
                clip = clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
                
                clips.append(clip)
            
            # Concatenate clips
            # method="compose" is safer for different sizes
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Add audio
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                
                # Handle Trimming
                if audio_start > 0 or (audio_end is not None and audio_end > 0):
                    start = audio_start
                    end = audio_end if audio_end is not None and audio_end > 0 else audio.duration
                    # Ensure end is within bounds
                    end = min(end, audio.duration)
                    if start < end:
                        audio = audio.subclipped(start, end)
                
                # Loop audio if shorter than video
                if audio.duration < final_clip.duration:
                    # Manual loop
                    n_loops = int(final_clip.duration / audio.duration) + 1
                    audio = concatenate_audioclips([audio] * n_loops).subclipped(0, final_clip.duration)
                else:
                    audio = audio.subclipped(0, final_clip.duration)
                final_clip = final_clip.with_audio(audio)

            # Write file
            logger = None
            if progress_callback:
                logger = CallbackLogger(progress_callback)
            
            final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', logger=logger or 'bar')
            return True
        except Exception as e:
            print(f"Error generating video: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _apply_ken_burns(self, clip, width, height, focus_point=(0.5, 0.5)):
        """
        Applies a Ken Burns effect (pan & zoom) to the clip.
        focus_point: (x, y) tuple in 0.0-1.0 range indicating interest point.
        """
        w, h = clip.size
        duration = clip.duration
        
        # Zoom factor
        zoom_factor = random.uniform(1.15, 1.35)
        
        # Calculate dimensions of the zoomed image
        new_w = int(width * zoom_factor)
        new_h = int(height * zoom_factor)
        
        # Resize the clip first
        zoomed_clip = clip.resized((new_w, new_h))
        
        # Available movement range
        max_x = new_w - width
        max_y = new_h - height
        
        # Focus point in zoomed clip pixels
        fx = focus_point[0] * new_w
        fy = focus_point[1] * new_h
        
        # Ideal top-left to center the focus point
        target_x = fx - width / 2
        target_y = fy - height / 2
        
        # Clamp to bounds
        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))
        
        # Determine movement
        # 70% Zoom In, 30% Zoom Out
        mode = 'zoom_in' if random.random() < 0.7 else 'zoom_out'
        
        if mode == 'zoom_in':
            # Start: Center of image (or slightly offset)
            # End: target_x, target_y (Focused on face)
            
            # Start at center of scrollable area
            start_x = max_x / 2
            start_y = max_y / 2
            
            # Or start at random position?
            # Let's start at center for stability
            
            end_x = target_x
            end_y = target_y
            
        else: # zoom_out
            # Start: Focused on face
            # End: Center
            
            start_x = target_x
            start_y = target_y
            
            end_x = max_x / 2
            end_y = max_y / 2

        def make_frame(t):
            # Ease-in-out interpolation? Or just linear.
            # Linear is standard for Ken Burns.
            progress = t / duration
            
            # Simple ease-out for smoother feel?
            # progress = 1 - (1 - progress) * (1 - progress)
            
            x = int(start_x + (end_x - start_x) * progress)
            y = int(start_y + (end_y - start_y) * progress)
            
            # Ensure bounds
            x = max(0, min(x, max_x))
            y = max(0, min(y, max_y))
            
            # Get frame from zoomed clip
            frame = zoomed_clip.get_frame(t)
            
            # Crop: [y:y+height, x:x+width]
            return frame[y:y+height, x:x+width]

        return VideoClip(make_frame, duration=duration)

