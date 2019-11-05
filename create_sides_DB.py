from rubik import Cubik
import pandas as pd

all_actions = ["U", "R", "F", "D", "L", "B",
			   "U'", "R'", "F'", "D'", "L'", "B'",
			   "U2", "R2", "F2", "D2", "L2", "B2"
			   ]

sides = [2,4,5,7,10,18,19,25,13,20,21,28,16,22,23,31,42,44,45,47,34,36,37,39]

db = []

def recursion(cubik, i, action, prev_action, prev_actions):
	if i > 3:
		return None

	new_cubik = cubik.copy()
	new_cubik.apply_moves([action])

	for side in sides:
		new_pos = new_cubik.get_new_pos(side)

		if side != new_pos:
			db.append( [side, new_pos, i+1, prev_actions[0], prev_actions[1] if len(prev_actions) > 1 else None, prev_actions[2] if len(prev_actions) > 2 else None] )

	new_actions = all_actions[:]

	if prev_action == None:
		pass
	elif prev_action[-1] == "'":
		del new_actions[new_actions.index(prev_action[0])]
	elif prev_action[-1] != '2':
		del new_actions[new_actions.index(prev_action + "'")]

	for act in all_actions:
		recursion(new_cubik, i+1, act, action, prev_actions + [act])


if __name__ == '__main__':
	cubik = Cubik()

	for i, action in enumerate(all_actions):
		print("Start recursion for action " + action)
		recursion(cubik, 0, action, None, [action])
		print("Done in", i+1, "/", len(all_actions))

	df_db = pd.DataFrame(db, columns=['side', 'position', 'grade', 'first_move', 'second_move', 'third_move'])
	filtered_db = pd.DataFrame()

	for side1 in sides:
		for side2 in sides:
			if (side1 == side2):
				continue

			df_min = df_db[(df_db['side'] == side1) & (df_db['position'] == side2)]['grade'].min()
			df_db_min = df_db[(df_db['side'] == side1) & (df_db['position'] == side2) & (df_db['grade'] == df_min)].drop_duplicates()
			filtered_db = pd.concat([filtered_db, df_db_min], ignore_index=True)

	# filtered_db = pd.DataFrame(filtered_db, columns=['side', 'position', 'grade', 'first_move', 'second_move', 'third_move'])
	filtered_db.to_csv("side_moves_db.csv")
