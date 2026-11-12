def test_homepage_has_members_link(page, base_url):
    page.goto(base_url)
    page.screenshot(path="homepage.png")
    print("URL:", page.url)
    print("TITLE:", page.title())

    print(page.content())

    members_link = page.get_by_role("link", name="members")

    assert members_link.is_visible()