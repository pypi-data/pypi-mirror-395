"""
Core AURA class - main entry point for users
"""

import pandas as pd
import numpy as np
from pathlib import Path
from .graph_generator import GraphGenerator
from .feature_extractor import FeatureExtractor
from .qa_engine import QAEngine
from .gui import AuraGUI


class Aura:
    """
    Main AURA class for data visualization and interactive Q&A
    
    Usage:
        aura = Aura()
        aura.load_data("data.csv")
        aura.generate_insights()
        aura.launch_gui()
    """
    
    def __init__(self):
        self.data = None
        self.graphs = []
        self.embeddings = None
        self.graph_metadata = []
        self.qa_engine = QAEngine()
        self.gui = None
    
    def load_data(self, csv_path: str) -> None:
        """Load and validate CSV data"""
        try:
            print(f"\n📂 Loading data from {csv_path}...")
            self.data = pd.read_csv(csv_path)
            print(f"✓ Loaded: {self.data.shape[0]} rows × {self.data.shape[1]} columns")
            self._validate_data()
        except Exception as e:
            raise ValueError(f"Error loading CSV: {str(e)}")
    
    def _validate_data(self) -> None:
        """Validate data quality"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            raise ValueError("Need at least 2 numeric columns for analysis")
        print(f"  ✓ Data validation passed ({len(numeric_cols)} numeric columns)")
    
    def generate_insights(self) -> dict:
        """Generate 15 graphs and extract features"""
        if self.data is None:
            raise ValueError("Load data first using load_data()")
        
        print("\n📊 Generating 15 graphs...")
        graph_gen = GraphGenerator(self.data)
        self.graphs, self.graph_metadata = graph_gen.create_all_graphs()
        print(f"✓ Created {len(self.graphs)} graphs")
        
        print("🔍 Extracting visual features...")
        extractor = FeatureExtractor()
        self.embeddings = extractor.extract_features(self.graphs)
        print(f"✓ Embeddings shape: {self.embeddings.shape}")
        
        self.qa_engine.prepare(self.data, self.graph_metadata, self.embeddings)
        
        insights = {
            "total_graphs": len(self.graphs),
            "data_shape": self.data.shape,
            "embeddings_shape": self.embeddings.shape,
            "numeric_columns": len(self.data.select_dtypes(include=[np.number]).columns),
        }
        
        print("✓ Insights ready! Ask questions about your data.")
        return insights
    
    def ask(self, question: str) -> str:
        """Interactive Q&A about the data"""
        if self.embeddings is None:
            raise ValueError("Generate insights first using generate_insights()")
        
        answer = self.qa_engine.answer(question)
        return answer
    
    def get_data_flaws(self) -> dict:
        """Identify data quality issues"""
        if self.data is None:
            raise ValueError("Load data first")
        
        flaws = {
            "missing_values": self.data.isnull().sum().to_dict(),
            "duplicates": len(self.data) - len(self.data.drop_duplicates()),
            "numeric_stats": self.data.describe().to_dict(),
        }
        
        return flaws
    
    def launch_gui(self) -> None:
        """Launch interactive Tkinter GUI for Q&A"""
        if self.embeddings is None:
            raise ValueError("Generate insights first using generate_insights()")
        
        print("\n🎨 Launching interactive GUI...")
        self.gui = AuraGUI(self)
        self.gui.launch()
