import re

path = r'C:\Users\huawe\.gemini\antigravity\brain\3291834c-519f-43f0-8ec4-12369961d580\thesis.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix 1: Database Schema Paragraph
bad_db = "The schema design ensures that ## 4.4 UML Diagrams"
good_db = "The schema design ensures that temporal data (prices) and unstructured data (reviews) are strictly linked to their parent product, allowing complex `JOIN` queries to aggregate data for the AI models rapidly.\n\n## 4.4 UML Diagrams"
text = text.replace(bad_db, good_db)

# Fix 2: UML Bullet Points
bad_uml = """- **Use Case Diagram:** Illustrates the primary actor (Consumer) interacting with the system to "View Dashboard," "Analyze Campaign," and "Analyze Sentiment." The system internally triggers "Run NLP Model" and "Execute Deep Learning Inference" via `<<include>>` relationships.ow$ Check for Fake Discount using Tabular-as-Text BERT $\\rightarrow$ Apply -30 Penalty if True $\\rightarrow$ Compute `100 - (Lowest/Average)*50` $\\rightarrow$ Return JSON Response."""

good_uml = """- **Use Case Diagram:** Illustrates the primary actor (Consumer) interacting with the system to "View Dashboard," "Analyze Campaign," and "Analyze Sentiment." The system internally triggers "Run NLP Model" and "Execute Deep Learning Inference" via `<<include>>` relationships.
- **System Architecture Diagram:** Displays the bidirectional flow of JSON data between the Web Browser (Client) and the FastAPI server, followed by the unidirectional execution paths from the server to the SQLite Database, and HuggingFace Transformers pipeline for both Sentiment and Tabular-as-Text BERT.
- **Activity Diagram (Deal Scoring):** Maps the logical flow: Start $\\rightarrow$ Query 1-year price history $\\rightarrow$ Calculate Moving Average $\\rightarrow$ Check for Fake Discount using Tabular-as-Text BERT $\\rightarrow$ Apply -30 Penalty if True $\\rightarrow$ Compute `100 - (Lowest/Average)*50` $\\rightarrow$ Return JSON Response."""
text = text.replace(bad_uml, good_uml)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Corruption fixed!")
