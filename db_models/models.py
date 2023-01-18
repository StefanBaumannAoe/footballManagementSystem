from django.db import models

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    number = models.IntegerField()
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

class League(models.Model):
    name = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    players = models.ManyToManyField(Player)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    start_time = models.DateTimeField()
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

class FinancialPenalty(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class MatchPenalty(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=(('yellow', 'Yellow Card'), ('yellow-red', 'Yellow-Red Card'), ('red', 'Red Card'), ('time-suspension', 'Time Suspension')))
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    minutes = models.IntegerField()