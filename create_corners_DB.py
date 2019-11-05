from rubik import Cubik
import pandas as pd

all_actions = ["U", "R", "F", "D", "L", "B",
			   "U'", "R'", "F'", "D'", "L'", "B'",
			   "U2", "R2", "F2", "D2", "L2", "B2"
			   ]

corners = [1,3,6,8,9,11,24,26,12,14,27,29,15,17,30,32,41,43,46,48,33,35,38,40]

db = []

def recursion(cubik, i, action, prev_action, prev_actions):
	if i > 3:
		return None

	new_cubik = cubik.copy()
	new_cubik.apply_moves([action])

	for corner in corners:
		new_pos = new_cubik.get_new_pos(corner)

		if corner != new_pos:
			db.append( [corner, new_pos, i+1, prev_actions[0], prev_actions[1] if len(prev_actions) > 1 else None, prev_actions[2] if len(prev_actions) > 2 else None] )

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

	df_db = pd.DataFrame(db, columns=['corner', 'position', 'grade', 'first_move', 'second_move', 'third_move'])
	filtered_db = pd.DataFrame()

	for corner1 in corners:
		for corner2 in corners:
			if (corner1 == corner2):
				continue

			df_min = df_db[(df_db['corner'] == corner1) & (df_db['position'] == corner2)]['grade'].min()
			df_db_min = df_db[(df_db['corner'] == corner1) & (df_db['position'] == corner2) & (df_db['grade'] == df_min)].drop_duplicates()
			filtered_db = pd.concat([filtered_db, df_db_min], ignore_index=True)

	# filtered_db = pd.DataFrame(filtered_db, columns=['corner', 'position', 'grade'])
	filtered_db.to_csv("corner_moves_db.csv")
