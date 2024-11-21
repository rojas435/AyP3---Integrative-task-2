# bayesianNetwork.py
import itertools
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class CarDiagnosticBN:
    def __init__(self):
        # Define the Bayesian Network structure
        self.model = BayesianNetwork([
            ('Check struts, shocks, springs, frame welds.', 'Clunk or single tick?'),
            ('Check struts, shocks, springs, frame welds.', 'Noise on bumps only?'),

            ('Check ball joints, brakes, rack and tie rod ends, motor mounts.', 'Clunk or single tick?'),
            ('Check ball joints, brakes, rack and tie rod ends, motor mounts.', 'Noise on bumps only?'),

            ('Possible rear brake adjuster. Make sure parking brake is fully released.', 'Clunk or single tick?'),
            ('Possible rear brake adjuster. Make sure parking brake is fully released.', 'Only ticks when moving?'),
            ('Possible rear brake adjuster. Make sure parking brake is fully released.', 'Ticks rolling in neutral?'),
            ('Possible rear brake adjuster. Make sure parking brake is fully released.', 'Ticks only in reverse?'),

            ('Possible transmission tick. Check transmission fluid, filter.', 'Clunk or single tick?'),
            ('Possible transmission tick. Check transmission fluid, filter.', 'Only ticks when moving?'),
            ('Possible transmission tick. Check transmission fluid, filter.', 'Ticks rolling in neutral?'),
            ('Possible transmission tick. Check transmission fluid, filter.', 'Ticks only in reverse?'),

            ('CV joint going out or tire too big for wheel well (but not for long).', 'Clunk or single tick?'),
            ('CV joint going out or tire too big for wheel well (but not for long).', 'Only ticks when moving?'),
            ('CV joint going out or tire too big for wheel well (but not for long).', 'Ticks rolling in neutral?'),
            ('CV joint going out or tire too big for wheel well (but not for long).', 'Frequency drops on shifts?'),
            ('CV joint going out or tire too big for wheel well (but not for long).', 'Only ticks in turns, curves?'),

            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Clunk or single tick?'),
            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Only ticks when moving?'),
            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Ticks rolling in neutral?'),
            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Frequency drops on shifts?'),
            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Only ticks in turns, curves?'),
            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Just Changed Tires?'),
            ('Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', 'Removed hubcaps?'),

            ('Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', 'Clunk or single tick?'),
            ('Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', 'Only ticks when moving?'),
            ('Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', 'Ticks rolling in neutral?'),
            ('Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', 'Frequency drops on shifts?'),
            ('Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', 'Only ticks in turns, curves?'),
            ('Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', 'Just Changed Tires?'),

            ('Check bolted wheel covers, hub protectors for pebbles.', 'Clunk or single tick?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Only ticks when moving?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Ticks rolling in neutral?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Frequency drops on shifts?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Only ticks in turns, curves?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Just Changed Tires?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Removed hubcaps?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Inspect tire threads?'),
            ('Check bolted wheel covers, hub protectors for pebbles.', 'Ticks only slow speed?'),

            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Clunk or single tick?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Only ticks when moving?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Ticks rolling in neutral?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Frequency drops on shifts?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Only ticks in turns, curves?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Just Changed Tires?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Removed hubcaps?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Inspect tire threads?'),
            ('Likely brake pads ticking on warped rotor, also check axles for rubbing.', 'Ticks only slow speed?'),

            ('Check for nails or stones embedded in tire thread', 'Clunk or single tick?'),
            ('Check for nails or stones embedded in tire thread', 'Only ticks when moving?'),
            ('Check for nails or stones embedded in tire thread', 'Ticks rolling in neutral?'),
            ('Check for nails or stones embedded in tire thread', 'Frequency drops on shifts?'),
            ('Check for nails or stones embedded in tire thread', 'Only ticks in turns, curves?'),
            ('Check for nails or stones embedded in tire thread', 'Just Changed Tires?'),
            ('Check for nails or stones embedded in tire thread', 'Removed hubcaps?'),
            ('Check for nails or stones embedded in tire thread', 'Inspect tire threads?'),
            ('Check for nails or stones embedded in tire thread', 'Ticks only slow speed?'),

            ('Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.', 'Clunk or single tick?'),
            ('Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.', 'Only ticks when moving?'),
            ('Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.', 'Ticks rolling in neutral?'),
            ('Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.', 'Frequency drops on shifts?'),
            ('Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.', 'Only ticks when cold?'),


            ('Always check the silly stuff, like your passenger tapping on the roof.', 'Clunk or single tick?'),
            ('Always check the silly stuff, like your passenger tapping on the roof.', 'Only ticks when moving?'),
            ('Always check the silly stuff, like your passenger tapping on the roof.', 'Ticks rolling in neutral?'),
            ('Always check the silly stuff, like your passenger tapping on the roof.', 'Frequency drops on shifts?'),
            ('Always check the silly stuff, like your passenger tapping on the roof.', 'Only ticks when cold?'),
            ('Always check the silly stuff, like your passenger tapping on the roof.', 'Windshield wipers, radio off?'),

            ('Look for pulley wobble, inspect belts. Check for exhaust manifold leak. Get somebody with better hearing to help you localize where it’s coming from on the engine.', 'Clunk or single tick?'),
            ('Look for pulley wobble, inspect belts. Check for exhaust manifold leak. Get somebody with better hearing to help you localize where it’s coming from on the engine.', 'Only ticks when moving?'),
            ('Look for pulley wobble, inspect belts. Check for exhaust manifold leak. Get somebody with better hearing to help you localize where it’s coming from on the engine.', 'Windshield wipers, radio off?')


        ])

        # CPDs para nodos observables
        cpd_clunk_tick_obs = TabularCPD(
            variable='Clunk or single tick?', variable_card=2,
            values=[[0.7], [0.3]]  # Probabilidades iniciales
        )

        cpd_noise_bumps_obs = TabularCPD(
            variable='Noise on bumps only?', variable_card=2,
            values=[[0.6], [0.4]]  # Probabilidades iniciales
        )

        cpd_ticks_moving = TabularCPD(
            variable='Only ticks when moving?', variable_card=2,
            values=[[0.8], [0.2]]  # Probabilidades iniciales
        )

        cpd_ticks_neutral = TabularCPD(
            variable='Ticks rolling in neutral?', variable_card=2,
            values=[[0.85], [0.15]]  # Probabilidades iniciales
        )

        cpd_ticks_reverse = TabularCPD(
            variable='Ticks only in reverse?', variable_card=2,
            values=[[0.75], [0.25]]  # Probabilidades iniciales
        )

        cpd_frequency_drops = TabularCPD(
            variable='Frequency drops on shifts?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_ticks_turns = TabularCPD(
            variable='Only ticks in turns, curves?', variable_card=2,
            values=[[0.85], [0.15]]  # Probabilidades iniciales
        )

        cpd_changed_tires = TabularCPD(
            variable='Just Changed Tires?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_removed_hubcaps = TabularCPD(
            variable='Removed hubcaps?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_inspect_threads = TabularCPD(
            variable='Inspect tire threads?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_ticks_slow_speed = TabularCPD(
            variable='Ticks only slow speed?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_ticks_cold = TabularCPD(
            variable='Only ticks when cold?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_wipers_radio_off = TabularCPD(
            variable='Windshield wipers, radio off?', variable_card=2,
            values=[[0.9], [0.1]]  # Probabilidades iniciales
        )

        cpd_check_struts = TabularCPD(
            variable='Check struts, shocks, springs, frame welds.', variable_card=2,
            evidence=['Clunk or single tick?', 'Noise on bumps only?'],
            evidence_card=[2, 2],
            values=[
                [0.9, 0.7, 0.5, 0.3],  # Probability of True
                [0.1, 0.3, 0.5, 0.7]   # Probability of False
            ]
        )

        cpd_check_ball_joints = TabularCPD(
            variable='Check ball joints, brakes, rack and tie rod ends, motor mounts.', variable_card=2,
            evidence=['Clunk or single tick?', 'Noise on bumps only?'],
            evidence_card=[2, 2],
            values=[
                [0.85, 0.65, 0.45, 0.25],
                [0.15, 0.35, 0.55, 0.75]
            ]
        )

        cpd_possible_rear_brake_adjuster = TabularCPD(
            variable='Possible rear brake adjuster. Make sure parking brake is fully released.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Ticks only in reverse?'],
            evidence_card=[2, 2, 2, 2],
            values=[
                [0.8, 0.7, 0.6, 0.5, 0.7, 0.6, 0.5, 0.4,
                0.6, 0.5, 0.4, 0.3, 0.5, 0.4, 0.3, 0.2],
                [0.2, 0.3, 0.4, 0.5, 0.3, 0.4, 0.5, 0.6,
                0.4, 0.5, 0.6, 0.7, 0.5, 0.6, 0.7, 0.8]
            ]
        )

        cpd_possible_transmission_tick = TabularCPD(
            variable='Possible transmission tick. Check transmission fluid, filter.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Ticks only in reverse?'],
            evidence_card=[2, 2, 2, 2],
            values=[
                [0.75, 0.65, 0.55, 0.45, 0.65, 0.55, 0.45, 0.35,
                0.55, 0.45, 0.35, 0.25, 0.45, 0.35, 0.25, 0.15],
                [0.25, 0.35, 0.45, 0.55, 0.35, 0.45, 0.55, 0.65,
                0.45, 0.55, 0.65, 0.75, 0.55, 0.65, 0.75, 0.85]
            ]
        )

        cpd_cv_joint_tire = TabularCPD(
            variable='CV joint going out or tire too big for wheel well (but not for long).', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks in turns, curves?'],
            evidence_card=[2, 2, 2, 2, 2],
            values=[
                [0.9, 0.8, 0.7, 0.6, 0.7, 0.6, 0.5, 0.4, 0.8, 0.7, 0.6, 0.5, 0.7, 0.6, 0.5, 0.4, 
                 0.6, 0.5, 0.4, 0.3, 0.5, 0.4, 0.3, 0.2, 0.4, 0.3, 0.2, 0.1, 0.3, 0.2, 0.1, 0.1],  # True
                [0.1, 0.2, 0.3, 0.4, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.3, 0.4, 0.5, 0.6, 
                 0.4, 0.5, 0.6, 0.7, 0.5, 0.6, 0.7, 0.8, 0.6, 0.7, 0.8, 0.9, 0.7, 0.8, 0.9, 0.9]   # False
            ]
        )

        cpd_remove_hubcaps = TabularCPD(
            variable='Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks in turns, curves?', 'Just Changed Tires?', 'Removed hubcaps?'],
            evidence_card=[2, 2, 2, 2, 2, 2, 2],
            values=[
                [0.85, 0.75, 0.65, 0.55, 0.75, 0.65, 0.55, 0.45, 0.65, 0.55, 0.45, 0.35, 0.55, 0.45, 0.35, 0.25, ...],  # True
                [0.15, 0.25, 0.35, 0.45, 0.25, 0.35, 0.45, 0.55, 0.35, 0.45, 0.55, 0.65, 0.45, 0.55, 0.65, 0.75, ...]   # False
            ]
        )

        cpd_stop_driving = TabularCPD(
            variable='Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks in turns, curves?', 'Just Changed Tires?'],
            evidence_card=[2, 2, 2, 2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )

        cpd_check_bolted_wheel = TabularCPD(
            variable='Check bolted wheel covers, hub protectors for pebbles.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks in turns, curves?', 'Just Changed Tires?', 'Removed hubcaps?', 'Inspect tire threads?', 'Ticks only slow speed?'],
            evidence_card=[2, 2, 2, 2, 2, 2, 2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )

        cpd_likely_brake_pads = TabularCPD(
            variable='Likely brake pads ticking on warped rotor, also check axles for rubbing.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks in turns, curves?', 'Just Changed Tires?', 'Removed hubcaps?', 'Inspect tire threads?', 'Ticks only slow speed?'],
            evidence_card=[2, 2, 2, 2, 2, 2, 2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )

        cpd_check_nails = TabularCPD(
            variable='Check for nails or stones embedded in tire thread', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks in turns, curves?', 'Just Changed Tires?', 'Removed hubcaps?', 'Inspect tire threads?', 'Ticks only slow speed?'],
            evidence_card=[2, 2, 2, 2, 2, 2, 2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )

        cpd_check_exhaust = TabularCPD(
            variable='Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks when cold?'],
            evidence_card=[2, 2, 2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )

        cpd_check_silly = TabularCPD(
            variable='Always check the silly stuff, like your passenger tapping on the roof.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Ticks rolling in neutral?', 'Frequency drops on shifts?', 'Only ticks when cold?', 'Windshield wipers, radio off?'],
            evidence_card=[2, 2, 2, 2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )

        cpd_look_pulley = TabularCPD(
            variable='Look for pulley wobble, inspect belts. Check for exhaust manifold leak. Get somebody with better hearing to help you localize where it’s coming from on the engine.', variable_card=2,
            evidence=['Clunk or single tick?', 'Only ticks when moving?', 'Windshield wipers, radio off?'],
            evidence_card=[2, 2, 2],
            values=[
                [0.9, 0.85, 0.8, 0.75, 0.85, 0.8, 0.75, 0.7, 0.8, 0.75, 0.7, 0.65, 0.75, 0.7, 0.65, 0.6,
                0.7, 0.65, 0.6, 0.55, 0.65, 0.6, 0.55, 0.5, 0.6, 0.55, 0.5, 0.45, 0.55, 0.5, 0.45, 0.4],  # True
                [0.1, 0.15, 0.2, 0.25, 0.15, 0.2, 0.25, 0.3, 0.2, 0.25, 0.3, 0.35, 0.25, 0.3, 0.35, 0.4,
                0.3, 0.35, 0.4, 0.45, 0.35, 0.4, 0.45, 0.5, 0.4, 0.45, 0.5, 0.55, 0.45, 0.5, 0.55, 0.6]   # False
            ]
        )
        
        # Add CPDs to the model
        self.model.add_cpds(
            cpd_clunk_tick_obs,
            cpd_noise_bumps_obs, cpd_ticks_moving,
            cpd_ticks_neutral, cpd_ticks_reverse, 
            cpd_frequency_drops, cpd_ticks_turns, cpd_changed_tires,
            cpd_removed_hubcaps, cpd_inspect_threads, cpd_ticks_slow_speed, 
            cpd_ticks_cold, cpd_wipers_radio_off,
            cpd_check_struts, cpd_check_ball_joints, cpd_possible_rear_brake_adjuster,
            cpd_possible_transmission_tick,
            cpd_cv_joint_tire, cpd_remove_hubcaps, cpd_stop_driving,
            cpd_check_bolted_wheel, cpd_likely_brake_pads, cpd_check_nails,
            cpd_check_exhaust, cpd_check_silly, cpd_look_pulley
        )
        
        # Initialize inference engine
        self.inference = VariableElimination(self.model)
    
    def get_diagnostic_flow(self):
        """
        Returns the diagnostic questions and flow
        """
        return {
            'sound_diagnostic': [
                "Is the noise a 'clunk' or a single 'tick'?",
                "Does the noise only happen when going over bumps?",
                "Does the noise only occur when the car is moving?",
                "Does the noise happen when rolling in neutral?",
                "Does the frequency decrease during gear shifts?",
                "Does the noise only happen in turns or curves?",
                "Did you just change tires?",
                "Were the hubcaps removed?",
                "Does the noise only happen at low speeds?",
                "Ticks only in reverse?",
                "Inspect tire threads?",
                "Only ticks when cold?",
                "Windshield wipers, radio off?",

            ]
        }
    
    def get_probabilities(self, symptoms):
        """
        Calculate probabilities based on symptoms
        """
        evidence = {}
        
        # Map symptoms to Bayesian Network variables
        symptom_mapping = {
            'clunk_tick': 'Clunk or single tick?',
            'noise_bumps': 'Noise on bumps only?',
            'ticks_moving': 'Only ticks when moving?',
            'ticks_neutral': 'Ticks rolling in neutral?',
            'ticks_reverse': 'Ticks only in reverse?',
            'ticks_turns': 'Only ticks in turns, curves?',
            'frequency_shifts': 'Frequency drops on shifts?',
            'ticks_slow_speed': 'Ticks only slow speed?',
            'changed_tires': 'Just Changed Tires?',
            'removed_hubcaps': 'Removed hubcaps?',
            'inspect_threads': 'Inspect tire threads?',
            'ticks_when_cold': 'Only ticks when cold?',
            'windshield_wipers_off': 'Windshield wipers, radio off?',
        }
        
        for symptom, value in symptoms.items():
            mapped_var = symptom_mapping.get(symptom.lower())
            if mapped_var:
                evidence[mapped_var] = 1 if value.lower() == 'si' else 0
        
        # Calculate probabilities
        results = {}
        
        # Main problem probabilities
        problems = [
        'Check struts, shocks, springs, frame welds.',
        'Check ball joints, brakes, rack and tie rod ends, motor mounts.',
        'Possible rear brake adjuster. Make sure parking brake is fully released.',
        'Possible transmission tick. Check transmission fluid, filter.',
        'CV joint going out or tire too big for wheel well (but not for long).',
        'Remove hubcaps before proceeding. Loose wire retainer, pebbles can tick.',
        'Stop driving (and surfing the web) now! Make sure the wheel lugs were tightened.',
        'Check bolted wheel covers, hub protectors for pebbles.',
        'Likely brake pads ticking on warped rotor, also check axles for rubbing.',
        'Check for nails or stones embedded in tire thread',
        'Check exhaust pipe forward of catalytic converter for leaks. Listen for lifter rap on valve cover.',
        'Always check the silly stuff, like your passenger tapping on the roof.',
        'Look for pulley wobble, inspect belts. Check for exhaust manifold leak. Get somebody with better hearing to help you localize where it’s coming from on the engine.',]
        
        for problem in problems:
            query = self.inference.query(
                variables=[problem],
                evidence=evidence
            )
            results[problem] = query.values[1] * 100
        
        # Secondary symptom probabilities
        secondary_symptoms = [
            'Windshield wipers, radio off?',
            'Just Changed Tires?',
            'Inspect tire threads?',
            'Removed hubcaps?',
            'Ticks only slow speed?',
        ]
        for symptom in secondary_symptoms:
            query = self.inference.query(
                variables=[symptom],
                evidence=evidence
            )
            results[symptom] = query.values[1] * 100
        
        return results