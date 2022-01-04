from math import log2
from os import read
import random


DIMINPUT = 10000 #dimensione file di input


#array con le frequenze empiriche delle lettere nella lingua italiana(semplificato), fonte: Wikipedia
#per 1050 lettere
arraylettere = ['a']*110 + [' ']*80 + ['b']*9 +['c']*45+['d']*37+['e']*108+['f']*9+['g']*16+['h']*15+['i']*103+['l']*65+['m']*25+['n']*68+['o']*88+['p']*30+['q']*5+['r']*63+['s']*56+['t']*55+['u']*30+['v']*21+['z']*5+['w']*1+['x']*1+['y']*1+['j']*2+['k']*2





#riempe array da 0 a 26 con rispettive freq:: 0=a 1=b ... 25=z 26=' '
def freqs(x, array):
	array[x]+=1


def logList(lista):
	for couple in lista:
		print("%s , %s ||" %(couple.car, couple.num), end='')
	print()


def toInt(x):
	if(x == ' '):
		return 26
	else:
		return ord(x)-97

##########################################################################################
arrayfreq = [0]*27 
file_caratteri = 'filechar.txt'

f = open(file_caratteri, 'w+')

for i in range(DIMINPUT): #riempo fileext
	x = random.randint(0,1049)
	carac = arraylettere[x];
	freqs(toInt(carac), arrayfreq) #array con le frequenze empiriche di ogni char
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

	# Only L child.
		if self.r is None:
			lines, n, p, x = self.l._display_aux()
			s = '%s' % self.car
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

	# Only R child.
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
listN = [] #lista Nodi
for i in range(27):
	if i != 26:
		listN.append( Node(chr(i+97), arrayfreq[i]) )
	else:
		listN.append( Node(' ', arrayfreq[26]) )

listN.sort(key=lambda x: x.num, reverse=True)


#########################DISPLAY ALBERO#########################################################################################
logList(listN)
print()

listNN = [] #lista nodi Nuova, ogni elemente è una tripla: (nodo_padre, figlio_destro, figlio_sinistro)
			# serve come input per la successiva codifica

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
#########################DISPLAY ALBERO#########################################################################################


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
	

# print(cod(listNN, 'a'))
# print(cod(listNN, 'b'))

#####################################################################
###########################CREAZIONE DEL FILE CODIFICATO##########################################
file_in = open("filechar.txt", 'r');
file_cod = open("filecodificato.txt", 'w+');

for line in file_in:
	for c in line:
		file_cod.write(cod(listNN, c));


#####################################################################
#####################################################################


######################CALCOLO DELL'ENTROPIA E DELLA LUNGHEZZA ATTESA################################
def H(arr):
	s = 0
	for i in range(0, 26):
		s = s + (arr[i]/DIMINPUT)*log2(DIMINPUT/arr[i])
	return s

def L(arr):
	s = 0;
	for i in range(0, 26):
		if(i == 26):
			carattere_i = " "
		else:
			carattere_i = chr(i+97)
		
		s = s + (arr[i]/DIMINPUT)*len(cod(listNN, carattere_i))
	return s

# H ≈ L, la codifica di huffman èsenza ridondanza, non si può migliorare ulteriormente
print("H =", H(arrayfreq))
print("L =", L(arrayfreq))