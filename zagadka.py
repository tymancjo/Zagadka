# Biblioteki
import random
import matplotlib.pyplot as plt
import numpy as np

# pewne założenia początkowe
 
t = 10
Ta = 2.7 * t
Tb = 3.9 * t
Tc = 4.8 * t

SingleShiftTime = 8*60 

# Pula czasów testów
Testy = [Ta, Tb, Tc]
timetable = [[0,0,0,0,0]]

# Stanowiska
class Stanowisko:
	"""objek Stanowisko"""
	def __init__(self, Testy=Testy):
		self.free = True
		self.output = 0
		self.Testy = Testy
		self.testType = [0,0,0]

	def Test(self, t):
		if self.free:
			randTest = random.randint(1, 3)
			self.testTime = Testy[randTest-1]
			
			if t + self.testTime <= SingleShiftTime:
				self.free = False
				self.testStart = t
				self.testEnd = self.testStart + self.testTime
				self.testType[randTest-1] += 1
				return True
			else:
				self.testEnd = 0
				self.testStart = 0
				return False

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
POd =[0] 
ACBd =[0] 


# liczba wyłączników
Breakers = 0

# czas
dni = 0

iloscZmian = 1000

for x in range(iloscZmian):
	time = 0
	while (time < SingleShiftTime):
		time += t
		Breakers +=1
		# S1 S2 S3 PO
		timetableRow=[0,0,0,0,0]

		S1.update(time)
		S2.update(time)
		S3.update(time)

		if not S1.Test(time):
			if not S2.Test(time):
				if not S3.Test(time):
					PO += 1
					timetableRow[3] = 1
				else:
					timetableRow[2] = 1
			else:
				timetableRow[1] = 1
		else:
			timetableRow[0] = 1

		timetableRow[4] = abs(timetable[-1][4] - 1)	
			
		timetable.append(timetableRow)

	dni += 1

	POd.append(PO - sum(POd))
	ACBd.append(Breakers - sum(ACBd))

POd.remove(0)
ACBd.remove(0)
ax = [x for x in range(iloscZmian)]

POd = np.array(POd)
ACBd = np.array(ACBd)
ax = np.array(ax) + 1

timetable = np.array(timetable)
timetable_x = np.linspace(1,timetable.shape[0], timetable.shape[0])


# plt.subplot(211)
plt.bar(ax,ACBd / (SingleShiftTime/t), color='lightgray', width=0.8)
plt.bar(ax,POd /  (SingleShiftTime/t),color='r', width=0.4)
plt.plot(ax, np.ones(len(ax))*PO/Breakers, 'r--')
# plt.plot(ax, , 'r--')

text = 'Average: {}'.format(PO/Breakers)

plt.text(3, PO/Breakers - 0.1, text, style='italic', color='white', 
	bbox={'facecolor':'black', 'alpha':0.9, 'pad':3} )
plt.title('Ilość Wyprodukowana / Ilośc odłożona - znormalizowane')
plt.ylabel('Wyprodukowane / Pole odkładcze')
plt.xlabel('numer zmiany produkcyjnej')

# plt.subplot(212)
# plt.bar(ax,ACBd)
# plt.ylabel('Wyprodukowanych')
# plt.xlabel('numer zmiany produkcyjnej')

plt.show()

if timetable_x.shape[0] < 200:
	plt.step(timetable_x,timetable[:,0], label='S1')
	plt.step(timetable_x,timetable[:,1]+1.5, label='S2')
	plt.step(timetable_x,timetable[:,2]+3, label='S3')
	plt.step(timetable_x,timetable[:,3]+4.5, label='PO')
	plt.step(timetable_x,timetable[:,4]+6, label='takt')

	plt.xticks(timetable_x, rotation='vertical', fontsize=1000/timetable_x.shape[0])
	plt.grid(axis='x', color='black', linestyle='-', linewidth=1, alpha=0.3)
	plt.legend()
	plt.show()


print('Report, dni: {}, zmian: {}'.format(dni / 2, dni))
print('Wyprodukowanych wyłączników: {}'.format(Breakers))
print('Testów w stacji 1: {}'.format(S1.output))
print('Testów w stacji 2: {}'.format(S2.output))
print('Testów w stacji 3: {}'.format(S3.output))
print('Aparatów na polu odkładczym: {}'.format(PO))
print('Suma kontrolna: {}'.format(PO+S1.output+S2.output+S3.output))
print('Sprawdzenie czy w testerach nie zostały aparaty')
print('tester 1 pusty: {}'.format(S1.free))
print('tester 2 pusty: {}'.format(S2.free))
print('tester 3 pusty: {}'.format(S3.free))

print('Procent aparatów z {} zmian na polu odkładczym: {}%'.format(round(dni / 2), 100*PO/Breakers))

print('Podział testów w stacji 1: A:{:.2f}% B:{:.2f}% C:{:.2f}%'.format(100*S1.testType[0] / S1.output, 100*S1.testType[1] / S1.output, 100*S1.testType[2] / S1.output))
print('Podział testów w stacji 2: A:{:.2f}% B:{:.2f}% C:{:.2f}%'.format(100*S2.testType[0] / S2.output, 100*S2.testType[1] / S2.output, 100*S2.testType[2] / S2.output))
print('Podział testów w stacji 3: A:{:.2f}% B:{:.2f}% C:{:.2f}%'.format(100*S3.testType[0] / S3.output, 100*S3.testType[1] / S3.output, 100*S3.testType[2] / S3.output))

