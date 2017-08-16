from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Course, Step


class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="test2 Learn to write regular expressions in Python"
        )
        now = timezone.now()
        self.assertLess(course.create_at, now)


    def setUp(self):
        self.course = Course.objects.create(
            title="Introductioin to Doctest",
            description="test 2"
        )


    def test_step_creation(self):
        step = Step.objects.create(
            title="introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())


class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title = "test 3",
            description = "tes 3"
        )
        self.courseNew = Course.objects.create(
            title = "test 3-2",
            description = "test 3-2"
        )
        self.step = Step.objects.create(
            title = "test 3",
            description="test 3",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail',
                                       kwargs={'pk':self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])

    def test_step_detail(self):
        resp = self.client.get(reverse('courses:step',
                                       kwargs={
                                           'course_pk':self.course.pk,
                                           'step_pk':self.step.pk
                                       }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
