import unittest
from unittest.mock import Mock, call

from ingest import replace_source_documents


class ReplaceSourceDocumentsTests(unittest.TestCase):
    def test_replaces_existing_chunks_for_source(self):
        vectorstore = Mock()
        chunks = [Mock(), Mock()]

        replace_source_documents(vectorstore, chunks, "data/genai_notes.pdf")

        self.assertEqual(
            vectorstore.mock_calls,
            [
                call.delete(where={"source": "data/genai_notes.pdf"}),
                call.add_documents(chunks),
            ],
        )

