"""
Generate 15 different graphs for data visualization
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64


class GraphGenerator:
    """Generate 15 diverse graphs from CSV data"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        sns.set_style("whitegrid")
    
    def create_all_graphs(self) -> tuple:
        """Create all graphs in parallel with progress bar"""
        from tqdm import tqdm
        import concurrent.futures
        import sys
        
        tasks = []
        
        # 1. Correlation Heatmap
        tasks.append((self._correlation_heatmap, (), {"type": "heatmap", "name": "Correlation Matrix"}))
        
        # 2-4. Distribution plots (first 3 numeric columns)
        for col in self.numeric_cols[:3]:
            tasks.append((self._distribution_plot, (col,), {"type": "distribution", "name": f"Distribution: {col}"}))
        
        # 5-7. Scatter plots (pairs of numeric columns)
        for i in range(min(3, len(self.numeric_cols)-1)):
            tasks.append((self._scatter_plot, (self.numeric_cols[i], self.numeric_cols[i+1]), {"type": "scatter", "name": f"Relationship: {self.numeric_cols[i]} vs {self.numeric_cols[i+1]}"}))
        
        # 8-10. Box plots (first 3 numeric columns)
        for col in self.numeric_cols[:3]:
            tasks.append((self._box_plot, (col,), {"type": "boxplot", "name": f"Outliers: {col}"}))
        
        # 11-13. Category counts (first 3 categorical columns)
        for col in self.categorical_cols[:3]:
            tasks.append((self._category_bar_plot, (col,), {"type": "bar", "name": f"Categories: {col}"}))
        
        # 14. Data quality
        tasks.append((self._missing_data_plot, (), {"type": "missing", "name": "Data Quality"}))
        
        # 15. Feature importance via variance
        tasks.append((self._variance_plot, (), {"type": "variance", "name": "Feature Importance"}))
        
        graphs = []
        metadata = []
        
        # Execute in parallel
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Submit all tasks
            future_to_meta = {executor.submit(func, *args): meta for func, args, meta in tasks}
            
            # Process as they complete with progress bar
            for future in tqdm(concurrent.futures.as_completed(future_to_meta), total=len(tasks), desc="Generating Graphs", unit="graph", file=sys.stdout):
                meta = future_to_meta[future]
                try:
                    graph_bytes = future.result()
                    graphs.append(graph_bytes)
                    metadata.append(meta)
                except Exception as e:
                    print(f"⚠ Error generating {meta['name']}: {e}")
        
        return graphs, metadata
    
    def _correlation_heatmap(self):
        """Correlation heatmap"""
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = self.data[self.numeric_cols].corr()
            sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, cbar_kws={'label': 'Correlation'})
            ax.set_title("Correlation Matrix", fontsize=14, fontweight='bold')
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()
    
    def _distribution_plot(self, col):
        """Distribution histogram"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(self.data[col].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_title(f"Distribution: {col}", fontsize=12, fontweight='bold')
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()
    
    def _scatter_plot(self, col1, col2):
        """Scatter plot"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(self.data[col1], self.data[col2], alpha=0.6, s=50, color='steelblue')
            ax.set_title(f"{col1} vs {col2}", fontsize=12, fontweight='bold')
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()
    
    def _box_plot(self, col):
        """Box plot for outlier detection"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.boxplot(self.data[col].dropna())
            ax.set_title(f"Outlier Detection: {col}", fontsize=12, fontweight='bold')
            ax.set_ylabel(col)
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()
    
    def _category_bar_plot(self, col):
        """Bar plot for categories"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            counts = self.data[col].value_counts()
            ax.bar(range(len(counts)), counts.values, color='steelblue')
            ax.set_xticks(range(len(counts)))
            ax.set_xticklabels(counts.index, rotation=45, ha='right')
            ax.set_title(f"Categories: {col}", fontsize=12, fontweight='bold')
            ax.set_ylabel("Count")
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()
    
    def _missing_data_plot(self):
        """Missing data visualization"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            missing = (self.data.isnull().sum() / len(self.data)) * 100
            missing = missing[missing > 0]
            if len(missing) > 0:
                ax.barh(missing.index, missing.values, color='coral')
                ax.set_xlabel("Missing %")
                ax.set_title("Data Quality Issues", fontsize=12, fontweight='bold')
            else:
                ax.text(0.5, 0.5, "No Missing Data", ha='center', va='center', fontsize=14)
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()
    
    def _variance_plot(self):
        """Feature importance by variance"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            variance = self.data[self.numeric_cols].var()
            variance = variance / variance.max()  # Normalize
            ax.barh(variance.index, variance.values, color='seagreen')
            ax.set_xlabel("Normalized Variance")
            ax.set_title("Feature Importance", fontsize=12, fontweight='bold')
            return self._fig_to_bytes(fig)
        except Exception:
            plt.close()
            return self._empty_plot()

    def _empty_plot(self):
        """Return empty plot on error"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, "Error Generating Plot", ha='center', va='center')
        return self._fig_to_bytes(fig)
    
    @staticmethod
    def _fig_to_bytes(fig):
        """Convert matplotlib figure to bytes"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return buf.getvalue()
