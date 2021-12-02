import jetFunctions as jet
import numpy as np
sred1 = jet.Adc_Sred("/home/gr109/Desktop/kazbek/calibr0.txt")
sred2 = jet.Adc_Sred("/home/gr109/Desktop/kazbek/calibr1.txt")
pressure1 = 0
pressure2 = 59
jet.calibration(sred1, sred2, pressure1, pressure2)
jet.calibration_move()
Data1 = jet.readJetData('10mm.txt')
Data2 = jet.readJetData('20mm.txt')
Data3 = jet.readJetData('30mm.txt')
Data4 = jet.readJetData('40mm.txt')
Data5 = jet.readJetData('50mm.txt')
Data6 = jet.readJetData('60mm.txt')
jet.plot_speed(Data1,Data2,Data3,Data4,Data5,Data6)