from src.clock_factory import *
from unittest import TestCase

class TestDemo(TestCase):
    def test_one(self):
        factory = ClockFactory()
        clock = factory.create("hh:mm")
        for i in range(10000):
            clock.increment()
            print(clock.str())
    def test_two(self):
        factory = ClockFactory()
        clock = factory.create("hh:mm")
        clock.invariant()
    def test_tree(self):
        factory = ClockFactory()
        clock = factory.create("hh:mm")
        for number in clock.numbers:
            number.reset()