def test_homepage_loads(page, base_url):
    page.goto(base_url)

    assert page.title() is not None
    assert page.url == base_url + "/"

    # Saves a screenshot of the visible viewport
    page.screenshot(path="homepage.png")

def test_homepage_has_members_link(page, base_url):
    page.goto(base_url)

    members_link = page.locator("a[href='members/']")
    #print(members_link)
    assert members_link.count() > 0
    assert members_link.is_visible()
    #above passed, but CoPilot suggested this was more robust.
    #members_link = page.get_by_role("link", name="members")
    #assert members_link.is_visible()
    # Saves a screenshot of the entire scrollable page
    page.screenshot(path="members_link_check.png", full_page=True)
