# AURA: Artificial Understanding and Reasoning Assistant

[![PyPI version](https://badge.fury.io/py/aura-viz.svg)](https://badge.fury.io/py/aura-viz)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**What if AI could see your data the way you do?**

AURA transforms data visualization from a manual interpretation task into an automated, AI-powered insight engine. Upload your dataset, and AURA generates comprehensive visualizations while simultaneously analyzing patterns, trends, and anomalies through computer vision and natural language.

---

## Why AURA?

Traditional data analysis tools generate charts—but you still need to interpret them. AURA goes further: it **sees** your visualizations, understands statistical patterns, and explains insights in plain English.

**The Challenge**  
Most AI systems analyze only text-based statistics (means, correlations, standard deviations). They're blind to what humans see instantly in charts: clusters, outliers, distributions, trends.

**The Solution**  
AURA combines automated visualization generation with a specialized vision model trained on 100,000 scientific plots. The result: AI that genuinely understands your data's visual story.

---

## Core Features

**Comprehensive Visualization Suite**  
Automatically generates 50+ chart types from your CSV data—correlation matrices, scatter plots, distribution plots, box plots, violin plots, heatmaps, and advanced statistical graphics.

**AI Vision Model**  
The VisionTextBridge neural network analyzes each visualization to detect:
- Trends (positive, negative, stable relationships)
- Density patterns (sparse, clustered, dense distributions)
- Outliers (statistical anomalies using IQR methods)
- Shape characteristics (uniform, skewed, bimodal, irregular)

**Natural Language Insights**  
Converts visual patterns into human-readable explanations. Instead of staring at dozens of charts, get instant interpretations like: *"Strong positive correlation detected (r=0.87). Data shows right-skewed distribution with three significant outliers."*

**Interactive Q&A**  
Ask questions about your data in plain English. AURA grounds responses in actual visual patterns it detected, not just statistical summaries.

**Privacy-First Architecture**  
Runs completely offline using local Mistral-7B model—ideal for sensitive healthcare, financial, or proprietary business data. Cloud API integration (GPT-4, Azure OpenAI) available when needed.

**Blazing Fast**  
Lightweight 1.2M parameter vision model delivers sub-second inference on standard CPUs. No GPU required. Full analysis of 50 visualizations completes in under 15 seconds.

---

## Installation

```bash
pip install aura-viz
```

**Requirements**: Python 3.9+, 2GB RAM, 200MB disk space  
**Note**: Import as `aura` (package name is `aura-viz`)

---

## Quick Start

### Basic Usage

```python
from aura import Aura

# Initialize
analyzer = Aura()

# Load your data
analyzer.load_data("sales_data.csv")

# Generate visualizations + AI analysis
# (First run auto-downloads 150MB vision model)
analyzer.generate_insights()

# Launch interactive dashboard
analyzer.start_interactive_mode()
```

That's it. AURA handles the rest—chart generation, pattern detection, and interactive exploration.

---

## Example Workflow

```python
from aura import Aura

# 1. Initialize and load data
app = Aura()
app.load_data("customer_transactions.csv")

# 2. Generate comprehensive analysis
app.generate_insights()

# Example output:
# "Analyzing correlation heatmap... Stable trend (87% confidence), 
#  Dense distribution (92%), No outliers detected (95%)"
#
# "Analyzing price vs quantity scatter... Strong negative correlation 
#  (r=-0.76), Medium density (81%), 3 outliers present (88%)"

# 3. Ask questions interactively
app.start_interactive_mode()

# In the dashboard, you can ask:
# "What relationships exist between price and purchase frequency?"
# "Are there any unusual patterns in customer behavior?"
# "Which features show the strongest correlations?"
```

---

## Configuration Options

### Using Local Models (Offline)

Default configuration uses Ollama with Mistral-7B for complete privacy:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral
ollama pull mistral

# AURA auto-detects and uses local model
```

### Using Cloud APIs

For enhanced capabilities, configure OpenAI or Azure:

**Linux/Mac**:
```bash
export AURA_API_KEY="sk-your-key-here"
export AURA_MODEL="gpt-4"
```

**Windows PowerShell**:
```powershell
$env:AURA_API_KEY="sk-your-key-here"
$env:AURA_MODEL="gpt-4"
```

**Python**:
```python
import os
os.environ["AURA_API_KEY"] = "sk-your-key-here"
os.environ["AURA_MODEL"] = "gpt-4"
```

---

## How It Works

AURA operates through a six-stage pipeline:

1. **Data Loading**: Parse and validate CSV input
2. **Visualization Generation**: Create 50+ diverse plot types using matplotlib/seaborn
3. **Visual Encoding**: Extract 2560-dimensional features using EfficientNetB7
4. **Pattern Recognition**: VisionTextBridge classifies trends, density, outliers, and shapes
5. **Language Synthesis**: Convert visual patterns into natural language descriptions
6. **Interactive Query**: Enable conversational exploration via LLM integration

The secret sauce is **VisionTextBridge**—a compact 1.2M parameter neural network trained specifically on scientific visualizations. Unlike generic vision models trained on photos, it understands statistical patterns in charts.

---

## Use Cases

**Healthcare & Life Sciences**  
Analyze clinical trial data, patient outcomes, and epidemiological trends offline with HIPAA compliance.

**Finance & Trading**  
Identify market patterns, portfolio correlations, and risk indicators while maintaining data privacy.

**Business Analytics**  
Enable non-technical teams to explore sales data, customer behavior, and operational metrics through natural language.

**Scientific Research**  
Accelerate exploratory data analysis across experimental datasets with automated pattern detection.

**Education**  
Help students learn statistical concepts through interactive visualization and AI-guided interpretation.

---

## Performance Benchmarks

| Metric | Performance |
|--------|-------------|
| Vision Model Size | 1.2M parameters |
| Inference Speed | 12ms per chart (CPU) |
| Memory Usage | 1.2GB peak |
| Full Analysis Time | ~14 seconds (50 charts) |
| Pattern Accuracy | 93.9% average |
| Deployment | CPU-only, no GPU needed |

**Efficiency Comparison**: AURA's vision model is 10,000x smaller than GPT-4V while maintaining comparable accuracy for data visualization tasks.

---

## Model Information

**VisionTextBridge Architecture**:
- Input: 2560-D visual embeddings from EfficientNetB7
- Hidden layers: 1024 → 512 → 256 neurons
- Output: 4 independent classification heads
- Training: 100,000 scientific plots from PlotQA dataset
- File size: 4.8MB (.h5 format)

**Automatic Download**: On first run, AURA downloads the pre-trained model (~150MB) to `~/.aura/models/`. No manual setup required.

---

## Advanced Features

**Multi-Task Classification**  
Four specialized classification heads analyze different aspects simultaneously:
- Trend detection (3 classes)
- Density analysis (3 classes)  
- Outlier detection (2 classes)
- Distribution shape (4 classes)

**Statistical Grounding**  
Pattern classifications are validated against classical statistical methods (Pearson correlation, IQR thresholds, skewness/kurtosis metrics).

**Extensible Architecture**  
Plug in custom LLMs, add new visualization types, or fine-tune the vision model on domain-specific data.

---

## Troubleshooting

**Model Download Issues**:
```python
# Manually trigger model download
from aura import Aura
app = Aura()
app.download_model()  # Forces fresh download
```

**Memory Constraints**:
```python
# Process fewer visualizations
app.generate_insights(max_plots=25)
```

**API Configuration**:
```python
# Verify environment variables
import os
print(os.getenv("AURA_API_KEY"))
print(os.getenv("AURA_MODEL"))
```

---

## Roadmap

- Enhanced visualization types (3D plots, time series decomposition)
- Fine-tuning support for domain-specific datasets
- Web-based dashboard interface
- Multi-dataset comparison mode
- Export capabilities (PDF reports, presentations)

---

## Contributing

Contributions welcome! Areas of interest:
- New visualization templates
- Performance optimizations
- Documentation improvements
- Dataset-specific adaptations

Submit issues and pull requests on [GitHub](https://github.com/hanish9193/AURA).

---

## License

MIT License - Free for personal and commercial use.

---

## Citation

```bibtex
@software{aura2024,
  title={AURA: Artificial Understanding and Reasoning Assistant},
  author={Kumar, S. Hanish and Rajalakshmi, S.},
  year={2024},
  url={https://github.com/hanish9193/AURA}
}
```

---

## Links

- **GitHub Repository**: [github.com/hanish9193/AURA](https://github.com/hanish9193/AURA)
- **PyPI Package**: [pypi.org/project/aura-viz](https://pypi.org/project/aura-viz)
- **Documentation**: [Coming Soon]
- **Issues & Support**: [GitHub Issues](https://github.com/hanish9193/AURA/issues)

---

**Built for analysts, researchers, and data scientists who want AI that truly understands their data.**