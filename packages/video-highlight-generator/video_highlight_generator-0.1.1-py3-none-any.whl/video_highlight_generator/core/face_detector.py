from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np

class FaceDetector:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

    def detect_faces(self, image_path: str):
        try:
            img = Image.open(image_path).convert('RGB')
            # Detect faces
            boxes, probs = self.mtcnn.detect(img)
            
            faces_data = []
            if boxes is not None:
                # Get embeddings
                faces_aligned = self.mtcnn(img)
                if faces_aligned is not None:
                    embeddings = self.resnet(faces_aligned.to(self.device)).detach().cpu().numpy()
                    
                    for i, box in enumerate(boxes):
                        faces_data.append({
                            "box": box.tolist(),
                            "prob": float(probs[i]),
                            "embedding": embeddings[i].tolist()
                        })
            return faces_data
        except Exception as e:
            print(f"Error detecting faces in {image_path}: {e}")
            return []

    def cluster_faces(self, all_faces_data, threshold=0.8):
        """
        Groups faces by similarity.
        all_faces_data: List of dicts, each containing 'embedding' (list) and 'image_path'.
        Returns: List of clusters (each cluster is a list of image_paths).
        """
        if not all_faces_data:
            return []
            
        embeddings = torch.tensor([f['embedding'] for f in all_faces_data]).to(self.device)
        n = len(embeddings)
        
        # Calculate distance matrix
        dists = torch.cdist(embeddings, embeddings)
        
        # Simple greedy clustering
        clusters = []
        visited = set()
        
        for i in range(n):
            if i in visited:
                continue
                
            # Start a new cluster with this face
            current_cluster = [all_faces_data[i]]
            visited.add(i)
            
            # Find all similar faces
            for j in range(i + 1, n):
                if j in visited:
                    continue
                
                if dists[i, j] < threshold:
                    current_cluster.append(all_faces_data[j])
                    visited.add(j)
            
            clusters.append(current_cluster)
            
        return clusters
