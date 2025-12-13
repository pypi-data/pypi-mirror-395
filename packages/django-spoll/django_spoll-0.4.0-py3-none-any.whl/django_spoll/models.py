import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone

# hierarchy / structure it's django -> db -> models -> Model
# The different model field types (DateTimeField, CharField) correspond to the appropriate HTML input widget.
# Each type of field knows how to display itself in the Django admin.
DATE_PUBLISHED = "Date Published"

class QuestionType(models.Model):

    name = models.CharField(max_length=50, unique=True, default="player")
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return self.name

class Question(models.Model):
    # Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.
    #Has id & q attributes
    text = models.CharField("Question", max_length=200)
    type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING, default=1)
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.text

    @admin.display(boolean=True, ordering="pub_date", description="Published recently?")
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now

class TeamType(models.Model):

    name = models.CharField(max_length=50, unique=True, default="league")
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return self.name

class Country(models.Model):

    name = models.CharField(max_length=200, unique=True, default="Mexico")
    abbreviation = models.CharField(max_length=200, default="MX")
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.name

class Player(models.Model):

    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    age = models.IntegerField(default=0)
    nickname = models.CharField(max_length=100)
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.name

class Coach(models.Model):

    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    age = models.IntegerField(default=0)
    nickname = models.CharField(max_length=100)
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.name

class Team(models.Model):

    name = models.CharField(max_length=200)
    type = models.ForeignKey(TeamType, on_delete=models.DO_NOTHING, default=1)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    nickname = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    uniform_color_local = models.CharField(max_length=100, default="#FFFFFF")
    uniform_color_visitant = models.CharField(max_length=100, default="#000000")
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.name

class PlayerChoice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Player, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.choice.name

class TeamChoice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Team, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.choice.name

class CoachChoice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Coach, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(DATE_PUBLISHED, default=timezone.now)

    def __str__(self):
        return str(self.id) + ":" + self.choice.name