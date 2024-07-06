from l_star_inexperienced.common.conjecture_solver import find_solution # type: ignore
from l_star_inexperienced.common.constants import _Const # type: ignore
from l_star_inexperienced.grinchtein_et_al.glp_algorithm import GlpAlgorithm # type: ignore
from l_star_inexperienced.teachers.test_teacher import TestTeacher # type: ignore

CONST = _Const()

if __name__ == "__main__":
    glp_algorithm = GlpAlgorithm(alphabet=['0', '1'], teacher=TestTeacher())
    print("GLP Algo Object initialized")
    glp_algorithm.obs_table.print_table()
    print(glp_algorithm.is_obs_table_closed())
    print(glp_algorithm.is_obs_table_consistent())
    # Logic changed, proper things still pending
    print("This is not closed because of extended row 00 not having a match")
    print("Lets try fixing it")
    glp_algorithm.make_initial_conjecture()
    print(glp_algorithm.is_obs_table_closed())
    print(glp_algorithm.is_obs_table_consistent())
    print(glp_algorithm.obs_table.extended_table_component)
    print(glp_algorithm.get_s_plus())
    print(glp_algorithm.get_s_minus())
    proposed_dfa = find_solution(glp_algorithm.obs_table, 
                    glp_algorithm.get_s_plus(), 
                    glp_algorithm.get_s_minus())
    proposed_dfa.print_parameters()
    print(proposed_dfa.get_state_for_word("010010010111111"))
    print(proposed_dfa.is_word_accepted("010010010111111"))




