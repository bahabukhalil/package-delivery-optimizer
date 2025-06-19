from copy import deepcopy
import random
from models import DeliverySolution, Van

class GeneticAlgorithmSolver:
    def __init__(self, vans, parcels, population_size=75, mutation_rate=0.05, generations=500):
        self.vans = vans
        self.parcels = parcels
        self.size = population_size
        self.mutation = mutation_rate
        self.generations = generations

    def generate_solution(self):
        vans_copy = [Van(v.id, v.capacity) for v in self.vans]
        unassigned = self.parcels[:]
        random.shuffle(unassigned)

        for p in unassigned:
            random.shuffle(vans_copy)
            for v in vans_copy:
                if v.can_fit(p):
                    v.assigned_parcels.append(p)
                    break

        return DeliverySolution(vans_copy)

    def crossover(self, p1, p2):

        seen_ids = set()
        merged_parcels = []
        for sol in [p1, p2]:
            for v in sol.vans:
                for p in v.assigned_parcels:
                    if p.id not in seen_ids:
                        merged_parcels.append(p)
                        seen_ids.add(p.id)

        random.shuffle(merged_parcels)
        vans = [Van(v.id, v.capacity) for v in self.vans]
        for p in merged_parcels:
            for v in vans:
                if v.can_fit(p):
                    v.assigned_parcels.append(p)
                    break
        return DeliverySolution(vans)

    def mutate(self, solution):
        vans = deepcopy(solution.vans)
        flat = [p for v in vans for p in v.assigned_parcels]
        if len(flat) < 2:
            return DeliverySolution(vans)

        p1, p2 = random.sample(flat, 2)
        v1 = v2 = None

        for v in vans:
            if p1 in v.assigned_parcels:
                v1 = v
            if p2 in v.assigned_parcels:
                v2 = v

        if v1 != v2:
            v1.assigned_parcels.remove(p1)
            v2.assigned_parcels.remove(p2)

            if v1.can_fit(p2) and v2.can_fit(p1):
                v1.assigned_parcels.append(p2)
                v2.assigned_parcels.append(p1)
            else:

                v1.assigned_parcels.append(p1)
                v2.assigned_parcels.append(p2)

        return DeliverySolution(vans)

    def solve(self):
        pop = [self.generate_solution() for _ in range(self.size)]

        for _ in range(self.generations):
            pop.sort(key=lambda s: s.calculate_total_distance())
            new_pop = pop[:2]

            while len(new_pop) < self.size:
                p1, p2 = random.sample(pop[:20], 2)
                child = self.crossover(p1, p2)
                if random.random() < self.mutation:
                    child = self.mutate(child)
                new_pop.append(child)

            pop = new_pop

        return min(pop, key=lambda s: s.calculate_total_distance())
