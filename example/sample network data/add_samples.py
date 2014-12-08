from rolodex.models import Person

edge_docs = ['0.edges',]#'107.edges','348.edges','414.edges','686.edges']
base= '/home/jon/DMN/Scripts/django-rolodex/example/sample network data/facebook/'
relationships =[]

for doc in edge_docs:
    
    with open(base+doc,'r+') as file:
	print doc
        for line in file:
            ents=line.split()
            print type(ents[0])
            ent1, get = Person.objects.get_or_create(firstName='node',lastName=ents[0])
            ent2, get = Person.objects.get_or_create(firstName='node',lastName=ents[1])
            if 'n'+ents[0]+'-n'+ents[1] not in relationships:
                print "added "+ents[0]+">>"+ents[1]
                ent1.add_p2p(ent2)            
                relationships.append('n'+ents[0]+'-n'+ents[1])
                relationships.append('n'+ents[1]+'-n'+ents[0])
