import json, math

N = 12
R1 = 60.0
R2 = 105.0

verts = [(0.0, 0.0)]
for r in (R1, R2):
    for i in range(N):
        a = 2 * math.pi * i / N
        verts.append((r * math.cos(a), r * math.sin(a)))

def I(i): return 1 + (i % N)
def O(i): return 1 + N + (i % N)

edges, assign, fold_angles, lookup = [], [], [], {}

def edge(a, b, typ, angle=0):
    k = tuple(sorted((a, b)))
    if k in lookup:
        return lookup[k]
    j = len(edges)
    edges.append([a, b])
    assign.append(typ)
    fold_angles.append(angle)
    lookup[k] = j
    return j

# Layer 1: Chinese-fan radial folds
for i in range(N):
    typ = "M" if i % 2 == 0 else "V"
    edge(0, I(i), typ, -90 if typ == "M" else 90)

# Interface ring
for i in range(N):
    typ = "V" if i % 2 == 0 else "M"
    edge(I(i), I(i+1), typ, 90 if typ == "V" else -90)

# Layer 2: endpoint collar
for i in range(N):
    typ = "V" if i % 2 == 0 else "M"
    edge(I(i), O(i), typ, 90 if typ == "V" else -90)

for i in range(N):
    if i % 2 == 0:
        edge(I(i+1), O(i), "M", -90)
    else:
        edge(I(i), O(i+1), "V", 90)

for i in range(N):
    edge(O(i), O(i+1), "B", 0)

faces = []
for i in range(N):
    faces.append([0, I(i), I(i+1)])

for i in range(N):
    if i % 2 == 0:
        faces.append([I(i), I(i+1), O(i)])
        faces.append([I(i+1), O(i+1), O(i)])
    else:
        faces.append([I(i), I(i+1), O(i+1)])
        faces.append([I(i), O(i+1), O(i)])

fold = {
    "file_spec": 1.1,
    "file_creator": "Two-layer Chinese-fan/counter-collar prototype",
    "frame_title": "12-sector fan with triangular endpoint collar",
    "vertices_coords": verts,
    "edges_vertices": edges,
    "edges_assignment": assign,
    "edges_foldAngle": fold_angles,
    "faces_vertices": faces
}

with open("two_layer_chinese_fan_prototype.fold", "w") as f:
    json.dump(fold, f, indent=2)
