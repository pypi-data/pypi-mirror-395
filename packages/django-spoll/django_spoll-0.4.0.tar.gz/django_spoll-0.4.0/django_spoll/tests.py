import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question, QuestionType
from django.urls import reverse

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns F 4 qs whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_q = Question(pub_date=time)
        self.assertIs(future_q.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns F 4 qs whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=7, seconds=1)
        old_q = Question(pub_date=time)
        self.assertIs(old_q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() returns T 4 qs whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_q = Question(pub_date=time)
        self.assertIs(recent_q.was_published_recently(), True)

def create_q(text, days, name):
    """ Create a q with the given `text` & published the
    given num of `days` offset to now ("-" for qs published
    in the past, "+" for qs that have yet to be published)."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=text, type=create_q_type(name), pub_date=time)

def create_q_type(name):
    return QuestionType.objects.create(name=name, pub_date=timezone.now())

class QuestionIndexViewTests(TestCase):

    def test_no_qs(self):
        """ If no qs exist, an appropriate msg is displayed."""
        resp = self.client.get(reverse("soccerpoll:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No Soccer polls are available ...")
        self.assertQuerySetEqual(resp.context["latest_q_list"], [])

    def test_past_q(self):
        """Qs with a pub_date in the past are shown on the index page."""
        q = create_q(text="Past question.", days=-30, name="player")
        resp = self.client.get(reverse("soccerpoll:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerySetEqual(resp.context["latest_q_list"],[q],)

    def test_future_q(self):
        """Qs with a pub_date in the future aren't show on the index page."""
        create_q(text="Future question.", days=30, name="coach")
        resp = self.client.get(reverse("soccerpoll:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No Soccer polls are available ...")
        self.assertQuerySetEqual(resp.context["latest_q_list"], [])

    def test_future_q_and_past_q(self):
        """ Even if both past & future qs exist, only past qs are shown."""
        q1 = create_q(text="Past question.", days=-30, name="player")
        q2 = create_q(text="Future question.", days=30, name="coach")
        print('Publication date - q1: ' + str(q1.pub_date))
        print('Publication date - q2: ' + str(q2.pub_date))
        resp = self.client.get(reverse("soccerpoll:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerySetEqual(resp.context["latest_q_list"],[q1],)

    def test_two_past_qs(self):
        """The qs index page may display multiple qs."""
        q1 = create_q(text="Past question 1.", days=-30, name="team")
        q2 = create_q(text="Past question 2.", days=-5, name="player")
        resp = self.client.get(reverse("soccerpoll:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerySetEqual(resp.context["latest_q_list"],[q2, q1],)
#
class QuestionDetailViewTests(TestCase):

    def test_future_q(self):
        """Detail view of a q with pub_date in the future returns 404."""
        future_q = create_q(text="Future question.", days=5, name="player")
        url = reverse("soccerpoll:detail", args=(future_q.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_past_question(self):
        """Detail view of a q with pub_date in the past shows q text."""
        past_q = create_q(text="Past Question.", days=-5, name="coach")
        url = reverse("soccerpoll:detail", args=(past_q.id,))
        resp = self.client.get(url)
        self.assertContains(resp, past_q.text)
