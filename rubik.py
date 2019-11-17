
from Cubik import Cubik
import sys

all_actions = ["U", "R", "F", "D", "L", "B",
			   "U'", "R'", "F'", "D'", "L'", "B'",
			   "U2", "R2", "F2", "D2", "L2", "B2"
			   ]

def recurs_a_star(cubik, action, max_dep, stage=0, actions=all_actions):
	new_cubik = cubik.copy()
	new_cubik.apply_moves([action])

	if max_dep == 0:
		if new_cubik.heuristic_functions[stage]() == 0:
			return [action]

	if new_cubik.heuristic_functions[stage]() > max_dep:
		return None

	curr_actions = actions[:]
	curr_actions.remove(action)

	for act in curr_actions:
		res = recurs_a_star(new_cubik, act, max_dep - 1, stage, actions)

		if res != None:
			return [action] + res

	return None

if __name__ == '__main__':
	cubik = Cubik()

	# print(cubik.faces)
	
	# cubik.apply_moves(["U2", "B2", "B", "R2", "U'", "B'", "L", "F'"])
	# cubik.apply_moves(["U", "R"])
	# cubik.apply_moves(cubik.parse_moves("R2 D' B' D F2 R F2 R2 U L' F2 U' B' L2 R D B' R' B2 L2 F2 L2 R2 U2 D2"))

	# cubik.apply_moves(cubik.parse_moves("R U R D2 F R D' B2 L2 R F2 D' R F2 U L2 U' F2 U R2 U2 R2 D' B' D F2 R F2 R2 U L' F2 U' B'"))

	try:
		arg_str = " ".join(sys.argv[1:])
		cubik.apply_moves(cubik.parse_moves(arg_str))
	except Exception as ex:
		print("Error: bad argument input!")
		print("Error message:", ex)
		exit()
	
	cub_for_resolve = cubik.copy()

	curr_actions = all_actions[:]
	actions = []

	for stage in range(4):
		max_depth = cubik.heuristic_functions[stage]()
		all_res = []

		if stage == 1:
			curr_actions.remove('F')
			curr_actions.remove('B')
			curr_actions.remove("F'")
			curr_actions.remove("B'")
		elif stage == 2:
			curr_actions.remove('L')
			curr_actions.remove('R')
			curr_actions.remove("L'")
			curr_actions.remove("R'")
		elif stage == 3:
			curr_actions.remove('U')
			curr_actions.remove('D')
			curr_actions.remove("U'")
			curr_actions.remove("D'")

		for action in curr_actions:
			all_res = recurs_a_star(cubik, action, max_depth - 1, stage=stage, actions=curr_actions)

			if all_res != None:
				break

		if (all_res != None):
			cubik.apply_moves(all_res)

		if actions != None:
			actions += all_res

	cub_for_resolve.apply_moves(actions)
	# print("Solved =", cub_for_resolve.is_resolved())

	print(" ".join(actions))


