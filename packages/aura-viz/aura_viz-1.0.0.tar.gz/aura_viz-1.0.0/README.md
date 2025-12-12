# AURA - Advanced Unified Relationship Analyzer

A lightweight Python library for data visualization, insight extraction, and interactive Q&A powered by AI.

## Features

✨ **15 Automated Graphs**
- Correlations, distributions, scatter plots, outliers, feature importance, data quality analysis, and more

🔍 **Smart Insights**
- Automatically detects correlations, missing data, flaws, and outliers
- Pre-trained deep learning model (no training required)

🤖 **Interactive Q&A**
- Ask natural language questions about your data
- Get AI-powered insights about relationships and patterns

⚡ **Simple API**
\`\`\`python
from aura import Aura

aura = Aura()
aura.load_data("data.csv")
aura.generate_insights()
answer = aura.ask("What correlations exist?")
\`\`\`

## Installation

\`\`\`bash
pip install aura-viz
\`\`\`

## Quick Start

\`\`\`python
from aura import Aura

aura = Aura()
aura.load_data("your_data.csv")
insights = aura.generate_insights()

# Ask questions
aura.ask("What are the strongest correlations?")
aura.ask("Are there any missing values?")
aura.ask("What data quality issues exist?")
\`\`\`

## Interactive Streamlit App

\`\`\`bash
pip install streamlit
streamlit run app.py
\`\`\`

Upload CSV → Get 15 graphs → Ask questions → Done!

## What Gets Generated

- **15 Visualization Graphs** (PNG files in `/outputs`)
- **Correlation Matrix**
- **Feature Importance Analysis**
- **Data Quality Report**
- **Outlier Detection**
- **Distribution Analysis**

## How It Works

1. Load CSV data
2. Generate 15 graph visualizations
3. Extract visual features using **pre-trained EfficientNetB7**
4. Analyze data statistics and metadata
5. Answer user questions using embeddings + keyword matching

**No model training required!** Uses pre-trained models only.

## Using Custom LLMs (OpenAI, etc.)
By default, AURA uses a local Ollama instance (Mistral). If you prefer to use your own API (like OpenAI, Azure, or any OpenAI-compatible endpoint), simply set the following environment variables:

```bash
# Linux/Mac
export AURA_API_KEY="sk-..."
export AURA_MODEL="gpt-4"  # Optional, defaults to gpt-3.5-turbo

# Windows (PowerShell)
$env:AURA_API_KEY="sk-..."
$env:AURA_MODEL="gpt-4"
```

AURA will automatically detect the API key and switch from Ollama to your custom provider.

## Documentation

See `DEPLOYMENT_GUIDE.md` for:
- Local testing
- Streamlit usage
- PyPI installation

## License

MIT License - See LICENSE.txt

## Support

For issues: Create a GitHub issue or contact support@aura.dev
\`\`\`

```text file="LICENSE.txt"
MIT License

Copyright (c) 2025 AURA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
