from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

def allocate(line: OrderLine, batches: List[Batch]):
    allocatable_batches = (b for b in batches if b.can_allocate(line))
    selected_batch = None
    for ab in allocatable_batches:
        if ab.eta is None:
            ab.allocate(line)
            return ab.reference
        if selected_batch is None or ab.eta < selected_batch.eta:
            selected_batch = ab

    if selected_batch:
        selected_batch.allocate(line)
        return selected_batch.reference

    raise OutOfStock(f"Out of stock for sku {line.sku}")


class OutOfStock(Exception):
    pass

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None: 
            return True
        return self.eta > other.eta

    def __hash__(self):
        return hash(self.reference)

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
