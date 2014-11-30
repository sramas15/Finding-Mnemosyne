from cards.models import Card, CardSet, AssignedCard
from models import RegressionWeights

from datetime import datetime
import bisect

INTERVAL_BUCKETS = [
        60*60,
        60*60*4,
        60*60*12,
        60*60*24,
        60*60*24*2,
        60*60*24*4,
        60*60*24*8,
        60*60*24*16,
        60*60*24*64
    ]

def get_interval(interval):
    return bisect.bisect_right(INTERVAL_BUCKETS, interval)

def log_rep(user, card, assigned_card, new_grade):
    "Log a repetition. Make sure to call this before updating the assigned card."
    log = RepIntervalLog(
            user=user,
            card=card,
            grade=assigned_card.grade,
            new_grade=new_grade,
            easiness=assigned_card.easiness,
            ret_reps=assigned_card.ret_reps,
            ret_reps_since_lapse=assigned_card.ret_reps_since_lapse,
            lapses=assigned_card.lapses,
            interval=(datetime.now() - assigned_card.last_shown).total_seconds())

def add_unseen_cards(user, limit=20):
    "Schedule (at most 'limit') unseen cards to be studied now"
    new_assignments = AssignedCard.objects.filter(user=user, last_shown=None)[:limit]
    for assignment in new_assignments:
        assignment.scheduled_rep = datetime.now()
        assignment.save()

    return (assignment.card for assignment in new_assignments)

def get_scheduled_cards(user):
    "Get the cards that are due"
    return Card.objects.filter(assignedcard__user=user, assignedcard__scheduled_rep__lte=datetime.now())

def update_card(assigned_card, new_grade, new_rep_time):
    "Update card"
    assigned_card.easiness = easiness_update(assigned_card.easiness, new_grade)
    if assigned_card.grade <= 1:
        # If previous grade was [0, 1], increment acquisition phrase reps count.
        assigned_card.acq_reps += 1
    else:
        # Otherwise if grade was [2, 3, 4, 5], increment retention phase reps count.
        assigned_card.ret_reps += 1

        if new_grade <= 1:
            # User just "lapsed", retention -> acquisition phase
            assigned_card.lapses += 1
            assigned_card.ret_reps_since_lapse = 0
        else:
            # User is staying in retention phase
            assigned_card.ret_reps_since_lapse += 1
    assigned_card.last_shown = new_rep_time
    assigned_card.last_grade = new_grade
    assigned_card.scheduled_rep = schedule_rep(assigned_card)

def schedule_rep(assigned_card, target_grade=4):
    "Schedule the next repetition for the assigned card."
    weights = RegressionWeights.objects.get(user=assigned_card.user)

    return weights.intercept + \
            weights.grade * assigned_card.last_grade + \
            weights.easiness * assigned_card.easiness + \
            weights.ret_reps * assigned_card.ret_reps + \
            weights.ret_reps_since_lapse * assigned_card.ret_reps_since_lapse + \
            weights.lapses * assigned_card.lapses + \
            weights.new_grade * target_grade

def easiness_update(easiness, grade):
    return easiness - 0.8 + 0.28 * grade - 0.02 * (grade * grade)

