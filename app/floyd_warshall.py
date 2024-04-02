# Python3 program to find the shortest
# path between any two nodes using
# Floyd Warshall Algorithm.

# Initializing the distance and
# Next array
def initialize(dis,Next,V,INF,GRAPH):
	for i in range(V):
		for j in range(V):
			dis[i][j] = GRAPH[i][j]

			# No edge between node
			# i and j
			if (GRAPH[i][j] == INF):
				Next[i][j] = -1
			else:
				Next[i][j] = j

# Function construct the shortest
# path between u and v
def constructPath(u, v, Next):
	
	# If there's no path between
	# node u and v, simply return
	# an empty array
	if (Next[u][v] == -1):
		return {}

	# Storing the path in a vector
	path = [u]
	while (u != v):
		u = Next[u][v]
		path.append(u)

	return path

# Standard Floyd Warshall Algorithm
# with little modification Now if we find
# that dis[i][j] > dis[i][k] + dis[k][j]
# then we modify next[i][j] = next[i][k]
def floydWarshall(dis,Next,V,INF):
	for k in range(V):
		for i in range(V):
			for j in range(V):
				
				# We cannot travel through
				# edge that doesn't exist
				if (dis[i][k] == INF or dis[k][j] == INF):
					continue
				if (dis[i][j] > dis[i][k] + dis[k][j]):
					dis[i][j] = dis[i][k] + dis[k][j]
					Next[i][j] = Next[i][k]

# 위 함수들을 사용하여 프로젝트의 최단 거리, 최단 경로 초기화.
def floyd_warshall_initialize(DISTANCE_MATRIX,INF):
	# 총 vertices 개수
	V = len(DISTANCE_MATRIX)

	SHORTEST_DISTANCES = [[-1 for i in range(V)] for i in range(V)]
	Next = [[-1 for i in range(V)] for i in range(V)]

	initialize(SHORTEST_DISTANCES,Next,V,INF,DISTANCE_MATRIX)

	# r에서 c로 가는 최단 거리 구하기.
	floydWarshall(SHORTEST_DISTANCES,Next,V,INF)

	# r에서 c로 가는 최단 경로 구하기.
	SHORTEST_PATHS = [[-1 for i in range(V)] for i in range(V)]   
	for r in range(V):
		for c in range(V):
			SHORTEST_PATHS[r][c]=constructPath(r,c,Next)

	return SHORTEST_DISTANCES, SHORTEST_PATHS