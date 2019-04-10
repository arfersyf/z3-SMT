import numpy as np
from z3 import *

# generate msg
msg_cnt = 10
msg_array = [[] for i in range(msg_cnt)]

task_cnt = 10
# generate topo
node_cnt = 4
topo_link_hops = [[] for i in range(node_cnt*node_cnt)]

def generate_msg():
    for i in range(msg_cnt):
        msg_array[i].append(np.random.randint(0, 16))  # source
        msg_array[i].append(np.random.randint(0, 16))  # destination
        msg_array[i].append(np.random.randint(100, 1000))  # length
        msg_array[i].append(np.random.randint(1, 8))  # period

generate_msg()
print(msg_array)

for i in range(msg_cnt):
    if msg_array[i][0] == msg_array[i][1]:
        msg_array[i][1] += 1


def generate_topo(node_cnt):
    for i in range(node_cnt*node_cnt):
        for j in range(node_cnt*node_cnt):
            if(i == j):
                topo_link_hops[i].append(0)
            else:
                topo_link_hops[i].append(abs(i//node_cnt - j//node_cnt) + abs(i%node_cnt - j%node_cnt))

generate_topo(node_cnt)
print(topo_link_hops)


# msg to node
msg_node = [[[Int('x_%s_%s_%s' %(msg, node1, node2))
              for node2 in range(node_cnt)] for node1 in range(node_cnt)]for msg in range(msg_cnt)]
# msg to link
msg_link = [[[Int('y_%s_%s_%s' %(msg, node, node2))
              for node2 in range(node_cnt*node_cnt)] for node in range(node_cnt*node_cnt)]for msg in range(msg_cnt)]


# cons1: 0/1 node 2 src/dest
onezero_c  = [ And(0 <= msg_node[i][j][k], msg_node[i][j][k] <= 1)
             for i in range(msg_cnt) for j in range(node_cnt) for k in range(node_cnt)]
onezero2_c = [ And(0 <= msg_link[i][j][k], msg_link[i][j][k] <= 1)
             for i in range(msg_cnt) for j in range(node_cnt*node_cnt) for k in range(node_cnt*node_cnt)]
link_c = [If(topo_link_hops[i][j] == 1, True, msg_link[msg][i][j] == 0)
          for msg in range(msg_cnt) for i in range(node_cnt*node_cnt) for j in range(node_cnt*node_cnt)]

# cons2: src/dest node and link
srcdest_c = [ And(msg_node[i][msg_array[i][0]//node_cnt][msg_array[i][0]%node_cnt] == 1,
                  msg_node[i][msg_array[i][1]//node_cnt][msg_array[i][1]%node_cnt] == 1,
                  Sum(msg_link[i][msg_array[i][0]]) == 1,
                  Sum([a[msg_array[i][0]] for a in msg_link[i]]) == 0,
                  Sum([a[msg_array[i][1]] for a in msg_link[i]]) == 1,
                  Sum(msg_link[i][msg_array[i][1]]) == 0)
               for i in range(msg_cnt)]


# cons3: link to node
linknode_c = [ If(msg_link[msg][i][j] != 1, True,
                  And(msg_node[msg][i//node_cnt][i%node_cnt] == 1,
                      msg_node[msg][j//node_cnt][j%node_cnt] == 1))
               for msg in range(msg_cnt) for i in range(node_cnt*node_cnt) for j in range(node_cnt*node_cnt)]

# cons4: node oneinoneout
nodeonein_c = [If(Or(msg_node[msg][i][j] != 1, i*node_cnt + j == msg_array[msg][0]), True,
                  Sum([a[i*node_cnt + j] for a in msg_link[msg]])==1)
               for msg in range(msg_cnt) for i in range(node_cnt) for j in range(node_cnt)]

nodeoneout_c = [If(Or(msg_node[msg][i][j] != 1, i*node_cnt + j == msg_array[msg][1]), True,
                  Sum(msg_link[msg][i*node_cnt + j])==1)
               for msg in range(msg_cnt) for i in range(node_cnt) for j in range(node_cnt)]

# cons5: 两个node同出同入
twonode1_c = [Not(And(msg_link[msg][i][j] == 1 , msg_link[msg][j][i] == 1))
              for msg in range(msg_cnt) for i in range(node_cnt*node_cnt) for j in range(node_cnt*node_cnt)]

# cons6: length
def flatten(a):
    for each in a:
        if not isinstance(each, list):
            yield each
        else:
            yield from flatten(each)


for msg in range(msg_cnt):
    msg_node[msg] = list(flatten(msg_node[msg]))

length_c = [Sum(msg_node[i]) <= topo_link_hops[msg_array[i][0]][msg_array[i][1]] + 2 for i in range(msg_cnt)]


s = Solver()
s.add(onezero_c + onezero2_c + link_c + srcdest_c + linknode_c + nodeonein_c + nodeoneout_c + length_c + twonode1_c)
if s.check() == sat:
    m = s.model()
    r = [[ m.evaluate(msg_node[i][j]) for j in range(node_cnt*node_cnt)] for i in range(msg_cnt)]
    print_matrix(r)
    v = [[[m.evaluate(msg_link[i][j][k])
          for k in range(node_cnt*node_cnt)] for j in range(node_cnt*node_cnt)] for i in range(msg_cnt)]
    print_matrix(v)
else:
    print("failed to solve")
