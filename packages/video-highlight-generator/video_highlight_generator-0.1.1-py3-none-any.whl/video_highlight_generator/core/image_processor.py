import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np
import os

class ImageProcessor:
    def __init__(self):
        # Load pre-trained MobileNetV3
        self.model = models.mobilenet_v3_small(pretrained=True)
        self.model.eval()
        
        # Standard ImageNet normalization
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        # Load ImageNet labels (simplified for this example)
        self.labels = self._load_labels()

    def _load_labels(self):
        # Placeholder for actual ImageNet labels
        # In a real app, you'd load these from a file
        return {i: f"class_{i}" for i in range(1000)}

    def process_image(self, image_path):
        try:
            # Handle non-ASCII paths for OpenCV
            with open(image_path, "rb") as f:
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
                cv_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if cv_img is None:
                return None

            # Calculate sharpness using Laplacian
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Prepare for PyTorch
            # Convert BGR (OpenCV) to RGB (PIL)
            img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            
            input_tensor = self.preprocess(pil_img)
            input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

            with torch.no_grad():
                output = self.model(input_batch)
            
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            score = probabilities.max().item()
            
            # Get top predicted class as tag (placeholder logic)
            top_prob, top_catid = torch.topk(probabilities, 1)
            
            # Combine confidence and sharpness for a quality score
            # Normalize sharpness roughly (0-1000 to 0-1)
            final_score = score * 0.7 + (min(sharpness, 1000) / 1000) * 0.3
            
            return {
                "score": final_score,
                "tags": [str(top_catid.item())], # In real app, map to text
                "sharpness": sharpness
            }
        except Exception as e:
            print(f"Error analyzing {image_path}: {e}")
            return None
