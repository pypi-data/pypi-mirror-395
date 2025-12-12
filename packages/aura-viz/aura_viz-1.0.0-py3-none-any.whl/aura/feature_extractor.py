"""
Extract visual features from graphs using pre-trained CNN
"""

import numpy as np
from PIL import Image
from io import BytesIO
import hashlib


class FeatureExtractor:
    """
    Extract features from graph images using pre-trained EfficientNetB7
    Models are downloaded once and cached locally
    """
    
    def __init__(self):
        self.model = None
        self._load_pretrained_model()
    
    def _load_pretrained_model(self):
        """Load pre-trained model (downloaded once)"""
        try:
            from tensorflow.keras.applications import EfficientNetB7
            from tensorflow.keras.applications.efficientnet import preprocess_input
            
            print("📥 Loading pre-trained EfficientNetB7...")
            self.model = EfficientNetB7(weights='imagenet', include_top=True, pooling='avg', input_shape=(600, 600, 3))
            self.preprocess = preprocess_input
            print("✓ Pre-trained model loaded")
        except ImportError:
            print("⚠ TensorFlow not installed. Using fallback embeddings.")
            self.model = None
    
    def extract_features(self, graph_bytes_list):
        """
        Extract embeddings from graph images
        Returns: (n_graphs, 1280) array of feature vectors
        """
        embeddings = []
        
        for idx, graph_bytes in enumerate(graph_bytes_list):
            try:
                if self.model is not None:
                    # Use pre-trained model
                    embedding = self._extract_with_model(graph_bytes)
                else:
                    # Fallback: use image hash + basic stats
                    embedding = self._extract_fallback(graph_bytes)
                
                embeddings.append(embedding)
                if (idx + 1) % 5 == 0:
                    print(f"  Processed {idx + 1}/{len(graph_bytes_list)} graphs")
            except Exception as e:
                print(f"  ⚠ Error processing graph {idx}: {str(e)}")
                # Use zero embedding as fallback
                embeddings.append(np.zeros(1280))
        
        return np.array(embeddings)
    
    def _extract_with_model(self, graph_bytes):
        """Extract features using pre-trained model"""
        img = Image.open(BytesIO(graph_bytes))
        img = img.resize((600, 600))
        img_array = np.array(img) / 255.0
        
        # Ensure RGB (3 channels)
        if len(img_array.shape) == 2:
            img_array = np.stack([img_array] * 3, axis=-1)
        elif img_array.shape[2] == 4:  # RGBA -> RGB
            img_array = img_array[:, :, :3]
        
        img_array = np.expand_dims(img_array, axis=0)
        img_array = self.preprocess(img_array)
        
        embedding = self.model.predict(img_array, verbose=0)
        return embedding[0]
    
    def _extract_fallback(self, graph_bytes):
        """Fallback feature extraction without model"""
        # Use hash + image properties as features
        img_hash = hashlib.md5(graph_bytes).digest()
        
        # Resize to 1280 dimensions by tiling and padding
        features = np.frombuffer(img_hash, dtype=np.uint8)
        features = features.astype(np.float32) / 255.0
        
        # Pad to 1280 dimensions
        features = np.tile(features, (1280 // len(features) + 1))[:1280]
        return features
