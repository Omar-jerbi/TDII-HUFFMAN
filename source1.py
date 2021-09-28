import random


DIMINPUT = 100


def tochar(x):
	if(x == 26):
		return ' '
	else:
		return(chr(97+x)) 


#riempe array da 0 a 26 con rispettive freq:: 0=a 25=z 26=' '
def freqs(x, array):
	array[x]+=1


def logList(lista):
	for couple in lista:
		print("%s , %s ||" %(couple.car, couple.num), end='') #""" +1  per visualizzare freq empirica corretta """
	print()



##########################################################################################
arrayfreq = [0]*27  ##############   non ho la minima idea del perchè con -1 OK, con 0 KO    ####################
file_caratteri = 'fileext.txt'

f = open(file_caratteri, 'w+')

for i in range(DIMINPUT): #riempo fileext
	x = random.randint(0,26)
	carac = tochar(x)
	freqs(x, arrayfreq) #array con le frequenze_empiriche di ogni char
	f.write(carac)

f.close()

#############################################################################


class Node:
	def __init__(self, car, num):
		self.car = car
		self.num = num
		self.r = None
		self.l = None
		self.cod = ""

	def display(self):
		lines, *_ = self._display_aux()
		for line in lines:
			print(line)

	def _display_aux(self):
	#foglia
		if self.r == None and self.l == None:
			line = self.car
			width = len(line)
			height = 1
			middle = width // 2
			return [line], width, height, middle

	# Only l child.
		if self.r is None:
			lines, n, p, x = self.l._display_aux()
			s = '%s' % self.car
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

	# Only r child.
		if self.l is None:
			lines, n, p, x = self.r._display_aux()
			s = '%s' % self.car
			u = len(s)
			first_line = s + x * '_' + (n - x) * ' '
			second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
			shifted_lines = [u * ' ' + line for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

	# Two children.
		l, n, p, x = self.l._display_aux()
		r, m, q, y = self.r._display_aux()
		s = '%s' % self.car
		u = len(s)
		first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
		second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
		if p < q:
			l += [n * ' '] * (q - p)
		elif q < p:
			r += [m * ' '] * (p - q)
		zipped_lines = zip(l, r)
		lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
		return lines, n + m + u, max(p, q) + 2, n + u // 2




###########################################################################################
listN = [] #lista Node
for i in range(27):
	if i != 26:
		listN.append( Node(chr(i+97), arrayfreq[i]) )
	else:
		listN.append( Node(' ', arrayfreq[26]) )

listN.sort(key=lambda x: x.num, reverse=True)

################################################################################


"""listN = [
	Node('g', 70),
	Node('r', 65),
	Node('v', 48),
	Node('a', 32),
	Node('f', 31),
	Node('i', 20),
	Node('e', 11),
	Node('h', 4),
	Node('w', 1),
]
"""

logList(listN)
print()

listNN = []

while True:
	try:
		root = listN.pop()

		n2 = listN.pop()

		n = Node("$", root.num + n2.num)

		if root.num <= n2.num:
			n.r = root
			n.l = n2
		else:
			n.r = n2
			n.l = root

		tup = (n , root, n2) #padre #fDX #fSX

		listNN.append(tup)

		listN.append(n)
		listN.sort(key=lambda x: x.num, reverse=True)

	except IndexError:
		root.display()
		break


"""for x in listNN:
	print(x[0].car)
	print(x[1].car)
	print(x[2].car)
	print()
"""

def findCar(l, c):
	i = 0
	for x in l:
		if x[1].car == c or x[2].car == c:
			return i
		else:
			i += 1


def findTPadreDiRoot(l, n):
	i = 0
	for x in l:
		if x[1] == n or x[2] == n:
			return i
		else:
			i += 1	



def cod(list, c):
	res = ""
	posc = findCar(listNN, c) #pos della tupla

	tuplaOrg = list[posc]

	if tuplaOrg[0].r.car == c:
		res =res + '0'
	else:
		res = res + '1'

	while 1:
		posx = findTPadreDiRoot(list, tuplaOrg[0]) #pos della tupla padre della tuplaOrg
		x = list[posx]

		if x[1] == tuplaOrg[0]:
			res = res + '0'
		else:
			res = res + '1'
		
		tuplaOrg = x

		if x == list[len(list)-1]: break

	return res[::-1]
	


#####################################################################
print(cod(listNN, 'f'))
