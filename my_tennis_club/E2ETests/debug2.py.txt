def test_debug(page, base_url):
    page.goto(base_url)

    print("Members count:",
          page.locator("a[href='members/']").count())

    print("Members visible:",
          page.locator("a[href='members/']").is_visible())

    print("Main visible:",
          page.locator("main").is_visible())

    print("H1 visible:",
          page.locator("h1").is_visible())

    page.screenshot(path="homepage.png")

    print(page.locator("body").inner_text())