from teacher_b import TeacherB as Target
teacher_name = "Teacher B"
from l_star_inexperienced.grinchtein_et_al.glp_algorithm import GlpAlgorithm

# glp = GlpAlgorithm(alphabet=['a', 'b', 'c'], teacher=TeacherD())
# # TeacherC().accepting_fa.visualize()
# # TeacherC().rejecting_fa.visualize()

# result_dfa = glp.run(show_logs=True)
# result_dfa.visualize()
total_num_calls = 0
total_clauses = 0
total_max_clauses = 0
total_conjectures = 0
max_num_calls = 0
max_total_clauses = 0
max_max_clauses = 0
max_conjectures = 0

for i in range(100):
    print("iteration : ", i)
    glp = GlpAlgorithm(alphabet=['a', 'b', 'c'], teacher=Target())

    result_dfa = glp.run(show_logs=False)
    # result_dfa.visualize()

    total_num_calls += glp.num_calls
    max_num_calls = max(max_num_calls, glp.num_calls)

    total_clauses += glp.total_clauses
    max_total_clauses = max(max_total_clauses, glp.total_clauses)

    total_max_clauses += glp.max_clauses
    max_max_clauses = max(max_max_clauses, glp.max_clauses)

    total_conjectures += glp.total_conjectures
    max_conjectures = max(max_conjectures, glp.total_conjectures)

print(teacher_name + " , GLP, iterations = 100")

print("Total num calls : ", total_num_calls)
print("Max num calls : ", max_num_calls)

print("Total Clauses : ", total_clauses)
print("Max Total Clauses : ", max_total_clauses)

print("Total Max Clauses : ", total_max_clauses)
print("Max Max Clauses : ", max_max_clauses)

print("Total Conjectures : ", total_conjectures)
print("Max Conjectures : ", max_conjectures)
