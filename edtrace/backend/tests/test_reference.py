import unittest
from edtrace import url_reference


class TestReferenceLabel(unittest.TestCase):
    def test_glm_team_label(self):
        ref = url_reference("https://arxiv.org/abs/2508.06471")
        self.assertIn("GLM-4.5 Team", ref.label)

    def test_kimi_team_label(self):
        ref = url_reference("https://arxiv.org/abs/2602.02276")
        self.assertIn("Kimi Team", ref.label)


if __name__ == "__main__":
    unittest.main()
