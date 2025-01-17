import math

from scipy.optimize import fsolve

from properties import FloatProperty, PropertyCollection
import geometry
from simResult import SimAlert, SimAlertLevel, SimAlertType


def eRatioFromPRatio(k, pRatio):
    """Returns the expansion ratio of a nozzle given the pressure ratio it causes."""
    return (((k+1)/2)**(1/(k-1))) * (pRatio ** (1/k)) * ((((k+1)/(k-1))*(1-(pRatio**((k-1)/k))))**0.5)

class Nozzle(PropertyCollection):
    """An object that contains the details about a motor's nozzle."""
    def __init__(self):
        super().__init__()
        self.props['throat'] = FloatProperty('Throat Diameter', 'm', 0, 0.5)
        self.props['exit'] = FloatProperty('Exit Diameter', 'm', 0, 1)
        self.props['efficiency'] = FloatProperty('Efficiency', '', 0, 2)
        self.props['divAngle'] = FloatProperty('Divergence Half Angle', 'deg', 0, 90)
        self.props['convAngle'] = FloatProperty('Convergence Half Angle', 'deg', 0, 90)
        self.props['throatLength'] = FloatProperty('Throat Length', 'm', 0, 0.5)
        self.props['slagCoeff'] = FloatProperty('Slag Buildup Coefficient', '(m*Pa)/s', 0, 1e6)
        self.props['erosionCoeff'] = FloatProperty('Throat Erosion Coefficient', 'm/(s*Pa)', 0, 1e6)

    def getDetailsString(self, preferences):
        """Returns a human-readable string containing some details about the nozzle."""
        lengthUnit = preferences.units.getProperty('m')
        return 'Throat: ' + self.props['throat'].dispFormat(lengthUnit)

    def calcExpansion(self):
        """Returns the nozzle's expansion ratio."""
        return (self.props['exit'].getValue() / self.props['throat'].getValue()) ** 2

    def getThroatArea(self, dThroat=0):
        """Returns the area of the nozzle's throat. The optional parameter is added on to the nozzle throat diameter
        allow erosion or slag buildup during a burn."""
        return geometry.circleArea(self.props['throat'].getValue() + dThroat)

    def getExitArea(self):
        """Return the area of the nozzle's exit."""
        return geometry.circleArea(self.props['exit'].getValue())

    def getExitPressure(self, k, inputPressure):
        """Solves for the nozzle's exit pressure, given an input pressure and the gas's specific heat ratio."""
        return fsolve(lambda x: (1/self.calcExpansion()) - eRatioFromPRatio(k, x / inputPressure), 0)[0]

    def getDivergenceLosses(self):
        """Returns nozzle efficiency losses due to divergence angle"""
        divAngleRad = math.radians(self.props["divAngle"].getValue())
        return (1 + math.cos(divAngleRad)) / 2

    def getThroatLosses(self, dThroat=0):
        """Returns the losses caused by the throat aspect ratio as described in this document:
        http://rasaero.com/dloads/Departures%20from%20Ideal%20Performance.pdf"""
        throatAspect = self.props['throatLength'].getValue() / (self.props['throat'].getValue() + dThroat)
        if throatAspect > 0.45:
            return 0.95
        return 0.99 - (0.0333 * throatAspect)

    def getSkinLosses(self):
        """Returns the losses due to drag on the nozzle surface as described here:
        https://apps.dtic.mil/dtic/tr/fulltext/u2/a099791.pdf. This is a constant for now, as people likely don't have
        a way to measure this themselves."""
        return 0.99

    def getGeometryErrors(self):
        """Returns a list containing any errors with the nozzle's properties."""
        errors = []
        if self.props['throat'].getValue() == 0:
            aText = 'Throat diameter must not be 0'
            errors.append(SimAlert(SimAlertLevel.ERROR, SimAlertType.GEOMETRY, aText, 'Nozzle'))
        if self.props['exit'].getValue() < self.props['throat'].getValue():
            aText = 'Exit diameter must not be smaller than throat diameter'
            errors.append(SimAlert(SimAlertLevel.ERROR, SimAlertType.GEOMETRY, aText, 'Nozzle'))
        if self.props['efficiency'].getValue() == 0:
            aText = 'Efficiency must not be 0'
            errors.append(SimAlert(SimAlertLevel.ERROR, SimAlertType.CONSTRAINT, aText, 'Nozzle'))
        return errors
