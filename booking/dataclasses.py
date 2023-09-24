from dataclasses import dataclass


@dataclass
class BookingPriceTotal:
    platform_rate: float
    cleaning_cost: float
