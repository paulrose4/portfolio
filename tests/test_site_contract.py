import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]


class LocalReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attribute = "href" if tag in {"a", "link"} else "src" if tag in {
            "img",
            "script",
        } else None
        if attribute is None:
            return
        values = dict(attrs)
        value = values.get(attribute)
        if value:
            self.references.append(value)


class PortfolioContractTests(unittest.TestCase):
    def test_local_pages_reference_existing_files(self) -> None:
        root = ROOT.resolve()

        for page in ROOT.glob("*.html"):
            parser = LocalReferenceParser()
            parser.feed(page.read_text(encoding="utf-8"))

            for reference in parser.references:
                parsed = urlsplit(reference)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (page.parent / parsed.path).resolve()
                self.assertTrue(
                    target.is_relative_to(root),
                    f"{page.name} references a path outside the site: {reference}",
                )
                self.assertTrue(
                    target.exists(),
                    f"{page.name} references a missing file: {reference}",
                )

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

    def test_supportos_has_role_timeline_and_public_provenance(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        case_study = (ROOT / "supportos-case-study.html").read_text(
            encoding="utf-8"
        )

        for claim in (
            "2026 年 7 月中旬",
            "独立承担端到端工程交付",
            "需求分析与业务建模",
            "公开提交从安全审计后的代码快照开始",
            "public-release-provenance.zh-CN.md",
        ):
            self.assertIn(claim, index + case_study)

        self.assertNotIn("纯个人项目", index + case_study)
        self.assertNotIn("知识产权全部属于我", index + case_study)


if __name__ == "__main__":
    unittest.main()
