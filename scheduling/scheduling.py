from django.utils import timezone

from cards.models import Card, CardSet, AssignedCard
from models import RegressionWeights, RepIntervalLog, get_interval

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
        if new_grade <= 1:
            # User just "lapsed", transition from retention -> acquisition phase
            assigned_card.lapses += 1
            assigned_card.ret_reps_since_lapse = 0
        else:
            # User is staying in retention phase
            assigned_card.ret_reps_since_lapse += 1
            # If grade was [2, 3, 4, 5], increment retention phase reps count.
            assigned_card.ret_reps += 1

    ontime = (assigned_card.scheduled_rep <= new_rep_time)
    assigned_card.easiness = easiness_update(assigned_card.easiness, new_grade, ontime)
    assigned_card.last_shown = new_rep_time
    assigned_card.last_grade = new_grade
    assigned_card.scheduled_rep = schedule_rep(assigned_card)

    assigned_card.save()

def easiness_update(easiness, grade, ontime):
    # Don't update easiness when learning ahead. Easiness calculation consistent
    # with how Mnemosyne does the calculation (so the regression weights will be accurate)
    if ontime:
        if grade == 2:
            easiness -= 0.16
        if grade == 3:
            easiness -= 0.14
        if grade == 5:
            easiness += 0.10
        if easiness < 1.3:
            easiness = 1.3
    return easiness
    # return easiness - 0.8 + 0.28 * grade - 0.02 * (grade * grade)


from sklearn import svm
import numpy as np
import sys

def schedule_rep(assigned_card, target_grade=4):
    "Schedule the next repetition for the assigned card."

    # weights = RegressionWeights.objects.get(user=assigned_card.user)
    # new_interval = weights.intercept + \
    #         weights.grade * assigned_card.last_grade + \
    #         weights.easiness * assigned_card.easiness + \
    #         weights.ret_reps * assigned_card.ret_reps + \
    #         weights.ret_reps_since_lapse * assigned_card.ret_reps_since_lapse + \
    #         weights.lapses * assigned_card.lapses + \
    #         weights.new_grade * target_grade
    # new_interval = timedelta(days=1).total_seconds()

    svm_model = get_svm_model(assigned_card.user)
    features = np.array([assigned_card.last_grade, target_grade, assigned_card.easiness,
        assigned_card.ret_reps, assigned_card.ret_reps_since_lapse, assigned_card.lapses])
    new_interval_bucket = svm_model.predict(features)[0]
    new_interval = get_interval(new_interval_bucket)

    print >>sys.stderr, new_interval_bucket, new_interval

    return assigned_card.last_shown + timedelta(seconds=new_interval)

_user_to_svm = {}
def get_svm_model(user, window_size=150):
    if user in _user_to_svm:
        # TODO check whether it's time to retrain the model
        return _user_to_svm[user]

    # FIXME the logs may not actually be in chronological order...

    logs = RepIntervalLog.objects.filter(user=user)
    start_i = max(0, len(logs) - window_size)
    logs = logs[start_i:]

    x_train = np.array([(log.grade, log.new_grade, log.easiness,
        log.ret_reps, log.ret_reps_since_lapse, log.lapses) for log in logs])
    y_train = np.array([log.interval_bucket for log in logs])

    svm_model = svm.SVC()
    svm_model.fit(x_train, y_train)

    # begin debug code
    print >>sys.stderr, "Training score: %s" % svm_model.score(x_train, y_train)
    # print >>sys.stderr, svm_model.predict(x_train)
    # end debug code

    _user_to_svm[user] = svm_model

    return svm_model

