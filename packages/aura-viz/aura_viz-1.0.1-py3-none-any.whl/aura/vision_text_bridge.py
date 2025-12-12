"""
VisionTextBridge: Neural module that converts EfficientNetB0 embeddings (1280-D) 
to meaningful text descriptions for downstream LLM consumption.

Flow: 1280-D embeddings → semantic projection (4096-D) → learned attributes 
→ natural language descriptions that Mistral can understand
"""

import torch
import torch.nn as nn
import numpy as np
from pathlib import Path


class VisionTextBridge(nn.Module):
    """
    Neural adapter that bridges visual embeddings to semantic language space.
    
    Converts 1280-D CNN embeddings → text descriptions of visual patterns
    (correlations, trends, outliers, distributions)
    """
    
    def __init__(self, embedding_dim=1280, semantic_dim=4096):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.semantic_dim = semantic_dim
        
        self.projection = nn.Sequential(
            nn.Linear(embedding_dim, 2048),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(2048, semantic_dim),
            nn.LayerNorm(semantic_dim)
        )
        
        self.semantic_refiner = nn.Sequential(
            nn.Linear(semantic_dim, 2048),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(2048, semantic_dim)
        )
        
        self.trend_head = nn.Sequential(
            nn.Linear(semantic_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 3)
        )
        
        self.density_head = nn.Sequential(
            nn.Linear(semantic_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 3)
        )
        
        self.outlier_head = nn.Sequential(
            nn.Linear(semantic_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 2)
        )
        
        self.shape_head = nn.Sequential(
            nn.Linear(semantic_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 4)
        )
    
    def forward(self, embeddings):
        """
        Convert embeddings to semantic vectors + extract visual attributes
        
        Args:
            embeddings: (batch_size, 1280) tensor of CNN features
            
        Returns:
            semantic_vectors: (batch_size, 4096) semantic representations
            attributes: dict with RAW LOGITS (not softmax)
        """
        semantic = self.projection(embeddings)
        semantic = self.semantic_refiner(semantic)
        
        trend = self.trend_head(semantic)
        density = self.density_head(semantic)
        outliers = self.outlier_head(semantic)
        shape = self.shape_head(semantic)
        
        attributes = {
            'trend': trend,
            'density': density,
            'outliers': outliers,
            'shape': shape
        }
        
        return semantic, attributes
    
    def describe_embedding(self, embedding, metadata=None):
        """
        Convert single embedding to natural language description
        
        Args:
            embedding: (1280,) numpy array or torch tensor
            metadata: dict with graph_name, etc.
            
        Returns:
            description: str describing visual patterns
            semantic: semantic representation
        """
        if isinstance(embedding, np.ndarray):
            embedding = torch.from_numpy(embedding).unsqueeze(0).float()
        elif embedding.dim() == 1:
            embedding = embedding.unsqueeze(0)
        
        with torch.no_grad():
            semantic, attribute_logits = self.forward(embedding)
        
        trend_probs = torch.softmax(attribute_logits['trend'], dim=1)
        density_probs = torch.softmax(attribute_logits['density'], dim=1)
        outlier_probs = torch.softmax(attribute_logits['outliers'], dim=1)
        shape_probs = torch.softmax(attribute_logits['shape'], dim=1)
        
        trend_idx = trend_probs.argmax(dim=1).item()
        density_idx = density_probs.argmax(dim=1).item()
        outlier_idx = outlier_probs.argmax(dim=1).item()
        shape_idx = shape_probs.argmax(dim=1).item()
        
        trend_names = ['negative trend', 'flat trend', 'positive trend']
        density_names = ['sparse data', 'clustered data', 'dense data']
        outlier_names = ['no outliers', 'has outliers']
        shape_names = ['uniform distribution', 'skewed distribution', 'bimodal distribution', 'irregular shape']
        
        description = f"Visual pattern: {trend_names[trend_idx]}, {density_names[density_idx]}, {outlier_names[outlier_idx]}, {shape_names[shape_idx]}."
        
        if metadata and 'name' in metadata:
            description = f"[{metadata['name']}] {description}"
        
        return description, semantic.squeeze(0).cpu().numpy()


def train_vision_text_bridge(embeddings, labels, epochs=20, device='cpu'):
    """
    Supervised training with ground-truth labels and CrossEntropyLoss
    
    Args:
        embeddings: (n_graphs, 1280) array of CNN features
        labels: dict with keys ['trend', 'density', 'outliers', 'shape']
               each containing (n_graphs,) integer class indices
        epochs: training epochs
        device: 'cpu' or 'cuda'
        
    Returns:
        model: trained VisionTextBridge
    """
    if isinstance(embeddings, np.ndarray):
        embeddings = torch.from_numpy(embeddings).float()
    
    embeddings = embeddings.to(device)
    
    # Convert labels to tensors
    trend_labels = torch.tensor(labels['trend'], dtype=torch.long).to(device)
    density_labels = torch.tensor(labels['density'], dtype=torch.long).to(device)
    outlier_labels = torch.tensor(labels['outliers'], dtype=torch.long).to(device)
    shape_labels = torch.tensor(labels['shape'], dtype=torch.long).to(device)
    
    model = VisionTextBridge().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    criterion = nn.CrossEntropyLoss()
    
    print("🎓 Training VisionTextBridge with SUPERVISED labels...")
    
    for epoch in range(epochs):
        model.train()
        
        # Get raw logits from model
        semantic, attribute_logits = model(embeddings)
        
        # Calculate supervised loss against ground-truth labels
        loss_trend = criterion(attribute_logits['trend'], trend_labels)
        loss_density = criterion(attribute_logits['density'], density_labels)
        loss_outlier = criterion(attribute_logits['outliers'], outlier_labels)
        loss_shape = criterion(attribute_logits['shape'], shape_labels)
        
        loss = loss_trend + loss_density + loss_outlier + loss_shape
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % max(1, epochs // 5) == 0:
            print(f"  Epoch {epoch + 1}/{epochs} - Loss: {loss.item():.4f}")
    
    print("✓ VisionTextBridge trained with supervision!")
    return model


def save_model(model, path="models/vision_text_bridge.pt"):
    """Save trained model"""
    Path(path).parent.mkdir(exist_ok=True)
    torch.save(model.state_dict(), path)
    print(f"✓ Model saved to {path}")


def load_model(path="models/vision_text_bridge.pt", device='cpu'):
    """Load trained model"""
    model = VisionTextBridge().to(device)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model
