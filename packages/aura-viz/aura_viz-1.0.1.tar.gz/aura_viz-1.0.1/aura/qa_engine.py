"""
Interactive Q&A engine using local LLM + embeddings
Uses lightweight Hugging Face models for offline inference
Takes embeddings as context for data understanding
"""

import os
import pandas as pd
import numpy as np
import requests
import json
from pathlib import Path
import torch
from .vision_text_bridge_loader import VisionTextBridgeLoader

class QAEngine:
    """
    Interactive Q&A engine using Mistral + embeddings + VisionTextBridge descriptions
    """
    
    def __init__(self):
        self.data = None
        self.graph_metadata = []
        self.embeddings = None
        self.insights = {}
        
        # API Configuration
        self.api_key = os.getenv("AURA_API_KEY")
        self.api_base = os.getenv("AURA_API_BASE", "https://api.openai.com/v1")
        self.model_name = os.getenv("AURA_MODEL", "gpt-3.5-turbo")
        
        self.use_custom_api = bool(self.api_key)
        self.use_ollama = False if self.use_custom_api else self._check_ollama()
        
        self.vision_bridge = None
        self._load_vision_bridge()
        self.graph_descriptions = []  # Store text descriptions from embeddings
    
    def _check_ollama(self):
        """Check if Ollama is running with Mistral"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                mistral_available = any("mistral" in m.get("name", "").lower() for m in models)
                if mistral_available:
                    print("✓ Ollama with Mistral detected (optimal performance)")
                    return True
                else:
                    print("⚠ Ollama running but Mistral not found. Pull with: ollama pull mistral")
                    return False
            return False
        except:
            print("⚠ Ollama not running. Install from https://ollama.ai/ and run 'ollama pull mistral'")
            return False

    def _load_vision_bridge(self):
        """Load pre-trained VisionTextBridge model"""
        try:
            self.vision_bridge = VisionTextBridgeLoader()
            if self.vision_bridge.model:
                print("✓ VisionTextBridge loaded")
            else:
                print("⚠ VisionTextBridge model not found - will use fallback insights")
        except Exception as e:
            print(f"⚠ Could not load VisionTextBridge: {e}")
    
    def prepare(self, data, graph_metadata, embeddings):
        """Prepare Q&A engine with data and embeddings"""
        self.data = data
        self.graph_metadata = graph_metadata
        self.embeddings = embeddings
        
        self._convert_embeddings_to_descriptions()
        self._compute_insights()
        print(f"✓ Q&A Engine ready with {len(embeddings)} graph embeddings")
    
    def _convert_embeddings_to_descriptions(self):
        """Convert visual embeddings to natural language descriptions"""
        print("🌉 Converting embeddings to text descriptions...")
        
        if self.vision_bridge is None:
            print("⚠ Using fallback descriptions")
            self.graph_descriptions = [f"Graph {i}: Data visualization" for i in range(len(self.embeddings))]
            return
        
        try:
            # VisionTextBridgeLoader processes all embeddings at once
            descriptions = self.vision_bridge.convert_embeddings_to_insights(self.embeddings)
            self.graph_descriptions = descriptions
            
            print(f"✓ Generated {len(self.graph_descriptions)} text descriptions")
        except Exception as e:
            print(f"⚠ Error converting embeddings: {e}")
            self.graph_descriptions = [f"Graph {i}: Data visualization" for i in range(len(self.embeddings))]
    
    def _compute_insights(self):
        """Compute data insights from embeddings and data"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        embedding_stats = {
            "embedding_shape": self.embeddings.shape,
            "embedding_mean": float(np.mean(self.embeddings)),
            "embedding_std": float(np.std(self.embeddings)),
        }
        
        self.insights = {
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "dtypes": self.data.dtypes.to_dict(),
            "correlations": self.data[numeric_cols].corr().to_dict() if len(numeric_cols) > 0 else {},
            "missing_data": (self.data.isnull().sum() / len(self.data) * 100).to_dict(),
            "duplicates": len(self.data) - len(self.data.drop_duplicates()),
            "stats": self.data[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {},
            "graphs": [g.get('name', 'Unknown') for g in self.graph_metadata],
            "embeddings": embedding_stats,
        }

    def answer(self, question: str) -> str:
        """Answer user questions using LLM + embeddings"""
        try:
            # Build rich context from embeddings + descriptions
            context = self._build_context()
            
            descriptions_context = "\n".join(self.graph_descriptions[:5])  # Top 5 descriptions
            
            prompt = f"""You are an expert data analyst. Analyze the user's question based on visual insights from embeddings.

DATASET CONTEXT:
{context}

VISUAL INSIGHTS FROM EMBEDDINGS:
{descriptions_context}

USER QUESTION: {question}

Provide a concise, insightful analysis based on the visual patterns."""
            
            if self.use_custom_api:
                return self._generate_with_custom_api(prompt)
            elif self.use_ollama:
                return self._generate_with_ollama(prompt)
            else:
                return self._generate_fallback_insight(question)
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_with_custom_api(self, prompt: str) -> str:
        """Generate response using custom API (OpenAI compatible)"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            else:
                return f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"API Connection Error: {str(e)}"

    def _generate_with_ollama(self, prompt: str) -> str:
        """Generate response using Mistral via Ollama"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                return result if result else self._generate_fallback_insight("")
            return self._generate_fallback_insight("")
        
        except Exception as e:
            return self._generate_fallback_insight("")
    
    def _generate_fallback_insight(self, question: str) -> str:
        """Generate insights without model when unavailable"""
        q_lower = question.lower()
        
        if "correlation" in q_lower:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr = self.data[numeric_cols].corr()
                top_corr = corr.unstack().sort_values(ascending=False)
                return f"Correlations found: {top_corr[top_corr < 1].head(3).to_string()}"
            return "No numeric columns for correlation analysis."
        
        elif "missing" in q_lower:
            missing = self.data.isnull().sum()
            missing = missing[missing > 0]
            if len(missing) > 0:
                return f"Missing data detected:\n{missing.to_string()}"
            return "✓ No missing data found."
        
        elif "quality" in q_lower:
            total = len(self.data)
            duplicates = self.insights['duplicates']
            missing_pct = sum(self.insights['missing_data'].values())
            quality = 100 - (duplicates/total * 100) - missing_pct/max(len(self.insights['missing_data']), 1)
            return f"Data Quality Score: {max(0, quality):.1f}%\nDuplicates: {duplicates}\nMissing: {missing_pct:.1f}%"
        
        elif "outlier" in q_lower:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                outliers = []
                for col in numeric_cols:
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outlier_count = len(self.data[(self.data[col] < Q1 - 1.5*IQR) | (self.data[col] > Q3 + 1.5*IQR)])
                    if outlier_count > 0:
                        outliers.append(f"{col}: {outlier_count}")
                if outliers:
                    return "Outliers detected in:\n" + "\n".join(outliers)
                return "✓ No significant outliers found."
            return "No numeric data for analysis."
        
        else:
            summary = f"Dataset: {self.insights['shape'][0]} rows × {self.insights['shape'][1]} columns"
            cols_str = ", ".join(self.insights['columns'][:5])
            return f"{summary}\nColumns: {cols_str}..."
    
    def _build_context(self) -> str:
        """Build rich context from data and embeddings"""
        context = []
        
        context.append(f"Shape: {self.insights['shape'][0]} rows × {self.insights['shape'][1]} columns")
        context.append(f"Columns: {', '.join(self.insights['columns'][:10])}")
        
        # Missing data
        missing = {k: v for k, v in self.insights['missing_data'].items() if v > 0}
        if missing:
            context.append(f"Missing: {missing}")
        
        # Duplicates
        if self.insights['duplicates'] > 0:
            context.append(f"Duplicates: {self.insights['duplicates']}")
        
        # Graphs
        if self.insights['graphs']:
            context.append(f"Visualizations: {', '.join(self.insights['graphs'][:5])}")
        
        return "\n".join(context)
