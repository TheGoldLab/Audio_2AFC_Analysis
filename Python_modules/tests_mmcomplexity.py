"""
This is a test module to test the mmcomplexity module with unittest
Main reference: https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp
"""
import unittest
import types
import mmcomplexity as mmx


class TestModuleFunctions(unittest.TestCase):
    def test_allowed_sides(self):
        self.assertEqual(mmx.SIDES, {'left', 'right'})

    def test_check_valid_side(self):
        self.assertIsNone(mmx.check_valid_side('left'))
        self.assertIsNone(mmx.check_valid_side('right'))

        self.assertRaises(ValueError, mmx.check_valid_side, 0)
        self.assertRaises(ValueError, mmx.check_valid_side, 1)
        self.assertRaises(ValueError, mmx.check_valid_side, True)
        self.assertRaises(ValueError, mmx.check_valid_side, False)
        self.assertRaises(TypeError, mmx.check_valid_side, ['left'])

    def test_switch_side(self):
        self.assertEqual('left', mmx.switch_side('right'))
        self.assertEqual('right', mmx.switch_side('left'))
        mmx.SIDES.add('up')
        self.assertRaises(RuntimeError, mmx.switch_side, 'left')
        mmx.SIDES.remove('up')


class TestStimulusBlock(unittest.TestCase):
    def setUp(self):
        self.n = 10  # number of trials to generate
        self.h = 0.3 # hazard rate
        self.stim = mmx.Stimulus(self.n, self.h)

    def tearDown(self):
        del self.n
        del self.h
        del self.stim

    def test_number_of_trials(self):
        self.assertEqual(self.n, self.stim.num_trials)
        self.assertEqual(self.n, len(self.stim.sound_sequence))
        self.assertEqual(self.n, len(self.stim.source_sequence))

    def test_scalar_hazard(self):
        """test that only scalar h with 0 <= h <= 1 are accepted"""
        bad_h = [-1, 12, [.2,.3]]
        good_h = [0, 1, 3/4]
        for h in bad_h:
            self.assertRaises(ValueError, mmx.Stimulus, 10, h)
        for h in good_h:
            _ = mmx.Stimulus(10, h)

    def test_sequences_are_lists(self):
        self.assertIsInstance(self.stim.source_sequence, list)
        self.assertIsInstance(self.stim.sound_sequence, list)


class TestIdealObserverModel(unittest.TestCase):
    def setUp(self):
        self.n = 10
        self.s = mmx.Stimulus(self.n, .3)
        self.o = mmx.BinaryDecisionMaker(self.s)

    def tearDown(self):
        del self.s
        del self.o
        del self.n

    def test_num_observations(self):
        self.assertIsNone(self.o.observations)
        self.o.observe()
        num_obs = len(self.o.observations)
        self.assertEqual(num_obs, self.n)

    def test_decision_generator(self):
        self.o.observe()
        dec = self.o.process()
        self.assertIsInstance(dec, types.GeneratorType)
        self.assertEqual(len(list(dec)), self.n)
        dec2 = self.o.process()
        # check new generator is not exhausted
        first_item = next(dec2, 'exhausted')
        self.assertNotEqual(first_item, 'exhausted')
        self.assertIsInstance(first_item, tuple)








if __name__ == '__main__':
    unittest.main()
