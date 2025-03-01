# main.py
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import os
from openai import OpenAI

client = OpenAI(api_key="sk-18396a4dac4b4b4a856fdc3d313a21f3",
                base_url="https://api.deepseek.com")


class DeepSeekAssistant:
    def __init__(self, root):
        self.root = root
        self.history = []

        # Configure window
        root.title("DeepSeek Assistant")
        root.geometry("700x500")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Input Section
        self.query_label = tk.Label(self.root, text="Ask DeepSeek:")
        self.query_entry = tk.Entry(self.root, width=70)
        self.ask_button = tk.Button(
            self.root, text="Search", command=self.ask_question)

        # Response Display
        self.response_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=20
        )

        # Report Generation
        self.report_button = tk.Button(
            self.root,
            text="Generate HTML Report",
            command=self.generate_html_report
        )

        # Layout using grid
        self.query_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.query_entry.grid(row=1, column=0, padx=10, pady=5)
        self.ask_button.grid(row=1, column=1, padx=5, pady=5)
        self.response_area.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10)
        self.report_button.grid(row=3, column=0, columnspan=2, pady=5)

    def ask_question(self):
        question = self.query_entry.get().strip()
        if not question:
            messagebox.showwarning("Empty Input", "Please enter a question")
            return

        try:
            # Use the existing client instance instead of making direct requests
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": question}],
                temperature=0.7,
                max_tokens=1000
            )

            # Correct response parsing (using message.content instead of text)
            answer = response.choices[0].message.content.strip()
            self.show_response(question, answer)
            self.query_entry.delete(0, tk.END)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Request failed: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_response(self, question, answer):
        # Display in text area
        formatted_response = f"Q: {question}\\nA: {answer}\\n{'='*50}\\n\\n"
        self.response_area.insert(tk.END, formatted_response)

        # Store in history
        self.history.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "answer": answer
        })

        # Auto-scroll to bottom
        self.response_area.see(tk.END)

    # Add to DeepSeekAssistant class

# main.py

    def generate_html_report(self):
        if not self.history:
            messagebox.showinfo("Empty Report", "No queries to report")
            return

        try:
            # Create reports directory if not exists
            if not os.path.exists("reports"):
                os.makedirs("reports")

            # Generate filename with timestamp
            filename = f"reports/report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

            # Build HTML content
            html_content = f"""<html>
            <head>
                <title>DeepSeek Report</title>
                <style>
                    body {{ 
                        font-family: 'Segoe UI', Arial, sans-serif; 
                        margin: 0;
                        line-height: 1.6;
                    }}
                    .container {{ max-width: 800px; margin: 20px auto; padding: 0 20px; }}
                    .header {{ 
                        background: #1a237e;
                        color: white;
                        padding: 2rem;
                        margin-bottom: 2rem;
                    }}
                    h1 {{ 
                        margin: 0;
                        font-size: 2.5rem;
                        font-weight: 300;
                    }}
                    .subtitle {{
                        font-size: 1.1rem;
                        opacity: 0.9;
                        margin-top: 0.5rem;
                    }}
                    .qa-pair {{
                        background: #f8f9fa;
                        border-radius: 8px;
                        padding: 1.5rem;
                        margin-bottom: 1.5rem;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .question {{
                        color: #1a237e;
                        font-size: 1.2rem;
                        margin-bottom: 1rem;
                    }}
                    .answer {{
                        color: #333;
                        margin-left: 1rem;
                    }}
                    ul {{
                        padding-left: 1.5rem;
                        margin: 0.5rem 0;
                    }}
                    li {{ margin-bottom: 0.5rem; }}
                    hr {{ border: 0; border-top: 1px solid #eee; margin: 2rem 0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="container">
                        <h1>DeepSeek AI Report</h1>
                        <div class="subtitle">
                            Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        </div>
                    </div>
                </div>
                <div class="container">
                    <div class="content">"""

            for idx, item in enumerate(self.history, 1):
                # Format answer with bullet points if lines start with '-'
                answer_content = "\n".join([
                    f"<ul><li>{line[1:].strip()}</li></ul>" if line.startswith('-')
                    else f"<p>{line}</p>"
                    for line in item['answer'].split('\n')
                ])

                html_content += f"""
                    <div class="qa-pair">
                        <div class="query-meta">#{idx} • {item['timestamp']}</div>
                        <div class="question">Question: {item['question']}</div>
                        <div class="answer">{answer_content}</div>
                    </div>"""

            html_content += "</div></div></body></html>"

            # Write to file with UTF-8 encoding
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)

            messagebox.showinfo("Success", f"Report generated:\\n{filename}")

        except Exception as e:
            messagebox.showerror(
                "Report Error", f"Failed to generate report: {str(e)}")




# Add to bottom of main.py
if __name__ == "__main__":
    root = tk.Tk()
    app = DeepSeekAssistant(root)
    root.mainloop()


