# 마트 장보기 최단경로 API

## 📌 목차  
0. 요약
1. 실행 방법
2. API 예시
3. 주요 코드 설명 
4. 레퍼런스

# 0. 요약

![Image](https://github.com/user-attachments/assets/d00173f0-b4c7-4427-b1a0-cb7d013ce9f2)

마트 장보기 최단경로 문제를 외판원 문제(**Travelling Salesman Problem, TSP)로 접근했으며, 플로이드-워셜, held-karp, 2-opt 알고리즘을 사용하여 풀었습니다 [1][2][3].**

# 1. 실행 방법

```python
# 1. git clone.
git clone https://github.com/kdoubleh22/shortest-path.git

# 2. 프로젝트 폴더로 이동.
cd shortest-path

# 3. docker 빌드.
docker build -t name .

# 4. docker run.
docker run -p 80:80 name
```

# 2. API 예시

<img width="535" alt="Image" src="https://github.com/user-attachments/assets/0cfd93f7-c5f1-4a75-becd-b3b2b9aaebf7" />

# 3. 주요 코드 설명

## 3-1. main.py

```jsx
# distance matrix 초기화.
DISTANCE_MATRIX = make_distance_matrix(INF)
```

map_coordinates.txt 파일의 좌표를 읽어, distance matrix를 생성합니다.

플로이드-워셜 알고리즘을 활용하여 거리와 경로 모두 저장해줍니다 [4]. (추후 실제 경로 생성에 활용됩니다)

```python
visit_list = deepcopy(locations.item_locations)
start_location = locations.start_location
visit_list.insert(0,start_location)
visit_list.append(73)
```

물건들의 위치 list 앞에는 시작위치를, 뒤에는 계산대(73)를 붙여 TSP 알고리즘을 적용할 정점 list를 완성합니다.

visit_list 예시: [0, 1, 7, 9, 73]

```python
    # TSP 알고리즘을 적용하기 위해, 방문하는 위치들만으로 부분 그래프(sub graph) 만들기.
    # 부분 그래프 만들기.
    l = len(visit_list)
    sub_graph = [[-1 for i in range(l)] for i in range(l)]
    for r in range(l):
        for c in range(l):
            sub_graph[r][c] = SHORTEST_DISTANCES[visit_list[r]][visit_list[c]]
    # - sub_graph:
    # 0.00 13.4 11.4 10.3 5.63
    # 13.4 0.00 4.13 4.17 11.6
    # 11.4 4.13 0.00 2.11 9.65
    # 10.3 4.17 2.11 0.00 8.51
    # 5.63 11.6 9.65 8.51 0.00
```

위에서 만든 visit_list로 sub graph를 만듭니다.

sub graph를 만들지 않으면, 0~73번 정점 모두를 방문하는 의미 없는 경로가 나오기 때문입니다.

```python
# 방문해야할 장소 개수가 14개 미만일 때는 최적 해 algorithm인 held-karp algorithm 적용.
# 방문해야할 장소 개수가 14개 이상일 때는 heuristic algorithm인 2-opt algorithm 적용.
if l < 14:
    shortest_distance, temp_path = held_karp(sub_graph,INF)
else:
    # 입력 형태를 맞추기 위해, sub_graph를 numpy array로 변환해줌.
    sub_graph_np_array = np.array(sub_graph)

    # seed 초기화. seed[0]는 경로를, seed[1]은 거리를 의미.
    seed=[[],[]]

    # path 초기화는 숫자가 낮은 순서로 방문.
    seed[0]=[ i for i in range(len(sub_graph_np_array))]
    seed[1] = distance_calc(sub_graph_np_array,seed)

    temp_path,shortest_distance = local_search_2_opt(sub_graph_np_array,seed,-1,True)
```

시간 복잡도를 고려하여 물건의 개수에 따라 최적해 알고리즘인 held-karp 알고리즘과 휴리스틱 알고리즘인 2-opt 알고리즘을 적용하여 temp_path에 저장합니다 [5].

temp_path 예시: [0, 3, 2, 1, 4]

temp_path의 요소는 visit_list의 인덱스를 의미합니다.

즉, 실제 방문순서는 0 -> 9 -> 7 -> 1 -> 73 입니다.

```python
# 실제 경로로 변환해주기.
real_path = [start_location]
temp_path_len = len(temp_path)
for i in range(temp_path_len-1):
    real_path.extend(SHORTEST_PATHS[visit_list[temp_path[i]]][visit_list[temp_path[i+1]]][1:])
```

0 → 9 → 7 → 1 → 13 을 실제 경로로 변환해줍니다. (플로이드-워셜 알고리즘 활용 때 저장해둔 경로 사용)

real_path(실제 경로) 예시: [0, 71, 70, 69, 68, 58, 55, 52, 48, 45, 9, 45, 42, 39, 7, 39, 42, 41, 35, 1, 35, 41, 47, 51, 57, 63, 64, 65, 66, 67, 68, 69, 70, 73]

## 3-2. held_karp.py

```python
# 가중치 조정하여 끝 정점(계산대) 고정하기.
# 끝 정점 -> 시작 정점 간선의 가중치는 0으로.
dists[n - 1][0] = 0
# 끝 정점을 제외한 나머지 정점 -> 시작 정점 간선의 가중치는 INF로.
for r in range(1, n - 1):
    dists[r][0] = INF
```

held-karp 알고리즘은 TSP solving 알고리즘으로, 최소 비용을 갖는 해밀턴 순환 경로를 반환합니다 [6].

하지만 프로젝트에서는 끝 정점을 계산대로 고정하기 위해 위와같이 가중치를 조절하여 맨 끝에 계산대 → 시작위치 경로를 고정합니다 [7].

고정이 되는 이유는 TSP 알고리즘은 순환 경로를 반환하는데, 시작 정점으로 돌아오는 간선의 가중치(0, INF) 중 0(끝정점 → 시작정점 간선의 가중치)이 반드시 선택되기 때문입니다.

## 3-3. two_opt.py

```python
for i in range(1, len(city_list[0]) - 2):
    for j in range(i+1, len(city_list[0]) - 1):
        best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))
        # best_route[0][-1]    = best_route[0][0]     
```

순환 경로가 아닌, 시작점과 끝점을 고정 하기 위해 for문 범위를 바꾸고, 불필요한 코드는 주석 처리합니다.

레퍼런스 코드는 초기경로를 [0, 1, 2, 3, 4, 0] 으로 세팅 후, [2, 1, 0, 3, 4, 2] 와 같이 시작점과 끝점이 변할 수 있습니다 [8].

프로젝트 코드는 초기경로를 [0, 1, 2, 3, 4] 로 세팅 후, [0, 3, 2, 1, 4] 와 같이 시작점과 끝점을 고정합니다.

# 4. 레퍼런스

[[1] 외판원 문제](https://ko.wikipedia.org/wiki/%EC%99%B8%ED%8C%90%EC%9B%90_%EB%AC%B8%EC%A0%9C)

[[2] held-karp](https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm)

[[3] 2-opt](https://ko.wikipedia.org/wiki/2-OPT)

[[4] Finding shortest path between any two nodes using Floyd Warshall Algorithm](https://www.geeksforgeeks.org/finding-shortest-path-between-any-two-nodes-using-floyd-warshall-algorithm/)

[[5] Heuristics for the Traveling Salesman Problem by Christian Nilsson](https://www.isid.ac.in/~dmishra/doc/htsp.pdf)

[[6] https://github.com/CarlEkerot/held-karp](https://github.com/CarlEkerot/held-karp)

[[7] https://stackoverflow.com/questions/36086406/traveling-salesman-tsp-with-set-start-and-end-point](https://stackoverflow.com/questions/36086406/traveling-salesman-tsp-with-set-start-and-end-point)

[[8] https://github.com/Valdecy/pyCombinatorial](https://github.com/Valdecy/pyCombinatorial)
