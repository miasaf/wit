import graphviz

dot = graphviz.Digraph(comment='Commits Graph')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')
dot.edges(['AB', 'BL'])
#dot.edge('B', 'L', constraint='false')


#src = graphviz.Source('Commits graph { rankdir=LR; A -> B -> L }')
#src.render('C:\\Users\\miasa\\Desktop\\קורס פייתון\\week10\\wit\\.wit\\Commits Graph.gv', view=True)
#dot.render('C:\\Users\\miasa\\Desktop\\קורס פייתון\\week10\\wit\\.wit\\Commits Graph.gv', view=True) 


print(dot[0])

for i in range(2):
    print(i)