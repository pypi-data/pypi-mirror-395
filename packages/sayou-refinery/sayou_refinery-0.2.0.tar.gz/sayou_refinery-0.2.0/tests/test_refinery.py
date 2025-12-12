import unittest

from sayou.refinery.pipeline import RefineryPipeline


class TestRefineryPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = RefineryPipeline()

        self.pipeline.initialize(
            mask_email=True,
            imputation_rules={"tag": "general"},
            outlier_rules={"score": {"max": 100, "action": "drop"}},
        )

    def test_doc_markdown_normalization(self):
        """[Normalizer] 문서 딕셔너리가 Markdown 블록으로 잘 변환되고 마스킹되는지 확인"""
        raw_doc = {
            "pages": [
                {
                    "elements": [
                        {
                            "type": "text",
                            "text": "Contact: test@test.com",
                            "raw_attributes": {"semantic_type": "heading"},
                        }
                    ]
                }
            ]
        }

        blocks = self.pipeline.run(raw_doc, source_type="standard_doc")

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].type, "md")
        self.assertEqual(blocks[0].content, "# Contact: [EMAIL]")

    def test_deduplication(self):
        """[Processor] 중복된 텍스트 블록이 제거되는지 확인"""
        raw_doc = {
            "pages": [
                {
                    "elements": [
                        {"type": "text", "text": "Unique Line Content"},
                        {"type": "text", "text": "Duplicate Line Content"},
                        {"type": "text", "text": "Duplicate Line Content"},
                    ]
                }
            ]
        }
        blocks = self.pipeline.run(raw_doc, source_type="standard_doc")

        # 3개 입력 -> 2개 출력 (중복 제거)
        self.assertEqual(len(blocks), 2)

        content_list = [b.content for b in blocks]
        self.assertIn("Unique Line Content", content_list)
        self.assertEqual(content_list.count("Duplicate Line Content"), 1)

    def test_record_processing(self):
        """[Processor] 레코드의 결측치 채우기와 이상치 제거 확인"""
        raw_records = [
            {"id": 1, "tag": None, "score": 50},  # Imputation 대상
            {"id": 2, "tag": "A", "score": 200},  # Outlier (Drop) 대상 (max: 100)
            {"id": 3, "tag": "B", "score": 90},  # 정상
        ]

        blocks = self.pipeline.run(raw_records, source_type="json")

        # 3개 입력 -> 2개 출력
        self.assertEqual(len(blocks), 2)

        block1 = blocks[0].content
        self.assertEqual(block1["tag"], "general")

        ids = [b.content["id"] for b in blocks]
        self.assertNotIn(2, ids)
        self.assertIn(3, ids)


if __name__ == "__main__":
    unittest.main()
