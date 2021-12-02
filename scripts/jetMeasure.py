import jetFunctions as jet
calibration_move = 166
try:
    jet.initStepMotorGpio()
    jet.initSpiAdc()
    measure = []
    for j in range(100):
        measure.append(jet.getMeanAdc(100))
        jet.stepBackward(9)
        
    jet.showMeasures(measure, 100, 9, len(measure))
    jet.saveMeasures(measure, 100, 9, len(measure))
finally:
    jet.deinitSpiAdc()
    jet.deinitStepMotorGpio()

