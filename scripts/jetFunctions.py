import spidev
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np

directionPin = 27
enablePin = 22
stepPin = 17

spi = spidev.SpiDev()

def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print ("SPI for ADC has been initialized")


def deinitSpiAdc():
    spi.close()
    print ("SPI cleanup finished")


def getAdc():
    adcResponse = spi.xfer2([0, 0])
    adc = ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

    return adc


def getMeanAdc(samples):
    sum = 0
    for i in range(samples):
        sum += getAdc()
    
    return int(sum / samples)


def initStepMotorGpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([directionPin, enablePin, stepPin], GPIO.OUT)
    print ("GPIO for step motor have been initialized")


def deinitStepMotorGpio():
    GPIO.output([directionPin, enablePin, stepPin], 0)
    GPIO.cleanup()
    print ("GPIO cleanup finished")


def step():
    GPIO.output(stepPin, 0)
    time.sleep(0.005)
    GPIO.output(stepPin, 1)
    time.sleep(0.005)
    

def stepForward(n):
    GPIO.output(directionPin, 1)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


def stepBackward(n):
    GPIO.output(directionPin, 0)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


def saveMeasures(measures, samplesInMeasure, motorSteps, count):
    filename = 'jet-data {}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    with open(filename, "w") as outfile:
        outfile.write('- Jet Lab\n\n')
        outfile.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Number of samples in measure = {}\n'.format(samplesInMeasure))
        outfile.write('- Number of motor steps between measures = {}\n'.format(motorSteps))
        outfile.write('- Measures count = {}\n\n'.format(count))
        
        outfile.write('- adc12bit\n')
        np.savetxt(outfile, np.array(measures).T, fmt='%d')


def showMeasures(measures, samplesInMeasure, motorSteps, count):
    print('\nExperiment date = {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    print('Number of samples in measure = {}'.format(samplesInMeasure))
    print('Number of motor steps between measures = {}'.format(motorSteps))
    print('Measures count = {}\n'.format(count))
    
    plt.plot(measures)
    plt.show()


def readJetData(filename):
    with open(filename) as f:
        lines = f.readlines()

    steps = 0
    count = 0
    dataLineIndex = 0

    for index, line in enumerate(lines):
        if line[0] != '-' and line[0] != '\n':
            dataLineIndex = index
            break

        if 'steps' in line:
            words = line.split()
            for word in words:
                try:
                    steps = float(word)
                except ValueError:
                    pass

        if 'count' in line:
            words = line.split()
            for word in words:
                try:
                    count = int(word)
                except ValueError:
                    pass

    dataLines = lines[dataLineIndex:]
    data = np.asarray(dataLines, dtype=int)

    return data, steps, count

def Adc_Sred(filename):
    m=[]
    f = open(filename,"r")
    for i in f:
        m.append(int(i))
    return sum(m)/len(m)

def calibration(sr_1,sr_2,pressure_1,pressure_2):
    
    plt.axis([700, 1100, 0, 60])
    ax = plt.gca()
    ys = [pressure_1,pressure_2]
    xs = [sr_1,sr_2]
    trend = np.polyfit(xs, ys, 1)
    plt.plot(xs, ys, 'o')
    trendpoly = np.poly1d(trend)
    plt.plot(xs, trendpoly(xs), label=f"$P={trend[0]:0.3f}\;N{trend[1]:+0.2f}$")
    print(trendpoly(xs))
    print(trend)
    ax.set_facecolor('white')
    plt.xlabel('Отсчёты АЦП', fontsize=15)
    plt.ylabel('Давление [Па]', fontsize=15)
    plt.title('Калибровочный график зависимости показаний АЦП от давления', fontsize=15, fontweight='bold')
    ax.minorticks_on()
    plt.grid(which="both", linewidth=1)
    plt.grid(which="minor", ls="--", linewidth=0.25)
    plt.legend(fontsize=13)
    plt.savefig('pressure-calibration.png')
    plt.show()

    return trend
def calibration_move():
    fig = plt.figure(figsize=(10, 5), dpi=200)
    y1 =[0, 0.006]
    x1=[0, 100]
    plt.plot(x1, y1, 'o')
    plt.title('Калибровочный график зависимости перемещения трубки Пито от шага двигателя', fontsize=15, fontweight='bold')
    plt.ylabel('Перемещение трубки Пито [см]', fontsize=15)
    plt.xlabel('Количество шагов', fontsize=15)
    print(np.polyfit(x1, y1, 1)) # нахождение полиномиальной зависимости со степенью подгонки 1
    grafic = plt.plot(x1, y1 , label = 'y=5,2e-05*step[M]')
    plt.minorticks_on()
    plt.legend()
    plt.grid(which="both", linewidth=1)
    plt.grid(which="minor", ls="--", linewidth=0.25)
    plt.savefig('move-calibration.png')
    plt.show()


def plot_speed(Data1,Data2,Data3,Data4,Data5,Data6):
    y1 = np.array(Data1[0])
    y2 = np.array(Data2[0])
    y3 = np.array(Data3[0])
    y4 = np.array(Data4[0])
    y5 = np.array(Data5[0])
    y6 = np.array(Data6[0])

    y1 = np.array(Data1[0])
    p1 = 0.4083 * y1 - 334.7791
    u1=np.sqrt((2 * p1) / 1.2)
    x1 = np.linspace(0, ((5.2 / 100)), 120) # массив из последовательности точе(start,stop, quaniti)
    x1max = np.argmax(u1)                    # нахождение индекса максимального элемента массива(Вершина)
    delta1 = x1[x1max]                       # Центровка
    x1=x1 - delta1

    q1 = 1.2 * 2 * np.pi * 0.000052 * 4 * 1000 * u1 * x1
    q1 = np.sum(np.abs(q1)) / 2
    print(q1, end = '\n ')

    y2 = np.array(Data2[0])
    p2 = 0.4083 * y2 - 334.7791
    u2= np.sqrt((2 * p2) / 1.2)
    x2 = np.linspace(0, ((5.2 / 100)), 120)
    x2max = np.argmax(u2)
    delta2 = x2[x2max]
    x2 = x2 - delta2

    q2 = 1.2 * 2 * np.pi * 0.000052 * 4 * 1000 * u2 * x2
    q2 = np.sum(np.abs(q2)) / 2
    print(q2, end= '\n ')

    y3 = np.array(Data3[0])
    p3 = 0.4083 * y3 - 334.7791
    u3= np.sqrt((2 * p3) / 1.2)
    x3 = np.linspace(0, ((5.2 / 100)), 120)
    x3max=np.argmax(u3)
    delta3=x3[x3max]
    x3 = x3 - delta3

    q3=1.2 * 2 * np.pi * 0.000052 * 4 * 1000 * u3 * x3
    q3=np.sum(np.abs(q3)) / 2
    print(q3, end = '\n ')

    y4 = np.array(Data4[0])
    p4 = 0.4083 * y4 - 334.7791
    u4= np.sqrt((2 * p4) / 1.2)
    x4 = np.linspace(0, ((5.2 / 100)), 120)
    x4max = np.argmax(u4)
    delta4 = x4[x4max]
    x4 = x4 - delta4

    q4 = 1.2 * 2 * np.pi * 0.000052 * 4 * 1000 * u4 * x4
    q4 = np.sum(np.abs(q4)) / 2
    print(q4, end = '\n ')

    y5 = np.array(Data5[0])
    p5 = 0.4083 * y5 - 334.7791
    u5= np.sqrt((2 * p5) / 1.2)
    x5 = np.linspace(0, (5.2 / 100), 120)
    x5max = np.argmax(u5)
    delta5 = x5[x5max]
    x5 = x5 - delta5

    q5 = 1.2 * 2 * np.pi * 0.000052 * 4 * 1000 * u5 * x5
    q5 = np.sum(np.abs(q5)) / 2
    print(q5, end = '\n ')

    y6 = np.array(Data6[0])
    p6 = 0.4083 * y6 - 334.7791
    u6= np.sqrt((2 * p6) / 1.2)
    x6 = np.linspace(0, (5.2 / 100), 120)
    x6max = np.argmax(u6)
    delta6 = x6[x6max]
    x6 = x6 - delta6

    q6 = 1.2 * 2 * np.pi * 0.000052 * 4 * 1000 * u6 * x6
    q6 = np.sum(np.abs(q6)) / 2
    print(q6, end = '\n ')

    ###################################################################
    plt.figure(figsize=(10, 10))
    plt.title('Скорость потока воздуха в сечении затопленной струи')
    plt.xlabel('Положение трубки Пито относительно центра струи [мм]')
    plt.ylabel('Скорость воздуха [м/с]')

    plt.plot(x1, u1, color = 'g', label = 'Q1 (10 mm) = 4.04 [г/с]')
    plt.plot(x2, u2, color = 'r', label = 'Q2 (20 mm) = 4.51 [г/с]')
    plt.plot(x3, u3, color = 'c', label = 'Q3 (30 mm) = 5.01 [г/с]')
    plt.plot(x4, u4, color = 'y', label = 'Q4 (40 mm) = 5.29 [г/с]')
    plt.plot(x5, u5, color = 'm', label = 'Q5 (50 mm) = 5.65 [г/с]')
    plt.plot(x6, u6, color = 'k', label = 'Q6 (60 mm) = 6.04 [г/с]')

    plt.legend()
    plt.minorticks_on()
    plt.grid(which = 'major')
    plt.grid(which = 'minor', linestyle = '--')
    plt.savefig("Speeds")

    plt.show()
