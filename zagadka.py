# Biblioteki
import random

# pewne założenia początkowe
 
t = 10
Ta = 2.7 * t
Tb = 3.9 * t
Tc = 4.8 * t

TotalTime = 2*8*60 

# Pula czasów testów
Testy = [Ta, Tb, Tc]

# Stanowiska
class Stanowisko:
	"""objek Stanowisko"""
	def __init__(self, Testy=Testy):
		self.free = True
		self.output = 0
		self.Testy = Testy
		self.testType = []

	def Test(self, t):
		if self.free:
			self.free = False
			self.testStart = t
			randTest = random.randint(1, 3)
			self.testType.append(randTest)
			self.testTime = Testy[randTest-1]
			self.testEnd = self.testStart + self.testTime



			return True
		else:
			return False

	def update(self, t):
		if not self.free:
			if t >= self.testEnd:
				self.free = True
				self.output += 1
				self.testEnd = 0
				self.testStart = 0

# stanowiska testowe
S1 = Stanowisko()
S2 = Stanowisko()
S3 = Stanowisko()

# Pole odkładcze
PO = 0 

# liczba wyłączników
Breakers = 0

# czas
dni = 0
time = 0

dniAnalizy = 10000

for x in range(dniAnalizy):

	while (time < TotalTime*dniAnalizy):
		time += t
		Breakers +=1

		S1.update(time)
		S2.update(time)
		S3.update(time)

		if not S1.Test(time):
			if not S2.Test(time):
				if not S3.Test(time):
					PO += 1
	
	dni += 1


print('Report, dni: {}'.format(dni))
print('Total breakers: {}'.format(Breakers))
print('S1 breakers: {}'.format(S1.output))
print('S2 breakers: {}'.format(S2.output))
print('S3 breakers: {}'.format(S3.output))
print('Pole odkładcze breakers: {}'.format(PO))
print('Suma kontrolna: {}'.format(PO+S1.output+S2.output+S3.output))
print('tester 1 pusty: {}'.format(S1.free))
print('tester 2 pusty: {}'.format(S2.free))
print('tester 3 pusty: {}'.format(S3.free))

print('Procent ACB na polu odkładczym: {}%'.format(100*PO/Breakers))