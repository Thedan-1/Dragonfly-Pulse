from competition_intel.crawler.fetcher import discover_article_links


def test_discover_article_links_filters_keywords(monkeypatch) -> None:
    html = """
    <html><body>
      <a href='/a1'>第十七届竞赛报名通知</a>
      <a href='/a2'>关于课程安排</a>
      <a href='/a3'>赛事公告：省赛时间调整</a>
    </body></html>
    """

    def _fake_fetch(url: str) -> str:
        return html

    monkeypatch.setattr("competition_intel.crawler.fetcher.fetch_html", _fake_fetch)
    seeds = discover_article_links("https://example.com/list")

    urls = [s.url for s in seeds]
    assert "https://example.com/a1" in urls
    assert "https://example.com/a3" in urls
    assert "https://example.com/a2" not in urls


def test_discover_article_links_skips_non_http_links_and_fragments(monkeypatch) -> None:
    html = """
    <html><body>
      <a href="#notice">竞赛通知锚点</a>
      <a href="mailto:team@example.com">竞赛通知邮件</a>
      <a href="javascript:void(0)">竞赛通知脚本</a>
      <a href="/notice#details">竞赛通知</a>
      <a href="/notice#schedule">竞赛通知重复锚点</a>
    </body></html>
    """

    monkeypatch.setattr(
        "competition_intel.crawler.fetcher.fetch_html", lambda url: html
    )

    seeds = discover_article_links("https://example.com/list")

    assert [seed.url for seed in seeds] == ["https://example.com/notice"]
