import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import mimetypes

mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("video/mp4", ".mp4")

app = FastAPI(title="Video Highlight Generator")

from pydantic import BaseModel
from typing import List, Optional
from video_highlight_generator.core.image_processor import ImageProcessor
from video_highlight_generator.core.video_generator import VideoGenerator, get_image_date
from video_highlight_generator.core.database import Database
from video_highlight_generator.core.face_detector import FaceDetector
import glob

# Initialize Core Modules
# Initialize Core Modules
db_path = os.getenv("DB_PATH", "video_highlight_generator.db")
db = Database(db_path)
image_processor = ImageProcessor()
video_generator = VideoGenerator()
face_detector = FaceDetector()

class AnalysisRequest(BaseModel):
    folder_paths: List[str]

class VideoRequest(BaseModel):
    image_paths: List[str]
    audio_path: Optional[str] = None
    audio_start: Optional[float] = 0.0
    audio_end: Optional[float] = None
    output_path: str
    resolution: str = "1080p" # 1080p (PC) or 9:16 (Phone)
    image_duration: float = 3.0
    title_text: Optional[str] = ""
    ken_burns_effect: bool = False

from fastapi import Header
from fastapi.responses import StreamingResponse
import aiofiles

async def chunk_generator(file_path, start, end, chunk_size=1024*1024):
    try:
        async with aiofiles.open(file_path, "rb") as f:
            await f.seek(start)
            while start <= end:
                read_size = min(chunk_size, end - start + 1)
                data = await f.read(read_size)
                if not data:
                    break
                yield data
                start += len(data)
    except (ConnectionResetError, OSError):
        # Client disconnected, stop streaming
        pass

@app.get("/api/image")
async def get_image(path: str, range: str = Header(None)):
    print(f"Requested media path: {path}")
    if not os.path.exists(path):
        print(f"Media not found: {path}")
        return {"error": "Media not found"}, 404
    
    # Guess mime type
    media_type, _ = mimetypes.guess_type(path)
    if media_type is None:
        media_type = "application/octet-stream"
        
    # For video files, use custom streaming to handle Windows asyncio errors gracefully
    if media_type.startswith("video/") and range:
        try:
            file_size = os.path.getsize(path)
            start, end = range.replace("bytes=", "").split("-")
            start = int(start)
            end = int(end) if end else file_size - 1
            
            # Ensure bounds
            if start >= file_size:
                return {"error": "Requested range not satisfiable"}, 416
            
            chunk_size = 1024 * 1024 # 1MB chunks
            
            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(end - start + 1),
                "Content-Type": media_type,
            }
            
            return StreamingResponse(
                chunk_generator(path, start, end, chunk_size),
                headers=headers,
                status_code=206,
            )
        except Exception as e:
            print(f"Error streaming video: {e}")
            # Fallback to FileResponse
            return FileResponse(path, media_type=media_type)
        
    return FileResponse(path, media_type=media_type)

@app.post("/api/browse")
async def browse_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        folder_path = filedialog.askdirectory()
        root.destroy()
        
        if folder_path:
            folder_path = os.path.normpath(folder_path)
            return {"path": folder_path}
        return {"path": ""}
    except Exception as e:
        print(f"Error opening dialog: {e}")
        return {"error": str(e)}, 500

@app.post("/api/browse_file")
async def browse_file():
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.aac *.m4a")])
        root.destroy()
        
        if file_path:
            file_path = os.path.normpath(file_path)
            return {"path": file_path}
        return {"path": ""}
    except Exception as e:
        print(f"Error opening dialog: {e}")
        return {"error": str(e)}, 500

# Global progress state
progress_state = {
    "status": "idle",
    "percent": 0,
    "message": ""
}

@app.get("/api/progress")
async def get_progress():
    return progress_state

def update_progress(status, percent, message):
    progress_state["status"] = status
    progress_state["percent"] = percent
    progress_state["message"] = message

def process_analysis(request: AnalysisRequest):
    try:
        # Validate folders
        valid_folders = []
        for path in request.folder_paths:
            if os.path.exists(path):
                valid_folders.append(path)
        
        if not valid_folders:
            update_progress("error", 0, "No valid folders found")
            return
        
        update_progress("analyzing", 0, "Starting analysis...")
        
        # Find images across all folders
        extensions = ['*.jpg', '*.jpeg', '*.png']
        image_files = []
        seen_paths = set()
        for folder in valid_folders:
            for ext in extensions:
                for img_path in glob.glob(os.path.join(folder, ext)):
                    norm_path = os.path.normpath(img_path)
                    if norm_path not in seen_paths:
                        image_files.append(norm_path)
                        seen_paths.add(norm_path)
        
        total_images = len(image_files)
        if total_images == 0:
            update_progress("completed", 100, "No images found")
            progress_state["result"] = {"results": [], "people": [], "themes": []}
            return

        # Analyze images
        results = []
        
        # Batch check DB
        update_progress("analyzing", 0, "Checking cache...")
        cached_data = db.get_images_batch(image_files)
        
        new_images_to_process = []
        
        for img_path in image_files:
            if img_path in cached_data:
                data = cached_data[img_path]
                data['path'] = img_path
                results.append(data)
            else:
                new_images_to_process.append(img_path)
                
        # Process new images
        new_results_to_save = []
        total_new = len(new_images_to_process)
        
        for i, img_path in enumerate(new_images_to_process):
            # Update progress based on new images processing
            # We could also factor in cached images but processing new ones takes the most time
            percent = int((i / total_new) * 90) if total_new > 0 else 90
            update_progress("analyzing", percent, f"Analyzing new image {i+1}/{total_new}...")
            
            data = image_processor.process_image(img_path)
            if data:
                # Detect faces
                faces = face_detector.detect_faces(img_path)
                data['faces'] = faces
                data['path'] = img_path
                
                results.append(data)
                new_results_to_save.append((img_path, data['score'], data['tags'], faces))
                
                # Save in batches of 10
                if len(new_results_to_save) >= 10:
                    db.save_images_batch(new_results_to_save)
                    new_results_to_save = []
        
        # Save remaining
        if new_results_to_save:
            db.save_images_batch(new_results_to_save)
                
        # Face Detection & Clustering
        update_progress("clustering", 90, "Grouping faces...")
        
        # Flatten all faces for clustering
        all_faces = []
        for img_data in results:
            for face in img_data.get('faces', []):
                face['image_path'] = img_data.get('path', '') # Ensure path is linked
                all_faces.append(face)
                
        people_clusters = face_detector.cluster_faces(all_faces)
        
        # Format people for frontend
        people = []
        for i, cluster in enumerate(people_clusters):
            if not cluster: continue
            # Use the first face's image as the representative
            people.append({
                "id": str(i),
                "name": f"Person {i+1}",
                "count": len(cluster),
                "images": list(set([f['image_path'] for f in cluster]))
            })
        
        # Theme Detection (Simple tag aggregation)
        themes = {}
        for img in results:
            for tag in img.get('tags', []):
                themes[tag] = themes.get(tag, 0) + 1
                
        sorted_themes = [{'name': k, 'count': v} for k, v in sorted(themes.items(), key=lambda item: item[1], reverse=True)]
        
        update_progress("completed", 100, "Analysis complete")
        progress_state["result"] = {
            "results": results,
            "people": people,
            "themes": sorted_themes
        }

    except Exception as e:
        print(f"Error in background analysis: {e}")
        update_progress("error", 0, f"Error: {str(e)}")

@app.post("/api/analyze")
async def analyze_folder(request: AnalysisRequest, background_tasks: BackgroundTasks):
    # Start background task
    background_tasks.add_task(process_analysis, request)
    return {"status": "started", "message": "Analysis started in background"}

from fastapi import BackgroundTasks

# ... (imports)

def process_video_generation(request: VideoRequest, output_path: str, resolution: tuple, final_images: list):
    try:
        def progress_callback(percentage, **kwargs):
            update_progress("generating", percentage, f"Generating video: {int(percentage)}%")

        update_progress("generating", 0, "Starting video generation...")
        
        # Fetch face data for each image
        images_with_data = []
        for path in final_images:
            data = db.get_image_data(path)
            faces = data.get('faces', []) if data else []
            images_with_data.append({'path': path, 'faces': faces})

        success = video_generator.generate_video(
            images_with_data, 
            request.audio_path, 
            output_path,
            resolution=resolution,
            audio_start=request.audio_start,
            audio_end=request.audio_end,
            image_duration=request.image_duration,
            title_text=request.title_text,
            ken_burns_effect=request.ken_burns_effect,
            progress_callback=progress_callback
        )
        
        if success:
            update_progress("completed", 100, "Video generation complete")
            progress_state["result"] = output_path
        else:
            update_progress("error", 0, "Video generation failed")
            
    except Exception as e:
        print(f"Error in background generation: {e}")
        update_progress("error", 0, f"Error: {str(e)}")

@app.post("/api/generate")
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    resolution = (1920, 1080)
    if request.resolution == "9:16":
        resolution = (1080, 1920)
        
    # Smart Selection: Filter out low quality images if we have enough
    final_images = request.image_paths
    
    # Deduplicate input list just in case
    final_images = list(dict.fromkeys(final_images))

    if len(final_images) < 10:
        return {"status": "error", "message": "Not enough images selected. Please select at least 10 images."}, 400
    
    # Sort images chronologically
    try:
        final_images.sort(key=lambda x: get_image_date(x))
    except Exception as e:
        print(f"Error sorting images: {e}")
        # Fallback to name sort if date sort fails
        final_images.sort()

    if len(final_images) > 20:
        scored_images = []
        for path in final_images:
            data = db.get_image_data(path)
            score = data['score'] if data else 0
            scored_images.append({'path': path, 'score': score})
            
        # Sort by score descending to pick best ones
        scored_images.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep top 80%
        cutoff = int(len(scored_images) * 0.8)
        # Get the paths of the best images
        final_images = [x['path'] for x in scored_images[:cutoff]]
        

        
    # Handle Output Path
    output_path = request.output_path
    if os.path.isdir(output_path) or not output_path.endswith(('.mp4', '.mov', '.avi')):
        # It's a directory (or user just gave a folder path), generate filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"highlight_{timestamp}.mp4"
        if not os.path.exists(output_path):
             # If it doesn't exist and looks like a path, create it
             try:
                 os.makedirs(output_path, exist_ok=True)
             except:
                 # Fallback to current dir if invalid
                 output_path = "."
        
        output_path = os.path.join(output_path, filename)
        
    # Start background task
    background_tasks.add_task(process_video_generation, request, output_path, resolution, final_images)
    
    return {"status": "started", "message": "Video generation started in background"}

# Static Files
# Mount static directory to serve frontend assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

# Catch-all route for SPA
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # API requests should not be handled here, but if they fall through, return 404
    if full_path.startswith("api"):
        return {"error": "Not Found"}, 404
    
    # Serve index.html for any other route (SPA)
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not built yet. Please run 'npm run build' in frontend directory."}


def start():
    """Entry point for the console script"""
    uvicorn.run("video_highlight_generator.main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    start()
