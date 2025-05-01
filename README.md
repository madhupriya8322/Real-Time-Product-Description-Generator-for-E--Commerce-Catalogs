# E-Commerce Product Description Generator

This project utilizes the **Groq API** to generate product descriptions for e-commerce websites. It provides both a **single product description generator** and a **batch processing tool** for generating multiple product descriptions at once. Additionally, it includes a **description length analysis** feature that visualizes the word count distribution of generated descriptions.

## Libraries Used
- **requests**: For making HTTP requests to the Groq API.
- **gradio**: For creating the web-based user interface (UI).
- **matplotlib**: For visualizing description length distribution.
- **seaborn**: For enhancing matplotlib visualizations.
- **pandas**: Data manipulation (imported but not actively used in this code).

## Features
1. **Single Product Description**: 
   - Enter product name, category, and key features to generate a compelling e-commerce product description.
   
2. **Batch Processing**:
   - Enter a list of products (in the format `Name | Category | Features`) to generate descriptions for multiple products at once.

3. **Description Length Analysis**:
   - A visual representation of the word count distribution of the generated descriptions, helping to analyze the quality and length of descriptions.

## Installation

To get started, you'll need to install the necessary dependencies:

```bash
pip install requests gradio pandas matplotlib seaborn
