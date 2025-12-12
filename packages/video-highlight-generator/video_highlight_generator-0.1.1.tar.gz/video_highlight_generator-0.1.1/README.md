# Video Highlight Generator

**Video Highlight Generator** is a powerful, standalone AI tool that automatically creates engaging highlight videos from your photo collections. It combines state-of-the-art image analysis, face detection, and smart audio syncing to turn your memories into movies.

## 🚀 Features

-   **🧠 Smart Image Analysis**: Uses **MobileNetV3** to score image quality (sharpness, composition) and classify content.
-   **👤 Face Detection & Clustering**: Detects faces and groups them by person, allowing you to create person-specific highlight reels.
-   **🔍 Theme Detection**: Automatically identifies themes in your photos (e.g., "nature", "people", "urban").
-   **🎵 Audio Studio**:
    -   **Waveform Editor**: Visual audio trimmer to select the perfect segment.
    -   **Custom Audio**: Import your own music tracks.
    -   **Smart Looping**: Automatically loops audio to match video duration.
-   **📱 Multi-Format Export**: Generate videos optimized for **PC/TV (16:9)** or **Smartphone (9:16)**.
-   **📊 Progress Tracking**: Real-time visual progress bars for both image analysis and video generation.
-   **✨ Cinematic Effects**: Smooth cross-fade transitions and custom image duration.
-   **📝 Title Overlay**: Add a custom title to your video.
-   **⚡ Ultra-Fast Caching**: SQLite-based caching ensures instant re-scans and crash resilience.
-   **🎨 Modern Web Interface**: A sleek, dark-mode React frontend for easy folder selection and project management.

![App Screenshot](docs/demo.png)

## 📦 Installation

This tool is packaged as a single Python Wheel file for easy installation.

**Install via PIP**:
    ```
    pip install video-highlight-generator==0.1.1
    ```

## 📚 Documentation

- [Docker Usage Guide](docs/docker_usage.md)
- [Linux Installation Instructions](docs/linux_install_instructions.md)

## 🎮 Usage

1.  **Start the Application**:
    Run the following command in your terminal:
    ```
    video-highlight-generator
    ```

2.  **Open the Web Interface**:
    Open your browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

3.  **Create Your Highlight**:
    -   **Analyze**: Select your photo folders and click "Analyze Images". Watch the progress bar as it scans.
    -   **Review**: See the detected images, identified people, and themes.
    -   **Generate**:
        -   Select images (smart selection automatically picks the best ones).
        -   Choose output resolution (1080p or 9:16).
        -   Add custom audio and trim it using the waveform editor.
        -   Click "Generate Video" and watch the progress.

## 🔧 Development

To develop on this project:

1.  **Backend**:
    -   Install dependencies: `pip install -r requirements.txt` (or manually install from `setup.py`)
    -   Run dev server: `uvicorn video_highlight_generator.main:app --reload`

2.  **Frontend**:
    -   Navigate to `frontend/`
    -   Install dependencies: `npm install`
    -   Run dev server: `npm run dev`

## 📝 License

GNU General Public License v3.0
