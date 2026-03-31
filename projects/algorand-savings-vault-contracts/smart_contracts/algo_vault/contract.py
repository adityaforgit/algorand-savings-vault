from algopy import ARC4Contract, UInt64, GlobalState
from algopy.arc4 import abimethod


class AlgoVault(ARC4Contract):

    def __init__(self) -> None:
        self.total_savings = GlobalState(UInt64)
        self.milestone = GlobalState(UInt64)

    # ✅ initialize values
    @abimethod()
    def initialize(self) -> None:
        self.total_savings.value = UInt64(0)
        self.milestone.value = UInt64(100)

    # deposit
    @abimethod()
    def deposit(self, amount: UInt64) -> None:
        self.total_savings.value += amount

    # get savings
    @abimethod()
    def get_total_savings(self) -> UInt64:
        return self.total_savings.value

    # check milestone
    @abimethod()
    def check_milestone(self) -> UInt64:
        if self.total_savings.value >= self.milestone.value:
            return UInt64(1)
        return UInt64(0)