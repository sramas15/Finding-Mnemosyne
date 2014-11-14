import mnemosyne_logs
import numpy as np

CURR_GRADE = 0
PREV_GRADE = 1
ACQ_REPS = 8 # NO_IMPACT (was 2)
EASINESS = 2
RET_REPS = 3
LAPSES = 4
ACQ_REPS_SINCE_LAPSE = 9 #(was 5)
ACTUAL_INTERVAL = 5
RET_REPS_SINCE_LAPSE = 6
THINKING_TIME_PREV = 7


def get_training_data(limit=1000):
    users = mnemosyne_logs.list_user_ids(limit)
    num_examples = 0
    training_x = np.ones((limit, 10), dtype=float)
    training_y = np.ones(limit, dtype=float)
    for user in users:
        logs = mnemosyne_logs.fetch_logs(user)

        for card in logs:
            num_reps = len(card)
            for i in range(1, num_reps):
                prev = card[i-1]
                curr = card[i]
                training_x[num_examples][CURR_GRADE] = curr[mnemosyne_logs.GRADE]
                training_x[num_examples][PREV_GRADE] = prev[mnemosyne_logs.GRADE]
                training_x[num_examples][EASINESS] = prev[mnemosyne_logs.EASINESS]
                training_x[num_examples][RET_REPS] = prev[mnemosyne_logs.RET_REPS]
                training_x[num_examples][LAPSES] = prev[mnemosyne_logs.LAPSES]
                training_x[num_examples][ACTUAL_INTERVAL] = prev[mnemosyne_logs.ACTUAL_INTERVAL]
                training_x[num_examples][RET_REPS_SINCE_LAPSE] = prev[mnemosyne_logs.RET_REPS_SINCE_LAPSE]
                training_x[num_examples][THINKING_TIME_PREV] = prev[mnemosyne_logs.THINKING_TIME]
                training_x[num_examples][ACQ_REPS] = prev[mnemosyne_logs.ACQ_REPS]
                training_x[num_examples][ACQ_REPS_SINCE_LAPSE] = prev[mnemosyne_logs.ACQ_REPS_SINCE_LAPSE]
                training_y[num_examples] = curr[mnemosyne_logs.TIMESTAMP] - prev[mnemosyne_logs.TIMESTAMP]
                num_examples += 1
                if num_examples == limit:
                    return (training_x, training_y)


        