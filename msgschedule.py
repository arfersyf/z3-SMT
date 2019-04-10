import numpy as np
from z3 import *

# generate msg
msg_cnt = 4
msg_array = [[] for i in range(msg_cnt)]

task_cnt = 6
# generate topo
node_cnt = 3
topo_link_hops = [[] for i in range(node_cnt*node_cnt)]

def generate_msg():
    for i in range(msg_cnt):
        msg_array[i].append(np.random.randint(0, node_cnt*node_cnt))  # source
        msg_array[i].append(np.random.randint(0, node_cnt*node_cnt))  # destination
        msg_array[i].append(np.random.randint(100, 1000))  # length
        msg_array[i].append(np.random.randint(1, 7))  # period
        msg_array[i].append(msg_array[i][2] * 31 // (5 * 1000) + 1)  # 经过hop的时间

generate_msg()


for i in range(msg_cnt):
    if msg_array[i][0] == msg_array[i][1]:
        msg_array[i][1] += 1
print("msg_array:")
print(msg_array)

def generate_topo(node_cnt):
    for i in range(node_cnt*node_cnt):
        for j in range(node_cnt*node_cnt):
            if(i == j):
                topo_link_hops[i].append(0)
            else:
                topo_link_hops[i].append(abs(i//node_cnt - j//node_cnt) + abs(i%node_cnt - j%node_cnt))

generate_topo(node_cnt)
print_matrix(topo_link_hops)


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

#if s.check() == sat:
#    m = s.model()
#    r = [[ m.evaluate(msg_node[i][j]) for j in range(node_cnt*node_cnt)] for i in range(msg_cnt)]
#    print("msg_node:")
#    print_matrix(r)
#    v = [[[m.evaluate(msg_link[i][j][k])
#          for k in range(node_cnt*node_cnt)] for j in range(node_cnt*node_cnt)] for i in range(msg_cnt)]
#    print("msg_link:")
#    print_matrix(v)
#else:
#    print("failed to solve")

# 超周期
hyper_period = 5  # 2**(n-1)ms

msg_schedule_offset = [[[[Int('o_%s_%s_%s_%s' %(msg, node, node2, period))
                          for period in range(2**(hyper_period + 1 - msg_array[msg][3]))]
                         for node2 in range(node_cnt*node_cnt)]
                        for node in range(node_cnt*node_cnt)]
                       for msg in range(msg_cnt)]

# con1: 0-999
onethousand_c = [And(0 <= msg_schedule_offset[msg][i][j][p], msg_schedule_offset[msg][i][j][p] < 1000 * (2**(msg_array[msg][3] - 1)))
                 for msg in range(msg_cnt)
                 for i in range(node_cnt * node_cnt)
                 for j in range(node_cnt * node_cnt)
                 for p in range(2**(hyper_period + 1 - msg_array[msg][3]))
                 ]
#print(onethousand_c)
zerolink_c = [And(If(msg_link[msg][i][j] != 0, True, msg_schedule_offset[msg][i][j][p] == 0),
                  If(msg_link[msg][i][j] == 0, True, msg_schedule_offset[msg][i][j][p] != 0))
              for msg in range(msg_cnt)
              for i in range(node_cnt * node_cnt)
              for j in range(node_cnt * node_cnt)
              for p in range(2**(hyper_period + 1 - msg_array[msg][3]))
              ]
#print(zerolink_c)

# con2: 同一消息从源开始后一个比前一个大,并且连续
src_samemsg_c = [If(Or(msg_link[msg][msg_array[msg][0]][i] == 0, msg_link[msg][i][j] == 0), True,
                    And(msg_schedule_offset[msg][msg_array[msg][0]][i][p] + msg_array[msg][4] < msg_schedule_offset[msg][i][j][p],
                        msg_schedule_offset[msg][msg_array[msg][0]][i][p] + msg_array[msg][4] + 2 > msg_schedule_offset[msg][i][j][p]))
                 for msg in range(msg_cnt)
                 for i in range(node_cnt * node_cnt)
                 for j in range(node_cnt * node_cnt)
                 for p in range(2**(hyper_period + 1 - msg_array[msg][3]))
                 ]
#print(src_samemsg_c)
link_samemsg_c = [If(Or(msg_link[msg][i][j] == 0, msg_link[msg][j][k] == 0), True,
                     And(msg_schedule_offset[msg][i][j][p] + msg_array[msg][4] < msg_schedule_offset[msg][j][k][p],
                         msg_schedule_offset[msg][i][j][p] + msg_array[msg][4] + 2 > msg_schedule_offset[msg][j][k][p]))
                  for msg in range(msg_cnt)
                  for i in range(node_cnt * node_cnt)
                  for j in range(node_cnt * node_cnt)
                  for k in range(node_cnt * node_cnt)
                  for p in range(2**(hyper_period + 1 - msg_array[msg][3]))
                  ]

dest_samemsg_c = [msg_schedule_offset[msg][i][msg_array[msg][1]][p] + msg_array[msg][4] < 1000 * (2**(msg_array[msg][3] - 1))
                  for msg in range(msg_cnt)
                  for i in range(node_cnt*node_cnt)
                  for p in range(2**(hyper_period + 1 - msg_array[msg][3]))
                  ]



# con3: 不同消息路径相同，offset不同
samelink_c = [If(Or(Or(msg_link[msg1][i][j] == 0, msg_link[msg2][i][j] == 0), msg1 == msg2), True,
                 Or(msg_schedule_offset[msg1][i][j][p1] + 2 ** msg_array[msg1][3] * 1000 * p1 >
                    msg_schedule_offset[msg2][i][j][p2] + 2 ** msg_array[msg2][3] * 1000 * p2 + msg_array[msg2][4],
                    msg_schedule_offset[msg2][i][j][p2] + 2 ** msg_array[msg2][3] * 1000 * p2 >
                    msg_schedule_offset[msg1][i][j][p1] + 2 ** msg_array[msg1][3] * 1000 * p1 + msg_array[msg1][4]
                    ))
              for msg1 in range(msg_cnt)
              for msg2 in range(msg_cnt)
              for i in range(node_cnt * node_cnt)
              for j in range(node_cnt * node_cnt)
              for p1 in range(2**(hyper_period + 1 - msg_array[msg1][3]))
              for p2 in range(2**(hyper_period + 1 - msg_array[msg2][3]))
              ]
#print(samelink_c)

s.add(onethousand_c + zerolink_c + src_samemsg_c + link_samemsg_c + dest_samemsg_c +samelink_c)
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(msg_node[i][j]) for j in range(node_cnt * node_cnt)] for i in range(msg_cnt)]
    print("msg_node:")
    print_matrix(r)
    v = [[[m.evaluate(msg_link[i][j][k])
           for k in range(node_cnt * node_cnt)] for j in range(node_cnt * node_cnt)] for i in range(msg_cnt)]
    print("msg_link:")
    print_matrix(v)
    s = [[[[m.evaluate(msg_schedule_offset[i][j][k][p])
           for p in range(2**(hyper_period + 1 - msg_array[i][3]))] for k in range(node_cnt * node_cnt)] for j in range(node_cnt * node_cnt)] for i in range(msg_cnt)]
    print("msg_schedule:")
    for msg in range(msg_cnt):
        print(s[msg])
else:
    print("failed to solve")
