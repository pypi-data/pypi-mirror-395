import logging

from sayou.refinery.pipeline import RefineryPipeline

logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_demo():
    print(">>> Initializing Sayou Refinery...")
    
    # 설정 주입: PII 마스킹 켜기, 결측치 규칙, 이상치 규칙 설정
    pipeline = RefineryPipeline()
    pipeline.initialize(
        mask_email=True,
        imputation_rules={"category": "Unknown"},
        outlier_rules={"price": {"min": 0, "max": 1000, "action": "clamp"}}
    )

    # ---------------------------------------------------------
    # Scenario 1: Document JSON -> Markdown (with PII Masking)
    # ---------------------------------------------------------
    print("\n=== [1] Document Normalization (Markdown + PII) ===")
    
    # sayou-document가 생성했다고 가정한 더미 데이터
    raw_doc = {
        "metadata": {"title": "User Report", "author": "admin@sayou.ai"},
        "pages": [
            {
                "elements": [
                    {
                        "type": "text", 
                        "text": "Contact support at help@sayou.ai or 010-1234-5678.",
                        "raw_attributes": {"semantic_type": "heading", "heading_level": 1}
                    },
                    {
                        "type": "text",
                        "text": "   Duplicate Paragraph.   ",
                        "raw_attributes": {}
                    },
                    {
                        "type": "text",
                        "text": "Duplicate Paragraph.", 
                        "raw_attributes": {}
                    }
                ]
            }
        ]
    }

    blocks = pipeline.run(raw_doc, source_type="standard_doc")
    
    for b in blocks:
        print(f"[{b.type}] {b.content}")

    # ---------------------------------------------------------
    # Scenario 2: Dirty HTML -> Clean Text
    # ---------------------------------------------------------
    print("\n=== [2] HTML Normalization (Tag Removal) ===")
    
    dirty_html = """
    <html>
        <style>body { color: red; }</style>
        <body>
            <h1>  Welcome  to   Sayou  </h1>
            <script>alert('hack');</script>
            <p>Clean    text content.</p>
        </body>
    </html>
    """
    
    blocks = pipeline.run(dirty_html, source_type="html")
    for b in blocks:
        print(f"[{b.type}] {repr(b.content)}")

    # ---------------------------------------------------------
    # Scenario 3: DB Records (Imputation & Outlier)
    # ---------------------------------------------------------
    print("\n=== [3] Record Normalization (Data Cleaning) ===")
    
    db_rows = [
        {"id": 1, "item": "Apple", "price": 500, "category": "Fruit"},
        {"id": 2, "item": "Banana", "price": 1500, "category": None}, # 결측치 (-> Unknown)
        {"id": 3, "item": "Diamond", "price": 99999, "category": "Gem"} # 이상치 (-> 1000 Clamp)
    ]
    
    blocks = pipeline.run(db_rows, source_type="json")
    
    for b in blocks:
        print(f"[{b.type}] {b.content}")

if __name__ == "__main__":
    run_demo()