from rest_framework import serializers
from . import models


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'course_name', 'fee', 'contents', 'duration')
        lookup_field = 'course_name'
        model = models.Courses
