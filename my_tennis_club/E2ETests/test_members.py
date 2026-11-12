def test_members_page_loads(page, base_url):
    response = page.goto(f"{base_url}/members/")

    assert response.status == 200
    assert page.url.endswith("/members/")
def test_members_page_contains_links(page, base_url):
    page.goto(f"{base_url}/members/")

    links = page.locator("a")

    assert links.count() > 0
def test_member_details_page_loads(page, base_url):
    page.goto(f"{base_url}/members/details/1")

    assert page.url.endswith("/members/details/1")
def test_member_details_page_has_content(page, base_url):
    page.goto(f"{base_url}/members/details/1")

    body_text = page.locator("body").text_content()

    assert body_text is not None
    assert len(body_text.strip()) > 0
def debug_test_list_member_names(page, base_url):
    page.goto(f"{base_url}/members/")
    #first_link = page.locator("a").first
    #first_link.click()
    #page.wait_for_load_state()
    #assert "/details/" in page.url
    links = page.locator("a")
    for i in range(links.count()):
        text = links.nth(i).text_content()
        href = links.nth(i).get_attribute("href")

        print(f"{i}: {text} -> {href}")
def test_open_first_member_details(page, base_url):
    page.goto(f"{base_url}/members/")
    details_link = page.locator("a[href*='details']").first
    details_link.click()
    page.wait_for_load_state()
    assert "/details/" in page.url
    body_text = page.locator("body").text_content()
    assert body_text is not None
    assert len(body_text.strip()) > 0