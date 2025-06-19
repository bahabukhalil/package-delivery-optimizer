import math
import random

class Parcel:
    def __init__(self, pid, x, y, weight, priority):
        self.id, self.x, self.y, self.weight, self.priority = pid, x, y, weight, priority

    def __str__(self):
        return f"Parcel {self.id} ({self.x:.1f},{self.y:.1f}) {self.weight}kg P{self.priority}"

class Van:
    def __init__(self, vid, capacity):
        self.id, self.capacity = vid, capacity
        self.assigned_parcels = []

    def can_fit(self, parcel):
        return self.remaining_capacity() >= parcel.weight

    def remaining_capacity(self):
        return self.capacity - sum(p.weight for p in self.assigned_parcels)

    def calculate_route_distance(self):
        if not self.assigned_parcels:
            return 0
        d, x, y = 0, 0, 0
        for p in self.assigned_parcels:
            d += math.hypot(p.x - x, p.y - y)
            x, y = p.x, p.y
        return d + math.hypot(x, y)  # back to shop

    def __str__(self):
        return f"Van {self.id} | Capacity: {self.capacity:.1f}kg | Remaining: {self.remaining_capacity():.1f}kg | Parcels: {len(self.assigned_parcels)}"

class DeliverySolution:
    def __init__(self, vans):
        self.vans = vans

    def calculate_total_distance(self):
        return sum(v.calculate_route_distance() for v in self.vans)

    def get_priority_score(self):
        score = 0
        for van in self.vans:
            for i, p1 in enumerate(van.assigned_parcels):
                for p2 in van.assigned_parcels[:i]:
                    if p1.priority < p2.priority:
                        score += (p2.priority - p1.priority)
        return score

    def copy(self):
        new_vans = [Van(v.id, v.capacity) for v in self.vans]
        for old_van, new_van in zip(self.vans, new_vans):
            new_van.assigned_parcels = old_van.assigned_parcels[:]
        return DeliverySolution(new_vans)

    def get_all_parcels(self):
        return [p for v in self.vans for p in v.assigned_parcels]

    def __str__(self):
        return f"Total distance: {self.calculate_total_distance():.2f} km"

def generate_random_data(num_vans, num_parcels):
    vans = [Van(i, random.uniform(80, 150)) for i in range(num_vans)]
    parcels = [Parcel(i, random.uniform(0, 100), random.uniform(0, 100),
                      random.uniform(5, 50), random.randint(1, 5)) for i in range(num_parcels)]
    return vans, parcels

def load_user_input_file(lines):
    i, vans, parcels = 0, [], []
    for _ in range(int(lines[i])):
        i += 1
        vid, cap = map(float, lines[i].split())
        vans.append(Van(int(vid), cap))
    i += 1
    for _ in range(int(lines[i])):
        i += 1
        pid, x, y, w, p = lines[i].split()
        parcels.append(Parcel(int(pid), float(x), float(y), float(w), int(p)))
    return vans, parcels

