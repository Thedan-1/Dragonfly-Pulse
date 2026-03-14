from competition_intel.llm.information_extractor import extract_information


def test_extract_information_rule_fallback() -> None:
    text = """
    第十七届全国大学生信息安全竞赛通知
    主办单位：教育部高等学校网络空间安全专业教学指导委员会
    报名时间：2026年03月01日-2026年04月20日
    比赛时间：2026年05月15日
    """
    payload = extract_information(
        text=text,
        announcement_title="第十七届全国大学生信息安全竞赛通知",
        source_url="https://example.com/notice/1",
        competition_name="全国大学生信息安全竞赛",
    )

    assert payload["competition_name"] == "全国大学生信息安全竞赛"
    assert payload["announcement_title"] == "第十七届全国大学生信息安全竞赛通知"
    assert payload["organizer"] is not None
    assert payload["registration_deadline"] is not None
    assert payload["competition_date"] is not None
