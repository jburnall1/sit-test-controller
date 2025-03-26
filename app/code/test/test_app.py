import context
import unittest
import test_main


class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_initialise_scenario(self):
        app = test_main.app.App()

    def test_has_last_three_sub_tests_resulted_in_all_failed_transmissions(self):
        app = test_main.app.App()
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        self.assertFalse(app._has_last_three_sub_tests_resulted_in_all_failed_transmissions())
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        self.assertFalse(app._has_last_three_sub_tests_resulted_in_all_failed_transmissions())
        app.results['sub_tests']['attenuation_120']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_110']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_100']=[0,0,0,0,0,0,0,0,0,0]
        self.assertTrue(app._has_last_three_sub_tests_resulted_in_all_failed_transmissions())

    def test_determine_and_set_next_attenuation_value(self):
        app = test_main.app.App()
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==110)
        app.interferer_to_sut_rx_attenuator_value = 70
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,0]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==75)
        app.interferer_to_sut_rx_attenuator_value = 70
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,1]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==60)
        app.interferer_to_sut_rx_attenuator_value = 75
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_75']=[0,0,0,0,0,0,0,0,0,0]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==76)
        app.interferer_to_sut_rx_attenuator_value = 76
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_75']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_76']=[0,0,0,0,0,0,0,0,0,0]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==77)
        app.interferer_to_sut_rx_attenuator_value = 77
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_75']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_76']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_77']=[0,0,0,0,0,0,0,0,0,0]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==78)
        app.interferer_to_sut_rx_attenuator_value = 78
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_75']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_76']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_77']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_78']=[0,0,0,0,0,0,0,0,0,0]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==79)
        app.interferer_to_sut_rx_attenuator_value = 79
        app.results['sub_tests'] = {}
        app.results['sub_tests']['attenuation_120']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_110']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_100']=[1,1,1,1,1,1,1,1,1,1]
        app.results['sub_tests']['attenuation_90']=[1,1,1,1,1,1,0,1,0,0]
        app.results['sub_tests']['attenuation_80']=[1,1,1,1,1,1,1,1,1,0]
        app.results['sub_tests']['attenuation_70']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_75']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_76']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_77']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_78']=[0,0,0,0,0,0,0,0,0,0]
        app.results['sub_tests']['attenuation_79']=[0,0,0,0,0,0,0,0,0,0]
        next_value = app._determine_and_set_next_attenuation_value()
        self.assertTrue(next_value==80)
        self.assertFalse(app.results['sub_tests'].get('attenuation_80', False))

