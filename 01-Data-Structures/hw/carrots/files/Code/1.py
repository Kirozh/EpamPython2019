print(True is not False)
print(True != False)
b = {'p', 'e', 'a', 'm'}
a = set()
a.add('e')
a.add('p')
a.add('a')
a.add('m')
print(a)
print(b)

print(1) if 100 % 2 == 0 else print(11)
i = 0
while i > 1:
    i = i+1
else:
    print('Loop error')
s = 'Unicode string'
s1 = s.encode("UTF-8")
print(type(s1))
s2 = s1.decode("UTF-8")
print(type(s2))
print(s2)

problem = "bbb"
#print(problem.split('\t'))
new_problem = "next problem! - новая проблема"
print(problem.join(new_problem))
print(new_problem.index('r'))
print(new_problem.center(40, '$'))
print(new_problem.partition(' pr'))
print(new_problem.count('e'))
print(repr(new_problem))
print('My name is {1} \nmy surname is {0}'.format('Vasya', 'Pupkin'))

list_example_1 = []
list_example_1.extend((1, 2, 3, 4, 5))
print(list_example_1)
list_example_1[:3] = [0] * 3
print(list(reversed(list_example_1)))

tuple_ = 1, 2
list_ = ['apple', 'banana', 'carrot', 'daemond']
for c, values in enumerate(list_, 0):
    print(c, values)
print(tuple_.__sizeof__())
print(list_.__sizeof__())

set_ = set('an ice cream')
set_.add(1)
print(set_)
print(type(set_))

dict_ = {}

dict_ = dict([('Ivanov', 22), ("Petrov", 18)])
print(dict_)
print('hallo')