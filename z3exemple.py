from z3 import *


# 数据类型：Real  Int  Bool
# 数学符号：**幂  ^ and  or


# 简单求解 Solver()   add

#x = Real('x')
#y = Real('y')
#s = Solver()
#s.add(x + y <3, x > 1, y > 1)
#print(s.check())
#print(s.model())


# 简化方程 simplify()
#x = Int('x')
#y = Int('y')
#print(simplify(x + y + 2*x + 3))
#print(simplify(x < y + x + 2))
#print(simplify(And(x + 1 >= 3, x**2 + x**2 + y**2 + 2 >= 5)))



# set_option(html_mode=False) 不懂
#x = Int('x')
#y = Int('y')
#print(x**2 + y**2 >= 1)
#set_option(html_mode=False)
#print(x**2 + y**2 >= 1)


# 设置小数点位数     输出？表示数据被缩短
#x = Real('x')
#y = Real('y')
#solve(x**2 + y**2 == 3, x**3 == 2)

#set_option(precision=30)     #小数点位数
#print("Solving, and displaying result with 30 decimal places")
#solve(x**2 + y**2 == 3, x**3 == 2)




# 穿越公式（个人理解  解析公式）
#x = Int('x')
#y = Int('y')
#n = x + y >= 3
#print("num args: ", n.num_args())
#print("children: ", n.children())
#print("1st child:", n.arg(0))
#print("2nd child:", n.arg(1))
#print("operator: ", n.decl())
#print("op name:  ", n.decl().name())



# z3创建有理数Q(NUM, DEL) 分子，分母  创建实数RealVal(1)
#print(1/3)
#print(RealVal(1)/3)
#print(Q(1,3))

#x = Real('x')
#print(x + 1/3)
#print(x + Q(1,3))
#print(x + "1/3")
#print(x + 0.25)


# 有理数展示为小数
#x = Real('x')
#solve(3*x == 1)

#set_option(rational_to_decimal=True)   #有理数变小数
#solve(3*x == 1)

#set_option(precision=30)
#solve(3*x == 1)


#无解情况
#x = Real('x')
#solve(x > 4, x < 0)   # no solution


# Bool操作   And, Or, Not, Implies (implication), If (if-then-else)
#p = Bool('p')
#q = Bool('q')
#r = Bool('r')
#solve(Implies(p, q), r == Not(q), Or(Not(p), r))


#p = Bool('p')
#q = Bool('q')
#print(And(p, q, True))
#print(simplify(And(p, q, True)))
#print(simplify(And(p, False)))


#p = Bool('p')
#x = Real('x')
#solve(Or(x < 5, x > 10), Or(p, x**2 == 2), Not(p))


# Solver      add(添加条件)   check(是否可行)   model(可行的答案)   push和pop一起用，这两个中间加的条件只在这两句语句中间有效

#x = Int('x')
#y = Int('y')

#s = Solver()
#print(s)

#s.add(x > 10, y == x + 2)
#print(s)
#print("Solving constraints in the solver s ...")
#print(s.check())
#print(s.model())

#print("Create a new scope...")
#s.push()
#s.add(y < 11)
#print(s)
#print("Solving updated set of constraints...")
#print(s.check())

#s.add(y>1)
#print(s)
#print(s.check())

#print("Restoring state...")
#s.pop()
#print(s)
#print("Solving restored set of constraints...")
#print(s.check())
#print(s.model())


# 2**x不是多项式，不可求解   unknown
#x = Real('x')
#s = Solver()
#s.add(2**x == 3)
#print(s.check())


# 没看懂
#x = Real('x')
#y = Real('y')
#s = Solver()
#s.add(x > 1, y > 1, Or(x + y > 3, x - y < 2))
#print("asserted constraints...")
#for c in s.assertions():
#    print(c)

#print(s.check())
#print("statistics for the last check method...")
#print(s.statistics())
# Traversing statistics
#for k, v in s.statistics():
#    print("%s : %s" % (k, v))



# 缩写Real
#x, y, z = Reals('x y z')
#s = Solver()
#s.add(x > 1, y > 1, x + y > 3, z - x < 10)
#print(s.check())

#m = s.model()
#print("x = %s" % m[x])

#print("traversing model...")
#for d in m.decls():
#    print("%s = %s" % (d.name(), m[d]))   # 模型的解


# 计算过程中可能把一个整型转换成实数型
#x = Real('x')
#y = Int('y')
#a, b, c = Reals('a b c')
#s, r = Ints('s r')
#print(x + y + 1 + (a + s))
#print(ToReal(y) + c)

#  支持所有的数学表达式
#a, b, c = Ints('a b c')
#d, e = Reals('d e')
#solve(a > b + 2,
#      a == 2*c + 10,
#      c + b <= 1000,
#      d >= e)


# 不同形式的化简
#x, y = Reals('x y')
# Put expression in sum-of-monomials form
#t = simplify((x + y)**3, som=True)
#print(t)
# Use power operator
#t = simplify(t, mul_to_power=True)
#print(t)


#不懂
#x, y = Reals('x y')
# Using Z3 native option names
#print(simplify(x == y + 2, ':arith-lhs', True))
# Using Z3Py option names
#print(simplify(x == y + 2, arith_lhs=True))

#print("\nAll available options:")
#help_simplify()


#不懂
#x, y = Reals('x y')
#solve(x + 10000000000000000000000 == y, y > 20000000000000000)

#print(Sqrt(2) + Sqrt(3))
#print(simplify(Sqrt(2) + Sqrt(3)))
#print(simplify(Sqrt(2) + Sqrt(3)).sexpr())
# The sexpr() method is available for any Z3 expression
#print((x + Sqrt(y) * 2).sexpr())

# 求解函数
#x = Int('x')
#y = Int('y')
#f = Function('f', IntSort(), IntSort())
#solve(f(f(x)) == x, f(x) == y, x != y)


#x = Int('x')
#y = Int('y')
#f = Function('f', IntSort(), IntSort())
#s = Solver()
#s.add(f(f(x)) == x, f(x) == y, x != y)
#print(s.check())
#m = s.model()
#print("f(f(x)) =", m.evaluate(f(f(x))))
#print("f(x)    =", m.evaluate(f(x)))

# 证明题求解方法
#p, q = Bools('p q')
#demorgan = And(p, q) == Not(Or(Not(p), Not(q)))
#print(demorgan)

#def prove(f):
#    s = Solver()
#    s.add(Not(f))
#    if s.check() == unsat:
#        print("proved")
#    else:
#        print("failed to prove")

#print("Proving demorgan...")
#prove(demorgan)



# list
# Create list [1, ..., 5]
#print([ x + 1 for x in range(5) ])

# Create two lists containing 5 integer variables
#X = [ Int('x%s' % i) for i in range(5) ]
#Y = [ Int('y%s' % i) for i in range(5) ]
#print(X)

# Create a list containing X[i]+Y[i]
#X_plus_Y = [ X[i] + Y[i] for i in range(5) ]
#print(X_plus_Y)

# Create a list containing X[i] > Y[i]
#X_gt_Y = [ X[i] > Y[i] for i in range(5) ]
#print(X_gt_Y)

#print(And(X_gt_Y))

# Create a 3x3 "matrix" (list of lists) of integer variables
#X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(3) ]for i in range(3) ]
#pp(X)


#X = IntVector('x', 5)      # 结果同上述创建list
#Y = RealVector('y', 5)
#P = BoolVector('p', 5)
#print(X)
#print(Y)
#print(P)
#print([ y**2 for y in Y ])
#print(Sum([ y**2 for y in Y ]))



X = [ Int('x%s' %i) for i in range(5) ]
def one_in():
    cnt = 0
    for i in range(5):
        if X[i] == 1:
           cnt += 1
    return cnt

s = Solver()
s.add(sum(X[i] for i in range(5))==3)
for i in range(5):
    s.add(X[i]<2)

print(s.check())
print(s.model())



