# ⚡ CAIF (Code AI Fast) Framework

> **Developer:** Rudra  
> **Version:** 0.0.1 (Alpha)

CAIF is a **unified, fast-track AI framework** built on Python. It is designed to significantly reduce the complexity and amount of code needed to train, deploy, and analyze **ANY** type of AI model—from image recognition and data analysis to fully interactive web chatbots.

CAIF handles all the hard parts automatically: data cleaning, intelligent Neural Network sketching, and rich text output generation (Markdown, HTML, & Python Code).

---

## 🚀 Key Features

* **⚡ Code Simplification:** Replaces hundreds of lines of complex Python with simple, one-line commands.
* **🌍 Omnivorous Data Loader:** Natively supports all major file types for training data (MP4, JPG, CSV, EXCEL, JSON, ZIP, etc.) from both local files and URLs.
* **🧠 Auto-Sketched Models:** Automatically designs and optimizes the Neural Network architecture (number of neurons and layers) based on the size and richness of your training data.
* **💬 Rich Text Output (MDP):** Models automatically respond in Markdown, which CAIF instantly converts into clean **HTML** (for websites) or runnable **Python Code** (for rich-text apps).
* **🌐 Specialized Builders:** Includes powerful shortcuts like `CAIF.WEB_CHATBOT()` for rapid, customizable web application creation.

---

## 🛠️ Installation

CAIF is published on PyPI and is easy to install using Python's package installer, `pip`.

```bash
pip install caif-framework
```

## 💡 Quick Start Example

This example shows how to train an AI to predict a value from a simple spreadsheet (CSV) and generate a rich report:
```python
from caif import CAIF

# 1. DATA: Load your data from a URL or file, and specify the column to predict.
# CAIF automatically handles cleaning, formatting, and converting data to "special numbers."
CAIF.DATA(
    source="[https://data.com/house_prices.csv](https://data.com/house_prices.csv)",
    type="csv",
    target_column="Sale_Price"
)

# 2. MODEL: Tell CAIF what kind of AI to build. Complexity (1-10) suggests the size.
# CAIF automatically designs the best Neural Network structure.
CAIF.MODEL(
    type="housing_predictor", 
    complexity=7, 
    time_limit="15m"
)

# 3. ANALYZE (Shortcut): Generates a full performance report of the model.
# The AI generates a Markdown report about its accuracy and key features.
CAIF.ANALYZE(focus="report")

# 4. OUTPUT: Save the final Markdown report as a clean HTML file.
# CAIF's MDP converts the rich text Markdown into HTML code.
CAIF.OUTPUT(target="HTML", save_as="house_price_analysis.html")
```

## 💬 Specialized Web Chatbot Example

Build and style a fully interactive, pirate-themed chatbot interface with one command:
```Python
CAIF.WEB_CHATBOT(
    personality="funny, pirate-themed",
    data_source="C:/MyFiles/pirate_dialogue.jsonl",
    interface="HTML, CSS, JS",
    look_spec="window: wood texture; font: italic gold"
)
```
