from array import array
from xml.dom import minidom
from collections import OrderedDict
from random import randint
import random

class MooreMachine(object): 
    inputSymbols = ['a', 'b']
    firstState = 's1'
    def MooreMachine(self, inputSymbols = None):
        if inputSymbols :
            self.inputSymbols = inputSymbols
        else :
            self.inputSymbols = ['a', 'b']
    
    def setFirstState(self, state):
        self.firstState = state
    
    def readXML(self):
        try : 
            xmldoc = minidom.parse('/var/www/dyplom/moor_automat1.xml')
        except Exception :
            print 'Wrong path or file no exists!!!\nMaybe XML-file was bad structured.'
            return False

        statesList = xmldoc.getElementsByTagName('state') 
        self.setFirstState(random.choice(statesList).attributes['val'].value)
        
        table = {}
        for state in statesList :
            table[state.attributes['val'].value] = {}
        
            probabilitiesA = state.getElementsByTagName('a')
            probabilitiesB = state.getElementsByTagName('b')
            
            sumProbB = sumProbA = 0
            for index, p in enumerate(probabilitiesA) :
                try :
                    sumProbA += int(p.attributes['p'].value)
                except ValueError:
                    print 'Unexpected value for probability in state', state.attributes['val'].value, '!!!\nCheck your XML-file.'
                    return False
              
                table[state.attributes['val'].value]['a' + `index` + '/' + p.attributes['p'].value] = p.firstChild.data
            if sumProbA != 100 :
                print 'Sum of probabilities not equals 100% in state', state.attributes['val'].value, '!!!\nCheck your XML-file.'
                return False
              
            for index, p in enumerate(probabilitiesB) :
                try :
                    sumProbB += int(p.attributes['p'].value)
                except ValueError:
                    print 'Unexpected value for probability in state', state.attributes['val'].value, '!!!\nCheck your XML-file.'
                    return False
              
                table[state.attributes['val'].value]['b' + `index` + '/' + p.attributes['p'].value] = p.firstChild.data
            if sumProbB != 100 :
                print 'Sum of probabilities not equals 100% in state', state.attributes['val'].value, '!!!\nCheck your XML-file.'
                return False
      
        table = OrderedDict(sorted(table.items(), key=lambda t: t[0]))

        return table

    def run(self, table, inputWord):
        counter = 0
        trajectory = curState = self.firstState
        if table :
            while counter < len(inputWord) :
                choices = table[curState]
                prob = randint(1, 100)
                up = 0
                for key, value in choices.iteritems() :
                    if key[0] == inputWord[counter] :
                        down = up
                        up += int(key[key.find('/') + 1 :])
                        if up == 100 :
                            curState = value
                            break
                        if prob > down and prob < up :
                            curState = value
                            break
                      
#                 print curState
                trajectory += curState
    
                counter += 1
            return trajectory
