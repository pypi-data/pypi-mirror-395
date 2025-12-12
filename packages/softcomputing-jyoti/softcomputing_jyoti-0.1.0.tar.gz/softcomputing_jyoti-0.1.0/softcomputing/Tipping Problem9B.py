# PRACTICAL 9B
# Fuzzy Tipping Problem

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

quality['poor'] = fuzz.trimf(quality.universe, [0, 0, 5])
quality['average'] = fuzz.trimf(quality.universe, [0, 5, 10])
quality['good'] = fuzz.trimf(quality.universe, [5, 10, 10])

service['poor'] = fuzz.trimf(service.universe, [0, 0, 5])
service['average'] = fuzz.trimf(service.universe, [0, 5, 10])
service['good'] = fuzz.trimf(service.universe, [5, 10, 10])

tip['less'] = fuzz.trimf(tip.universe, [0, 0, 5])
tip['some'] = fuzz.trimf(tip.universe, [5, 10, 20])
tip['much'] = fuzz.trimf(tip.universe, [15, 25, 25])

rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['less'])
rule2 = ctrl.Rule(service['average'], tip['some'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['much'])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# USER INPUT
q = float(input("Enter quality (0–10): "))
s = float(input("Enter service (0–10): "))

tipping.input['quality'] = q
tipping.input['service'] = s
tipping.compute()

print("Recommended Tip:", tipping.output['tip'])

quality.view()
service.view()
tip.view()
