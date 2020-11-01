import numpy as np

svod = np.load('VibKRD.npy', allow_pickle='TRUE').item()
viewer_stat = np.load('CPRF_is.npy', allow_pickle='TRUE').item()

cprf_score = {}
for item in svod:
    cprf_score[item.split("№")[1]] = svod[item].split('\n')

viewers_stat = {}
for item in viewer_stat:
    viewers_stat[item.split("№")[1]] = viewer_stat[item]

new_dict = {} # Словарь для агрегации итоговых данных
for item in cprf_score:
    if (item in cprf_score) and (item in viewers_stat):
        temp_dict = []
        temp_dict.append(cprf_score[item])
        temp_dict.append(viewers_stat[item])
        new_dict[item] = temp_dict

wo_cprf = []
for i in new_dict:
    if new_dict[i][1] == False:
        wo_cprf.append(i)
print("УИКи без наблюдателей КПРФ:")
print(", ".join(wo_cprf))
print("")

sum_cprf = 0
total_sum = 0


def count_scores(dict, cprf_viewer):
    sum_cprf = 0
    total_sum = 0
    for i in new_dict:
        if new_dict[i][1] == cprf_viewer:
            total_sum += (float(new_dict[i][0][0]) / float((new_dict[i][0][1]).replace("%", ""))) * 100
            sum_cprf += (float(new_dict[i][0][0]))
    return round((sum_cprf / total_sum) * 100, 2)


score_w_cprf_viewer = count_scores(new_dict, True)
score_wo_cprf_viewer = count_scores(new_dict, False)
print("| С представителем КПРФ: " + str(score_w_cprf_viewer) + " | " + " Без представителя КПРФ: " + str(
    score_wo_cprf_viewer) + " | " + "Разница: " + str(round(score_wo_cprf_viewer - score_w_cprf_viewer, 2)) + " |")
