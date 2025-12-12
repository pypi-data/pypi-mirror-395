"""
Load pre-trained VisionTextBridge model (best_model.h5)
Converts embeddings to text insights
"""

import os
import numpy as np
from pathlib import Path

class VisionTextBridgeLoader:
    """Load and use pre-trained VisionTextBridge model"""
    
    def __init__(self):
        self.model = None
        self.model_path = None
        self._find_and_load_model()
    
    def _find_and_load_model(self):
        """Find and load best_model.h5 from TextVisionBridge folder"""
        try:
            import tensorflow as tf
            from tensorflow import keras
            import requests
            from tqdm import tqdm
            
            # 1. Define model path (User Home Directory for persistence)
            home_dir = Path.home() / ".aura" / "models"
            home_dir.mkdir(parents=True, exist_ok=True)
            model_path = home_dir / "best_model.h5"
            
            # 2. Check if model exists, if not download it
            if not model_path.exists():
                print(f"⬇️ Model not found at {model_path}")
                print("⬇️ Downloading pre-trained VisionTextBridge model (158 MB)...")
                # DOWNLOAD URL from your GitHub Release
                url = "https://github.com/hanish9193/AURA/releases/download/v1.0.0/best_model.h5"
                
                try:
                    response = requests.get(url, stream=True)
                    total_size = int(response.headers.get('content-length', 0))
                    
                    with open(model_path, 'wb') as f, tqdm(
                        desc="Downloading",
                        total=total_size,
                        unit='iB',
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar:
                        for data in response.iter_content(chunk_size=1024):
                            size = f.write(data)
                            bar.update(size)
                    print("✓ Download complete")
                except Exception as e:
                    print(f"❌ Failed to download model: {e}")
                    print("⚠ Please manually download 'best_model.h5' and place it in ~/.aura/models/")
                    self.model = None
                    return

            # 3. Load the model
            print(f"📦 Loading VisionTextBridge model from {model_path}...")
            self.model = keras.models.load_model(str(model_path))
            self.model_path = model_path
            print(f"✓ VisionTextBridge model loaded successfully")
            
        except ImportError:
            print("⚠ TensorFlow not available. VisionTextBridge will not be used.")
            self.model = None
        except Exception as e:
            print(f"⚠ Error loading VisionTextBridge model: {str(e)}")
            import traceback
            traceback.print_exc()
            self.model = None
    
    def convert_embeddings_to_insights(self, embeddings):
        """
        Convert embeddings to text insights using VisionTextBridge
        
        Args:
            embeddings: (n_graphs, 2560) array from EfficientNetB7
        
        Returns:
            List of text descriptions for each graph
        """
        if self.model is None:
            return self._generate_fallback_insights(embeddings)
        
        try:
            # Pass embeddings through model
            predictions = self.model.predict(embeddings, verbose=0)
            insights = self._decode_predictions(predictions)
            return insights
            
        except Exception as e:
            print(f"⚠ Error converting embeddings: {str(e)}")
            return self._generate_fallback_insights(embeddings)
    
    def _decode_predictions(self, predictions):
        """Decode model predictions to text insights"""
        insights = []
        
        for pred in predictions:
            # Determine dominant classes
            if len(pred.shape) > 1:  # Multi-class output
                top_classes = np.argsort(pred[0])[-3:][::-1]
                confidence = pred[0][top_classes]
            else:
                top_classes = [np.argmax(pred)]
                confidence = [np.max(pred)]
            
            # Map to insights
            insight_text = self._class_to_insight(top_classes, confidence)
            insights.append(insight_text)
        
        return insights
    
    def _class_to_insight(self, classes, confidence):
        """Map class predictions to meaningful insights"""
        class_names = {
            0: "shows a positive trend",
            1: "shows a negative trend",
            2: "shows no clear trend",
            3: "has high variability",
            4: "has low variability",
            5: "contains outliers",
            6: "has clusters",
            7: "is normally distributed",
            8: "is skewed",
            9: "has multiple modes",
        }
        
        insights_list = []
        for cls, conf in zip(classes, confidence):
            if cls in class_names:
                insights_list.append(f"{class_names[cls]} (confidence: {conf:.2f})")
        
        return " | ".join(insights_list) if insights_list else "Graph shows data patterns"
    
    def _generate_fallback_insights(self, embeddings):
        """Generate fallback insights without VisionTextBridge"""
        insights = []
        
        for emb in embeddings:
            # Analyze embedding statistics
            mean_val = np.mean(emb)
            std_val = np.std(emb)
            energy = np.sum(emb ** 2)
            
            if energy > np.percentile([np.sum(e**2) for e in embeddings], 75):
                insight = "shows significant data variation with high feature complexity"
            elif std_val > 0.5:
                insight = "demonstrates moderate pattern diversity"
            else:
                insight = "shows relatively uniform data distribution"
            
            insights.append(insight)
        
        return insights

if __name__ == "__main__":
    print("🚀 Testing VisionTextBridgeLoader...")
    loader = VisionTextBridgeLoader()
    
    if loader.model:
        print("\n✅ SUCCESS: VisionTextBridge model loaded!")
        
        # Create dummy embedding for testing
        print("\n🧪 Testing inference with dummy data...")
        dummy_embedding = np.random.rand(1, 2560) # EfficientNetB7 output size
        try:
            insights = loader.convert_embeddings_to_insights(dummy_embedding)
            print(f"📝 Generated Insight: {insights}")
        except Exception as e:
            print(f"❌ Inference failed: {e}")
    else:
        print("\n❌ FAILURE: Could not load VisionTextBridge model.")
