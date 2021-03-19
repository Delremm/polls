from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from polls.models import Poll, Question, Answer


class PollSerializer(serializers.ModelSerializer):
    question_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Poll
        fields = ['name', 'description', 'date_start', 'date_end', 'question_set']

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'poll']

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer', 'user']

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    model = Answer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserPollsSerializer(serializers.ModelSerializer):
    answer_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'answer_set']

class UserPollsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPollsSerializer

