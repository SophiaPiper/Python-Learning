from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		## return false for questions who's pub_date is in the future
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		## return false for questions whose pub_date is older than 1 day
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		## return true for questions whose pub_date is within the last day
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	## create question with the given question_text and published the given number of days offset to now 
	## (negative for questions that have yet to be published).
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	def test_no_questions(self)
	## if no questions exist, display message
	response = self.client.get(reverse('polls:index'))
	self.assertEqual(response.status_code, 200)
	self.assertContains(response, "No polls are available.")
	self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		## Q's with a pub_date in the past are displayed on index page
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
			)

	def test_future_question(self):
		## Q's with pub_date in the future aren't displayed on index page
		create_question(question_text="Future question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_future_question_and_past_question(self):
		## even if both past and future questions exist, only past q's are displayed
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
			)

	def test_two_past_questions(self):
		## index page may display multiple q's
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question 2.>', '<Question: Past question 1.>']
			)

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		## detail view of a Q with a pub_date in the future returns 404
		future_question = create_question(question_text='Future Question.', days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		## detail view of Q with pub_date in the past displays Q text
		past_question = create_question(question_text='Past Question', days=-5)
		url = reverse('polls:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)
		