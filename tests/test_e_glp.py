from teacher_e import TeacherE as Target
teacher_name = "Teacher E"
teacher_list = []
for i in range(100):
    new_teacher = Target()
    teacher_list.append(new_teacher)
from l_star_inexperienced.grinchtein_et_al.glp_algorithm import GlpAlgorithm
total_num_calls = 0
total_clauses = 0
total_max_clauses = 0
total_conjectures = 0
max_num_calls = 0
max_total_clauses = 0
max_max_clauses = 0
max_conjectures = 0
algo_name = "GLP"

for i in range(100):
    print("iteration : ", i)

    algo = GlpAlgorithm(alphabet=['0','1'], teacher=teacher_list[i])

    result_dfa = algo.run(show_logs=True)

    total_num_calls += algo.num_calls
    max_num_calls = max(max_num_calls, algo.num_calls)

    total_clauses += algo.total_clauses
    max_total_clauses = max(max_total_clauses, algo.total_clauses)

    total_max_clauses += algo.max_clauses
    max_max_clauses = max(max_max_clauses, algo.max_clauses)

    total_conjectures += algo.total_conjectures
    max_conjectures = max(max_conjectures, algo.total_conjectures)


glp_results = {
    "Total num calls :" : total_num_calls,
    "Max num calls :": max_num_calls,
    "Total Clauses :": total_clauses,
    "Max Total Clauses :": max_total_clauses,
    "Total Max Clauses :": total_max_clauses,
    "Max Max Clauses :": max_max_clauses,
    "Total Conjectures :": total_conjectures,
    "Max Conjectures :": max_conjectures
}
print(teacher_name + " , " + algo_name + ", iterations = 100")

print("Total num calls :", glp_results["Total num calls :"])
print("Max num calls :", glp_results["Max num calls :"])

print("Total Clauses :", glp_results["Total Clauses :"])
print("Max Total Clauses :", glp_results["Max Total Clauses :"])

print("Total Max Clauses :", glp_results["Total Max Clauses :"])
print("Max Max Clauses :", glp_results["Max Max Clauses :"])

print("Total Conjectures :", glp_results["Total Conjectures :"])
print("Max Conjectures :", glp_results["Max Conjectures :"])


from l_star_inexperienced.leucker_et_al.lnl import LNLAlgorithm 
total_num_calls = 0
total_clauses = 0
total_max_clauses = 0
total_conjectures = 0
max_num_calls = 0
max_total_clauses = 0
max_max_clauses = 0
max_conjectures = 0
algo_name = "LNL"

for i in range(100):
    print("iteration : ", i)

    algo = LNLAlgorithm(alphabet=['0','1'], teacher=teacher_list[i])

    result_dfa = algo.run(show_logs=False)

    total_num_calls += algo.num_calls
    max_num_calls = max(max_num_calls, algo.num_calls)

    total_clauses += algo.total_clauses
    max_total_clauses = max(max_total_clauses, algo.total_clauses)

    total_max_clauses += algo.max_clauses
    max_max_clauses = max(max_max_clauses, algo.max_clauses)

    total_conjectures += algo.total_conjectures
    max_conjectures = max(max_conjectures, algo.total_conjectures)


lnl_results = {
    "Total num calls :" : total_num_calls,
    "Max num calls :": max_num_calls,
    "Total Clauses :": total_clauses,
    "Max Total Clauses :": max_total_clauses,
    "Total Max Clauses :": total_max_clauses,
    "Max Max Clauses :": max_max_clauses,
    "Total Conjectures :": total_conjectures,
    "Max Conjectures :": max_conjectures
}
print(teacher_name + " , " + algo_name + ", iterations = 100")

print("Total num calls :", lnl_results["Total num calls :"])
print("Max num calls :", lnl_results["Max num calls :"])

print("Total Clauses :", lnl_results["Total Clauses :"])
print("Max Total Clauses :", lnl_results["Max Total Clauses :"])

print("Total Max Clauses :", lnl_results["Total Max Clauses :"])
print("Max Max Clauses :", lnl_results["Max Max Clauses :"])

print("Total Conjectures :", lnl_results["Total Conjectures :"])
print("Max Conjectures :", lnl_results["Max Conjectures :"])

from l_star_inexperienced.chen_et_al.chen import ChenAlgorithm 
total_num_calls = 0
total_clauses = 0
total_max_clauses = 0
total_conjectures = 0
max_num_calls = 0
max_total_clauses = 0
max_max_clauses = 0
max_conjectures = 0
algo_name = "Chen"

for i in range(100):
    print("iteration : ", i)

    algo = ChenAlgorithm(alphabet=['0','1'], teacher=teacher_list[i])

    result_dfa = algo.run(show_logs=False)

    total_num_calls += algo.num_calls
    max_num_calls = max(max_num_calls, algo.num_calls)

    total_clauses += algo.total_clauses
    max_total_clauses = max(max_total_clauses, algo.total_clauses)

    total_max_clauses += algo.max_clauses
    max_max_clauses = max(max_max_clauses, algo.max_clauses)

    total_conjectures += algo.total_conjectures
    max_conjectures = max(max_conjectures, algo.total_conjectures)

algo_name = "GLP"

print(teacher_name + " , " + algo_name + ", iterations = 100")

print("Total num calls :", glp_results["Total num calls :"])
print("Max num calls :", glp_results["Max num calls :"])

print("Total Clauses :", glp_results["Total Clauses :"])
print("Max Total Clauses :", glp_results["Max Total Clauses :"])

print("Total Max Clauses :", glp_results["Total Max Clauses :"])
print("Max Max Clauses :", glp_results["Max Max Clauses :"])

print("Total Conjectures :", glp_results["Total Conjectures :"])
print("Max Conjectures :", glp_results["Max Conjectures :"])

algo_name = "Chen"

chen_results = {
    "Total num calls :" : total_num_calls,
    "Max num calls :": max_num_calls,
    "Total Clauses :": total_clauses,
    "Max Total Clauses :": max_total_clauses,
    "Total Max Clauses :": total_max_clauses,
    "Max Max Clauses :": max_max_clauses,
    "Total Conjectures :": total_conjectures,
    "Max Conjectures :": max_conjectures
}
print(teacher_name + " , " + algo_name + ", iterations = 100")

print("Total num calls :", chen_results["Total num calls :"])
print("Max num calls :", chen_results["Max num calls :"])

print("Total Clauses :", chen_results["Total Clauses :"])
print("Max Total Clauses :", chen_results["Max Total Clauses :"])

print("Total Max Clauses :", chen_results["Total Max Clauses :"])
print("Max Max Clauses :", chen_results["Max Max Clauses :"])

print("Total Conjectures :", chen_results["Total Conjectures :"])
print("Max Conjectures :", chen_results["Max Conjectures :"])


algo_name = "LNL"

print(teacher_name + " , " + algo_name + ", iterations = 100")

print("Total num calls :", lnl_results["Total num calls :"])
print("Max num calls :", lnl_results["Max num calls :"])

print("Total Clauses :", lnl_results["Total Clauses :"])
print("Max Total Clauses :", lnl_results["Max Total Clauses :"])

print("Total Max Clauses :", lnl_results["Total Max Clauses :"])
print("Max Max Clauses :", lnl_results["Max Max Clauses :"])

print("Total Conjectures :", lnl_results["Total Conjectures :"])
print("Max Conjectures :", lnl_results["Max Conjectures :"])