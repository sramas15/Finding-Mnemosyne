from django.utils import timezone

from cards.models import Card, CardSet, AssignedCard
from models import RegressionWeights, RepIntervalLog

from datetime import timedelta

def log_rep(assigned_card, new_grade, now):
    "Log a repetition. Make sure to call this before updating the assigned card."

    # Cannot log until second repetition
    if assigned_card.last_shown is None:
        return

    log = RepIntervalLog(
            user=assigned_card.user,
            card=assigned_card.card,
            grade=assigned_card.last_grade,
            new_grade=new_grade,
            easiness=assigned_card.easiness,
            ret_reps=assigned_card.ret_reps,
            ret_reps_since_lapse=assigned_card.ret_reps_since_lapse,
            lapses=assigned_card.lapses,
            interval=(now - assigned_card.last_shown).total_seconds())

def add_unseen_cards(user, limit=20):
    "Schedule (at most 'limit') unseen cards to be studied now"
    new_assignments = AssignedCard.objects.filter(user=user, last_shown=None)[:limit]
    for assignment in new_assignments:
        assignment.scheduled_rep = timezone.now()
        assignment.save()

    return (assignment.card for assignment in new_assignments)

def get_scheduled_cards(user):
    "Get the cards that are due"
    return Card.objects.filter(assignedcard__user=user, assignedcard__scheduled_rep__lte=timezone.now())

def update_card(assigned_card, new_grade, new_rep_time):
    "Update card"
    if assigned_card.last_grade > 1:
        # If grade was [2, 3, 4, 5], increment retention phase reps count.
        assigned_card.ret_reps += 1

        if new_grade <= 1:
            # User just "lapsed", transition from retention -> acquisition phase
            assigned_card.lapses += 1
            assigned_card.ret_reps_since_lapse = 0
        else:
            # User is staying in retention phase
            assigned_card.ret_reps_since_lapse += 1

    assigned_card.easiness = easiness_update(assigned_card.easiness, new_grade)
    assigned_card.last_shown = new_rep_time
    assigned_card.last_grade = new_grade
    assigned_card.scheduled_rep = schedule_rep(assigned_card)

    assigned_card.save()

def schedule_rep(assigned_card, target_grade=4):
    "Schedule the next repetition for the assigned card."

    """
    weights = RegressionWeights.objects.get(user=assigned_card.user)

    new_interval = weights.intercept + \
            weights.grade * assigned_card.last_grade + \
            weights.easiness * assigned_card.easiness + \
            weights.ret_reps * assigned_card.ret_reps + \
            weights.ret_reps_since_lapse * assigned_card.ret_reps_since_lapse + \
            weights.lapses * assigned_card.lapses + \
            weights.new_grade * target_grade
            """
    new_interval = timedelta(days=1).total_seconds()

    return assigned_card.last_shown + timedelta(seconds=new_interval)

def easiness_update(easiness, grade):
    return easiness - 0.8 + 0.28 * grade - 0.02 * (grade * grade)

