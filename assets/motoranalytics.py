from motor import Motor
import numpy as np

bounds = [
(0.06, 0.1),
(0.125, 0.31),
(0.125, 0.31),
(0, 3),
(0.005, 0.02),
(0.005, 0.02),
(0.01,0.1),
]
def randomVal(range):
    return round(np.random.uniform(low=range[0],high=range[1]), 4)
def evalFitnessFromValList(x):
    throat_dia = x[0]
    exit_dia = x[1]
    motor_width = x[2]
    fin_width = x[3]
    fin_len = x[4]
    inner_width = x[5]
    propCollection = {
        'config': {
            'maxPressure': 1500 * 6895,
            'maxMassFlux': 2 / 0.001422,
            'minPortThroat': 2,
            'burnoutWebThres': 0.01 / 39.37,
            'burnoutThrustThres': 0.1,
            'timestep': 0.1,
            'ambPressure': 101325,
            'igniterPressure': 150 * 6895,
            'mapDim': 750
        },
        'nozzle': {
            'throat': throat_dia,
            'exit': exit_dia,
            'efficiency': 1,
            'divAngle': 15,
            'convAngle': 30,
            'throatLength': 0,
            'slagCoeff': 0,
            'erosionCoeff': 0,
        },
        'propellant': {
                'name': 'MIT - Cherry Limeade',
                'density': 1680,
                'tabs': [
                    {
                        'minPressure': 0,
                        'maxPressure': 6.895e+06,
                        'a': 3.517054143255937e-05,
                        'n': 0.3273,
                        't': 3500,
                        'm': 23.67,
                        'k': 1.21
                    }
                ]
        },
        'grains': [
            {
                'type': "Finocyl",
                'properties': {
                    'diameter': motor_width,
                    'length': 3,
                    'numFins': 6,
                    'finWidth': fin_width,
                    'finLength': fin_len,
                    'coreDiameter': inner_width
                }
            },
            {
                'type': "Finocyl",
                'properties': {
                    'diameter': motor_width,
                    'length': motor_length,
                    'numFins': 6,
                    'finWidth': fin_width,
                    'finLength': fin_len,
                    'coreDiameter': inner_width
                }
            }
        ]
    }
    return fitness(Motor(propCollection).runSimulation())
def createRandomMotorInstance():
    motor_width = randomVal(ranges['OUTER_DIAMTER_RANGE'])
    inner_width = randomVal(ranges['CORE_DIAMETER'])
    fin_len = randomVal(ranges['FIN_LENGTH'])
    fin_width = randomVal(ranges['FIN_WIDTH'])
    throat_dia = randomVal(ranges['THROAT_DIAMETER'])
    exit_dia = randomVal(ranges['EXIT_DIAMTER'])
    while throat_dia > exit_dia:
        throat_dia = randomVal(ranges['THROAT_DIAMETER'])
        exit_dia = randomVal(ranges['EXIT_DIAMTER'])
    while motor_width < inner_width:
        motor_width = randomVal(ranges['OUTER_DIAMTER_RANGE'])
        inner_width = randomVal(ranges['CORE_DIAMETER'])
    print("motor_width",motor_width)
    print("inner_width",inner_width)
    print("fin_len",fin_len)
    print("fin_width",fin_width)
    print("throat_dia",throat_dia)
    print("exit_dia",exit_dia)
    propCollection = {
        'config': {
            'maxPressure': 1500 * 6895,
            'maxMassFlux': 2 / 0.001422,
            'minPortThroat': 2,
            'burnoutWebThres': 0.01 / 39.37,
            'burnoutThrustThres': 0.1,
            'timestep': 0.1,
            'ambPressure': 101325,
            'igniterPressure': 150 * 6895,
            'mapDim': 750
        },
        'nozzle': {
            'throat': throat_dia,
            'exit': exit_dia,
            'efficiency': 1,
            'divAngle': 15,
            'convAngle': 30,
            'throatLength': 0,
            'slagCoeff': 0,
            'erosionCoeff': 0,
        },
        'propellant': {
                'name': 'MIT - Cherry Limeade',
                'density': 1680,
                'tabs': [
                    {
                        'minPressure': 0,
                        'maxPressure': 6.895e+06,
                        'a': 3.517054143255937e-05,
                        'n': 0.3273,
                        't': 3500,
                        'm': 23.67,
                        'k': 1.21
                    }
                ]
        },
        'grains': [
            {
                'type': "Finocyl",
                'properties': {
                    'diameter': motor_width,
                    'length': 3,
                    'numFins': 6,
                    'finWidth': fin_width,
                    'finLength': fin_len,
                    'coreDiameter': inner_width
                }
            },
            {
                'type': "Finocyl",
                'properties': {
                    'diameter': motor_width,
                    'length': randomVal(ranges['MOTOR_LENGTH_RANGE']),
                    'numFins': 6,
                    'finWidth': fin_width,
                    'finLength': fin_len,
                    'coreDiameter': inner_width
                }
            }
        ]
    }
    return Motor(propCollection)
#A perfectly fit motor will have a value of 0
def fitness(simRes):
    val = 0
    val += abs(simRes.getPeakKN() - 230)
    val += abs(simRes.getPortRatio() - 2.5)*100
    val += abs(simRes.getImpulse() - 250000)/1000