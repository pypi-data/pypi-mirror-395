from setuptools import setup, find_packages

setup(
    name="video_highlight_generator",
    version="0.1.1",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "opencv-python",
        "torch",
        "facenet-pytorch",
        "moviepy>=2.0.0.dev0",
        "numpy>=2.0.0",
        "Pillow",
        "python-multipart",
        "aiofiles"
    ],
    entry_points={
        "console_scripts": [
            "video-highlight-generator=video_highlight_generator.main:start",
        ],
    },
)
