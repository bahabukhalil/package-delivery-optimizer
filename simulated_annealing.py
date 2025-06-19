import random
import math
from copy import deepcopy
from models import DeliverySolution, Van

class SimulatedAnnealingSolver:
    def __init__(self, vans, parcels, initial_temp=1000, cooling_rate=0.95, stopping_temp=1, iterations_per_temp=100):
        self.vans = vans
        self.parcels = parcels
        self.temp = initial_temp
        self.cooling = cooling_rate
        self.stop = stopping_temp
        self.iters = iterations_per_temp

    def generate_initial_solution(self):
        vans_copy = [Van(v.id, v.capacity) for v in self.vans]
        unassigned = []

        for p in sorted(self.parcels, key=lambda p: p.priority):
            assigned = False
            for v in sorted(vans_copy, key=lambda v: v.remaining_capacity(), reverse=True):
                if v.can_fit(p):
                    v.assigned_parcels.append(p)
                    assigned = True
                    break
            if not assigned:
                unassigned.append(p)

        if len(unassigned) == len(self.parcels):
            raise Exception("No parcels could be assigned. Van capacities might be too low.")

        return DeliverySolution(vans_copy)

    def get_neighbor(self, solution):
        new_sol = deepcopy(solution)
        move = random.choice(["swap", "relocate", "reverse"])
        vans = [v for v in new_sol.vans if v.assigned_parcels]

        if move == "swap" and len(vans) >= 2:
            v1, v2 = random.sample(vans, 2)
            p1, p2 = random.choice(v1.assigned_parcels), random.choice(v2.assigned_parcels)
            if (v1.remaining_capacity() + p1.weight - p2.weight >= 0 and
                v2.remaining_capacity() + p2.weight - p1.weight >= 0):
                i1, i2 = v1.assigned_parcels.index(p1), v2.assigned_parcels.index(p2)
                v1.assigned_parcels[i1], v2.assigned_parcels[i2] = p2, p1

        elif move == "relocate" and len(vans) >= 2:
            src = random.choice(vans)
            tgt = random.choice([v for v in new_sol.vans if v != src])
            if src.assigned_parcels:
                p = random.choice(src.assigned_parcels)
                if tgt.can_fit(p):
                    src.assigned_parcels.remove(p)
                    tgt.assigned_parcels.append(p)

        elif move == "reverse":
            van_choices = [v for v in vans if len(v.assigned_parcels) >= 2]
            if van_choices:
                van = random.choice(van_choices)
                i, j = sorted(random.sample(range(len(van.assigned_parcels)), 2))
                van.assigned_parcels[i:j+1] = list(reversed(van.assigned_parcels[i:j+1]))

        return new_sol

    def acceptance_probability(self, curr_cost, new_cost, temperature):
        if new_cost < curr_cost:
            return 1.0
        return math.exp(-(new_cost - curr_cost) / temperature)

    def solve(self):
        current = self.generate_initial_solution()
        best = deepcopy(current)
        temp = self.temp

        while temp > self.stop:
            for _ in range(self.iters):
                neighbor = self.get_neighbor(current)
                c_cost = current.calculate_total_distance()
                n_cost = neighbor.calculate_total_distance()

                if self.acceptance_probability(c_cost, n_cost, temp) > random.random():
                    current = neighbor
                    if n_cost < best.calculate_total_distance():
                        best = deepcopy(neighbor)

            temp *= self.cooling

        return best
