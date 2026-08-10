from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PortfolioContractTests(unittest.TestCase):
    def test_omnisell_uses_current_repository_and_architecture(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        case_study = (ROOT / "omnisell-case-study.html").read_text(encoding="utf-8")

        expected = (
            "https://github.com/paulrose4/omnisell-ai-agent",
            "Amazon 运营控制塔",
            "受控 Advisor",
            "read-only pilot",
            "770+",
        )
        for claim in expected:
            self.assertIn(claim, index + case_study)

        stale_claims = (
            "https://github.com/paulrose4/omnisell\"",
            "88/88",
            "Production Ready",
            "AutoGen 多 Agent 协作平台",
            "3 Agent 协作团队",
        )
        for claim in stale_claims:
            self.assertNotIn(claim, index + case_study)

    def test_omnisell_case_study_has_real_evidence_sections(self) -> None:
        case_study = (ROOT / "omnisell-case-study.html").read_text(encoding="utf-8")

        for section in (
            "黄金缺货闭环",
            "确定性代码负责什么",
            "批准 A、执行 B",
            "Schema Repair",
            "验证证据",
            "已知边界",
        ):
            self.assertIn(section, case_study)


if __name__ == "__main__":
    unittest.main()
