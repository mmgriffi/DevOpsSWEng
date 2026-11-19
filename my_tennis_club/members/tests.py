from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Member




class MemberViewsTestCase(TestCase):

    def setUp(self):
        """Creates a temporary member in the isolated test database."""
        self.member = Member.objects.create(
            firstname="John",
            lastname="Doe"
        )

    def test_main_page_view(self):
        """Tests that the landing page loads successfully."""
        url = reverse('main')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_members_list_view(self):
        """Tests that the member list loads and displays our test member."""
        url = reverse('members')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Verifies the created member's name shows up on the page
        self.assertContains(response, "John")

    def test_member_details_view(self):
        """Tests drilling down into a specific member's detail page."""
        url = reverse('details', args=[self.member.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")
        self.assertContains(response, "Doe")

    def test_member_details_not_found(self):
        """Tests that an invalid member ID correctly triggers a 404 error."""
        # Using 9999 assuming this ID won't exist in our fresh test DB
        url = reverse('details', args=[9999])

        # Django's default behavior for Member.objects.get(id=9999) when it
        # doesn't exist is throwing a DoesNotExist exception.
        # If you change your view later to use get_object_or_404(),
        # you would assert self.assertEqual(response.status_code, 404) instead.
        with self.assertRaises(Member.DoesNotExist):
            self.client.get(url)

class FooterVersionTests(TestCase):
    @override_settings(APP_VERSION="v9.9", BUILD_DATE="19-Nov-2026")
    def test_homepage_renders_version_and_build_date(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Version: v9.9")
        self.assertContains(response, "Build: 19-Nov-2026")
