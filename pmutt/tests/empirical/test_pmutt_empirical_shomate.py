import unittest
import numpy as np
from ase.build import molecule
from pmutt import constants as c
from pmutt import get_molecular_weight
from pmutt.statmech import StatMech, trans, rot, vib, elec
from pmutt.empirical.shomate import Shomate


class TestShomate(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.Shomate_direct = Shomate(
            name='H2O',
            elements={'H': 2, 'O': 1},
            a=np.array([30.09200, 6.832514, 6.793435, -2.534480, 0.082139,
                        -250.8810, 223.3967, -241.8264]),
            T_low=500.,
            T_high=1700.
        )

        self.Shomate_direct_dict = {
            'class': "<class 'pmutt.empirical.shomate.Shomate'>",
            'name': 'H2O',
            'phase': None,
            'elements': {'H': 2, 'O': 1},
            'a': [30.09200, 6.832514, 6.793435, -2.534480, 0.082139,
                  -250.8810, 223.3967, -241.8264],
            'T_low': 500.,
            'T_high': 1700.,
            'notes': None,
            'model': None,
            'misc_models': None,
            'smiles': None,
            'type': 'shomate',
            'units': 'J/mol/K'
        }

        self.Shomate_data = Shomate.from_data(
            name='H2O',
            elements={'H': 2, 'O': 1},
            phase='g',
            T=np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                        725., 750., 775., 800., 825., 850., 875., 900., 925.,
                        950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                        1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                        1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                        1550., 1575., 1600., 1625., 1650., 1675., 1700.]),
            CpoR=np.array([4.235796744, 4.267598139, 4.300310233, 4.333821197,
                           4.368036178, 4.402873306, 4.438260758, 4.474134568,
                           4.510436977, 4.547115164, 4.584120285, 4.621406707,
                           4.658931423, 4.696653576, 4.734534089, 4.772535363,
                           4.810621034, 4.848755777, 4.886905141, 4.925035419,
                           4.963113539, 5.001106966, 5.038983636, 5.07671188,
                           5.114260381, 5.151598119, 5.18869434, 5.225518516,
                           5.262040323, 5.298229611, 5.334056387, 5.369490794,
                           5.404503098, 5.439063673, 5.47314299, 5.506711603,
                           5.539740144, 5.572199316, 5.604059881, 5.635292657,
                           5.665868512, 5.695758359, 5.724933152, 5.753363882,
                           5.781021572, 5.807877279, 5.833902083, 5.859067093,
                           5.883343439]),
            T_ref=298.,
            HoRT_ref=-97.55170383,
            SoR_ref=22.71163786
        )

        self.Shomate_statmech = Shomate.from_model(
            name='H2O',
            elements={'H': 2, 'O': 1},
            phase='g',
            model=StatMech,
            trans_model=trans.FreeTrans,
            n_degrees=3,
            vib_model=vib.HarmonicVib,
            elec_model=elec.GroundStateElec,
            rot_model=rot.RigidRotor,
            potentialenergy=-14.2209,
            atoms=molecule('H2O'),
            symmetrynumber=2,
            spin=0,
            vib_wavenumbers=np.array([0.47462, 0.46033, 0.19633]),
            T_low=500.,
            T_high=1700.
        )
        self.mw = get_molecular_weight({'H': 2, 'O': 1}) # g/mol

    def test_get_CpoR(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        CpoR_expected = np.array([4.235796744, 4.267598139, 4.300310233,
                                  4.333821197, 4.368036178, 4.402873306,
                                  4.438260758, 4.474134568, 4.510436977,
                                  4.547115164, 4.584120285, 4.621406707,
                                  4.658931423, 4.696653576, 4.734534089,
                                  4.772535363, 4.810621034, 4.848755777,
                                  4.886905141, 4.925035419, 4.963113539,
                                  5.001106966, 5.038983636, 5.07671188,
                                  5.114260381, 5.151598119, 5.18869434,
                                  5.225518516, 5.262040323, 5.298229611,
                                  5.334056387, 5.369490794, 5.404503098,
                                  5.439063673, 5.47314299, 5.506711603,
                                  5.539740144, 5.572199316, 5.604059881,
                                  5.635292657, 5.665868512, 5.695758359,
                                  5.724933152, 5.753363882, 5.781021572,
                                  5.807877279, 5.833902083, 5.859067093,
                                  5.883343439])
        np.testing.assert_almost_equal(self.Shomate_direct.get_CpoR(T=T[0]),
                                       CpoR_expected[0])
        np.testing.assert_array_almost_equal(self.Shomate_direct.get_CpoR(T=T),
                                             CpoR_expected)

    def test_get_Cp(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        Cp_expected = np.array([4.235796744, 4.267598139, 4.300310233,
                                4.333821197, 4.368036178, 4.402873306,
                                4.438260758, 4.474134568, 4.510436977,
                                4.547115164, 4.584120285, 4.621406707,
                                4.658931423, 4.696653576, 4.734534089,
                                4.772535363, 4.810621034, 4.848755777,
                                4.886905141, 4.925035419, 4.963113539,
                                5.001106966, 5.038983636, 5.07671188,
                                5.114260381, 5.151598119, 5.18869434,
                                5.225518516, 5.262040323, 5.298229611,
                                5.334056387, 5.369490794, 5.404503098,
                                5.439063673, 5.47314299, 5.506711603,
                                5.539740144, 5.572199316, 5.604059881,
                                5.635292657, 5.665868512, 5.695758359,
                                5.724933152, 5.753363882, 5.781021572,
                                5.807877279, 5.833902083, 5.859067093,
                                5.883343439])*c.R('J/mol/K')
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_Cp(T=T[0], units='J/mol/K'),
                Cp_expected[0])
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_Cp(T=T, units='J/mol/K'),
                Cp_expected)
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_Cp(T=T[0], units='J/g/K'),
                Cp_expected[0]/self.mw)
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_Cp(T=T, units='J/g/K'),
                Cp_expected/self.mw)

    def test_get_HoRT(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        HoRT_expected = np.array([-56.50439376, -53.61125042, -50.97965343,
                                  -48.57545097, -46.37018744, -44.3399637,
                                  -42.46456033, -40.72675589, -39.11179131,
                                  -37.60694517, -36.20119391, -34.88493792,
                                  -33.64977889, -32.48833779, -31.39410484,
                                  -30.36131539, -29.38484627, -28.46012919,
                                  -27.58307762, -26.75002503, -25.9576724,
                                  -25.20304335, -24.48344574, -23.79643859,
                                  -23.13980357, -22.5115202, -21.90974438,
                                  -21.3327896, -20.77911052, -20.2472886,
                                  -19.73601934, -19.24410116, -18.7704255,
                                  -18.31396799, -17.87378072, -17.44898523,
                                  -17.03876635, -16.64236662, -16.25908132,
                                  -15.88825401, -15.52927251, -15.18156522,
                                  -14.84459794, -14.5178708, -14.20091565,
                                  -13.89329361, -13.59459279, -13.30442637,
                                  -13.02243068])
        np.testing.assert_almost_equal(self.Shomate_direct.get_HoRT(T=T[0]),
                                       HoRT_expected[0])
        np.testing.assert_array_almost_equal(self.Shomate_direct.get_HoRT(T=T),
                                             HoRT_expected)

    def test_get_H(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        H_expected = np.array([-56.50439376, -53.61125042, -50.97965343,
                               -48.57545097, -46.37018744, -44.3399637,
                               -42.46456033, -40.72675589, -39.11179131,
                               -37.60694517, -36.20119391, -34.88493792,
                               -33.64977889, -32.48833779, -31.39410484,
                               -30.36131539, -29.38484627, -28.46012919,
                               -27.58307762, -26.75002503, -25.9576724,
                               -25.20304335, -24.48344574, -23.79643859,
                               -23.13980357, -22.5115202, -21.90974438,
                               -21.3327896, -20.77911052, -20.2472886,
                               -19.73601934, -19.24410116, -18.7704255,
                               -18.31396799, -17.87378072, -17.44898523,
                               -17.03876635, -16.64236662, -16.25908132,
                               -15.88825401, -15.52927251, -15.18156522,
                               -14.84459794, -14.5178708, -14.20091565,
                               -13.89329361, -13.59459279, -13.30442637,
                               -13.02243068])*c.R('J/mol/K')*T
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_H(T=T[0], units='J/mol'),
                H_expected[0], decimal=4)
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_H(T=T, units='J/mol'),
                H_expected, decimal=4)
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_H(T=T[0], units='J/g'),
                H_expected[0]/self.mw, decimal=4)
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_H(T=T, units='J/g'),
                H_expected/self.mw, decimal=4)

    def test_get_SoR(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        SoR_expected = np.array([24.84034743, 25.04777818, 25.24705859,
                                 25.43895148, 25.62411782, 25.803134,
                                 25.97650557, 26.14467824, 26.30804687,
                                 26.46696281, 26.62173993, 26.77265968,
                                 26.91997528, 27.06391529, 27.20468657,
                                 27.34247693, 27.47745721, 27.60978326,
                                 27.73959751, 27.86703041, 27.99220165,
                                 28.11522125, 28.23619048, 28.35520273,
                                 28.47234423, 28.58769466, 28.7013278,
                                 28.81331199, 28.92371063, 29.03258257,
                                 29.13998246, 29.24596116, 29.35056593,
                                 29.45384082, 29.5558268, 29.6565621,
                                 29.75608232, 29.85442065, 29.95160805,
                                 30.04767338, 30.14264358, 30.23654374,
                                 30.32939729, 30.42122603, 30.5120503,
                                 30.60188904, 30.69075988, 30.77867922,
                                 30.8656623])
        np.testing.assert_almost_equal(self.Shomate_direct.get_SoR(T=T[0]),
                                       SoR_expected[0])
        np.testing.assert_array_almost_equal(self.Shomate_direct.get_SoR(T=T),
                                             SoR_expected)

    def test_get_S(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        S_expected = np.array([24.84034743, 25.04777818, 25.24705859,
                               25.43895148, 25.62411782, 25.803134,
                               25.97650557, 26.14467824, 26.30804687,
                               26.46696281, 26.62173993, 26.77265968,
                               26.91997528, 27.06391529, 27.20468657,
                               27.34247693, 27.47745721, 27.60978326,
                               27.73959751, 27.86703041, 27.99220165,
                               28.11522125, 28.23619048, 28.35520273,
                               28.47234423, 28.58769466, 28.7013278,
                               28.81331199, 28.92371063, 29.03258257,
                               29.13998246, 29.24596116, 29.35056593,
                               29.45384082, 29.5558268, 29.6565621,
                               29.75608232, 29.85442065, 29.95160805,
                               30.04767338, 30.14264358, 30.23654374,
                               30.32939729, 30.42122603, 30.5120503,
                               30.60188904, 30.69075988, 30.77867922,
                               30.8656623])*c.R('J/mol/K')
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_S(T=T[0], units='J/mol/K'),
                S_expected[0])
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_S(T=T, units='J/mol/K'),
                S_expected)
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_S(T=T[0], units='J/g/K'),
                S_expected[0]/self.mw)
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_S(T=T, units='J/g/K'),
                S_expected/self.mw)

    def test_get_GoRT(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        GoRT_expected = np.array([-81.34474118, -78.6590286,
                                  -76.22671203, -74.01440245, -71.99430526,
                                  -70.14309771, -68.4410659, -66.87143413,
                                  -65.41983818, -64.07390798, -62.82293385,
                                  -61.6575976, -60.56975418, -59.55225307,
                                  -58.59879142, -57.70379231, -56.86230349,
                                  -56.06991246, -55.32267513, -54.61705544,
                                  -53.94987405, -53.31826459, -52.71963622,
                                  -52.15164133, -51.6121478, -51.09921486,
                                  -50.61107217, -50.14610159, -49.70282116,
                                  -49.27987116, -48.8760018, -48.49006232,
                                  -48.12099143, -47.76780881, -47.42960753,
                                  -47.10554734, -46.79484867, -46.49678727,
                                  -46.21068937, -45.9359274, -45.67191608,
                                  -45.41810897, -45.17399522, -44.93909682,
                                  -44.71296595, -44.49518265, -44.28535267,
                                  -44.08310559, -43.88809298])
        np.testing.assert_almost_equal(self.Shomate_direct.get_GoRT(T=T[0]),
                                       GoRT_expected[0])
        np.testing.assert_array_almost_equal(self.Shomate_direct.get_GoRT(T=T),
                                             GoRT_expected)

    def test_get_G(self):
        T = np.array([500., 525., 550., 575., 600., 625., 650., 675., 700.,
                      725., 750., 775., 800., 825., 850., 875., 900., 925.,
                      950., 975., 1000., 1025., 1050., 1075., 1100., 1125.,
                      1150., 1175., 1200., 1225., 1250., 1275., 1300., 1325.,
                      1350., 1375., 1400., 1425., 1450., 1475., 1500., 1525.,
                      1550., 1575., 1600., 1625., 1650., 1675., 1700.])
        G_expected = np.array([-81.34474118, -78.6590286,
                               -76.22671203, -74.01440245, -71.99430526,
                               -70.14309771, -68.4410659, -66.87143413,
                               -65.41983818, -64.07390798, -62.82293385,
                               -61.6575976, -60.56975418, -59.55225307,
                               -58.59879142, -57.70379231, -56.86230349,
                               -56.06991246, -55.32267513, -54.61705544,
                               -53.94987405, -53.31826459, -52.71963622,
                               -52.15164133, -51.6121478, -51.09921486,
                               -50.61107217, -50.14610159, -49.70282116,
                               -49.27987116, -48.8760018, -48.49006232,
                               -48.12099143, -47.76780881, -47.42960753,
                               -47.10554734, -46.79484867, -46.49678727,
                               -46.21068937, -45.9359274, -45.67191608,
                               -45.41810897, -45.17399522, -44.93909682,
                               -44.71296595, -44.49518265, -44.28535267,
                               -44.08310559, -43.88809298])*c.R('J/mol/K')*T
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_G(T=T[0], units='J/mol'),
                G_expected[0], decimal=4)
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_G(T=T, units='J/mol'),
                G_expected, decimal=4)
        np.testing.assert_almost_equal(
                self.Shomate_direct.get_G(T=T[0], units='J/g'),
                G_expected[0]/self.mw, decimal=4)
        np.testing.assert_array_almost_equal(
                self.Shomate_direct.get_G(T=T, units='J/g'),
                G_expected/self.mw, decimal=4)

    def test_to_dict(self):
        self.maxDiff = None
        self.assertEqual(self.Shomate_direct.to_dict(),
                         self.Shomate_direct_dict)

    def test_from_dict(self):
        self.assertEqual(Shomate.from_dict(self.Shomate_direct_dict),
                         self.Shomate_direct)


if __name__ == '__main__':
    unittest.main()