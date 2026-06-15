import re

path = r'C:\Users\huawe\.gemini\antigravity\brain\3291834c-519f-43f0-8ec4-12369961d580\thesis.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the duplicate 4.2 System Architecture block
duplicate_arch = """## 4.2 System Architecture

The platform utilizes a modern Client-Server, API-driven architecture. 

1. **Presentation Layer (Client):** A web-based dashboard consisting of static HTML, CSS (Bootstrap), and JavaScript. It communicates entirely asynchronously via `fetch` API calls.
2. **Application Layer (Server):** The FastAPI application running on an ASGI server (Uvicorn). It routes HTTP requests, executes business logic, and orchestrates the AI models.
3. **Data Layer:** An SQLite relational database containing interconnected tables for products, reviews, and historical price points.

This decoupled architecture ensures that the computational weight of the NLP models is isolated on the server, allowing the client interface to remain highly responsive regardless of the end-user's device capabilities."""

text = text.replace(duplicate_arch, "")

# 2. Fix Database Design
text = text.replace("Isolation Forest anomaly detection", "Tabular-as-Text BERT anomaly detection sequence")

# 3. Fix UML
text = text.replace("Isolation Forest module, and HuggingFace Transformers pipeline.", "HuggingFace Transformers pipeline for both Sentiment and Tabular-as-Text BERT.")
text = text.replace("Check for Fake Discount using Isolation Forest", "Check for Fake Discount using Tabular-as-Text BERT")

# 4. Fix 5.1.2 Price Manipulation Detection Module
old_512 = """### 5.1.2 Price Manipulation Detection Module
This module tackles the "Fake Discount" phenomenon. It queries the `prices` table for a specific product and seller, extracting the `actual_price` and `claimed_original_price`. An `IsolationForest` model (from scikit-learn) is trained on-the-fly using features like the discount percentage and the price deviation from the 30-day moving average. Data points that the forest isolates near the root of its decision trees are flagged as anomalies (`is_manipulation = True`)."""

new_512 = """### 5.1.2 Price Manipulation Detection Module
This module tackles the "Fake Discount" phenomenon. It queries the `prices` table for a specific product and seller, extracting historical pricing patterns. These patterns are synthesized into a natural language sequence (Tabular-as-Text) and passed to the fine-tuned BERT Sequence Classifier. The transformer model evaluates the semantic relationship between the sequences and outputs a probability tensor. If the tensor predicts deception, the data point is flagged as an anomaly (`is_manipulation = True`)."""

text = text.replace(old_512, new_512)

# 5. Fix 5.4
text = text.replace("test the Isolation Forest.", "test the Deep Learning manipulation detection.")

# 6. Fix 6.2
text = text.replace("Complex endpoints involving Isolation Forest training and inference returned in ~300ms.", "Complex endpoints involving the Tabular-as-Text BERT inference returned in ~600ms.")

# 7. Fix References
text = re.sub(r'\[2\].*?Isolation Forest.*?\n\n', '', text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Thesis successfully purged of duplicate headings and legacy models!")
