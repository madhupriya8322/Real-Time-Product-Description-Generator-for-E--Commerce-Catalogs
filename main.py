pip install requests gradio pandas matplotlib seaborn



# Import necessary libraries
import requests  # For making HTTP requests to the Groq API
import gradio as gr  # For creating the web-based user interface
import pandas as pd  # For data manipulation (not used in this code but imported)
import matplotlib.pyplot as plt  # For creating visualizations
import seaborn as sns  # For enhancing matplotlib visualizations
from datetime import datetime  # For handling date and time

# Define a class to generate product descriptions
class ProductDescriptionGenerator:
    def __init__(self):
        self.groq_api_key = "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"
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.generated_descriptions = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Method to generate a product description
    def generate_product_description(self, product_name, category, features):
        if not all([product_name.strip(), category.strip(), features.strip()]):
            return "Error: All fields must be filled.", None

        prompt = f"Generate a compelling e-commerce product description (100-150 words) for:\n\nProduct Name: {product_name}\nCategory: {category}\nKey Features: {features}\n\nDescription:"

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are an AI assistant helping to create product descriptions."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                self.groq_api_url,
                headers={"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"},
                json=data
            )
            response.raise_for_status()
            description = response.json()["choices"][0]["message"]["content"].strip()
            self.generated_descriptions.append({
                "product": product_name,
                "text": description,
                "word_count": len(description.split())
            })
            viz_path = self.analyze_description_length()
            return description, viz_path
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to generate description - {str(e)}", None

    def batch_generate_descriptions(self, product_list):
        if not product_list.strip():
            return "Error: Please enter at least one product.", None

        results = []
        products = product_list.split('\n')

        # Clear previous descriptions for batch processing
        self.generated_descriptions = []

        for product in products:
            if '|' in product:
                try:
                    name, category, features = [x.strip() for x in product.split('|')]
                    if all([name, category, features]):
                        description, _ = self.generate_product_description(name, category, features)
                        results.append(f"Product: {name}\n{description}\n{'-'*50}")
                    else:
                        results.append(f"Error processing '{product}': All fields required")
                except ValueError:
                    results.append(f"Error processing '{product}': Invalid format")
            else:
                results.append(f"Error processing '{product}': Please use '|' separator")

        viz_path = self.analyze_description_length()
        return "\n".join(results), viz_path

    def analyze_description_length(self):
        if not self.generated_descriptions:
            return None

        lengths = [desc["word_count"] for desc in self.generated_descriptions]

        plt.figure(figsize=(10, 6))
        sns.histplot(lengths, bins=10, color='skyblue')
        plt.title('Distribution of Description Word Counts')
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')
        plt.axvline(x=100, color='green', linestyle='--', label='Min Target (100)')
        plt.axvline(x=150, color='red', linestyle='--', label='Max Target (150)')
        plt.legend()

        # Add text showing actual stats
        avg_length = sum(lengths) / len(lengths)
        plt.text(0.95, 0.95, f'Avg Words: {avg_length:.1f}\nCount: {len(lengths)}',
                transform=plt.gca().transAxes, ha='right', va='top')

        output_path = f'description_length_{self.timestamp}.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

# Create instance
generator = ProductDescriptionGenerator()

# Create Gradio UI with tabs
with gr.Blocks(title="E-Commerce Product Description Generator") as demo:
    gr.Markdown("# E-Commerce Product Description Generator")
    gr.Markdown("Generate high-quality product descriptions using Groq's API")

    with gr.Tab("Single Product"):
        with gr.Row():
            with gr.Column():
                single_name = gr.Textbox(label="Product Name", placeholder="e.g., Wireless Earbuds")
                single_category = gr.Textbox(label="Category", placeholder="e.g., Electronics")
                single_features = gr.Textbox(
                    label="Key Features (comma-separated)",
                    placeholder="e.g., noise-cancelling, 20-hour battery, waterproof"
                )
                single_button = gr.Button("Generate Description")

            with gr.Column():
                single_output = gr.Textbox(label="Generated Description", lines=10)
                single_viz = gr.Image(label="Description Length Analysis")

    with gr.Tab("Batch Processing"):
        with gr.Row():
            with gr.Column():
                batch_input = gr.Textbox(
                    label="Product List (one per line: Name | Category | Features)",
                    placeholder="Wireless Earbuds | Electronics | noise-cancelling, 20-hour battery\nSmart Watch | Wearables | heart rate monitor, waterproof",
                    lines=5
                )
                batch_button = gr.Button("Generate Batch Descriptions")

            with gr.Column():
                batch_output = gr.Textbox(label="Batch Results", lines=10)
                batch_viz = gr.Image(label="Description Length Analysis")

    # Event handlers
    single_button.click(
        fn=generator.generate_product_description,
        inputs=[single_name, single_category, single_features],
        outputs=[single_output, single_viz]
    )

    batch_button.click(
        fn=generator.batch_generate_descriptions,
        inputs=batch_input,
        outputs=[batch_output, batch_viz]
    )

# Launch the interface
demo.launch(share=True, debug=True)