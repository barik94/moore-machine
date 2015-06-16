from dyplom import MooreMachine
from random import randint
from collections import OrderedDict
from _dbus_bindings import Double

globalCount = 0
trajectoriesDictionary = {}
while globalCount < 1000 :
    inputWord = "";
    counter = 0
    machine = MooreMachine()
    while counter < 6 :
        if randint(1, 2) % 2 :
            inputWord += machine.inputSymbols[0]
        else :
            inputWord += machine.inputSymbols[1]
        counter += 1
    
#     print inputWord
    trajectory = machine.run(machine.readXML(), inputWord)
    if trajectory in trajectoriesDictionary :
        trajectoriesDictionary[trajectory] = trajectoriesDictionary[trajectory] + 1
    else :
        trajectoriesDictionary[trajectory] = 1
    globalCount += 1
    
trajectoriesDictionary = OrderedDict(reversed(sorted(trajectoriesDictionary.items(), key=lambda t: t[1])))
print 'Total -', len(trajectoriesDictionary), 'unique trajectories.'
print 'Most popular was:', trajectoriesDictionary.iterkeys().next()
for key, value in trajectoriesDictionary.items() :
    probability = Double(value) / 1000
    print key + ': ' + `value`, 'probability:', `probability * 100` + '%'
