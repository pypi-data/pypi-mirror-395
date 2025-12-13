import os.path as osp
import unittest as ut
from hotpot.__main__ import main


_parent_dir = osp.dirname(__file__)
class TestCliOptimize(ut.TestCase):
    """ This test block to test `CLI hotpot optimize ...`"""
    def test_next_params(self):
        # cmd = [
        #     'optimize',
        #     'somewhere',
        #     osp.join(_parent_dir, 'output', 'optimize'),
        #     '--examples', 'COF'
        # ]
        # self.assertEqual(main(cmd), 0, "Error terminated for hotpot optimize")
        #
        # cmd = [
        #     'optimize',
        #     'somewhere',
        #     osp.join(_parent_dir, 'output', 'optimize'),
        #     '--examples', 'COF',
        #     '--scatter-map'
        # ]
        # self.assertEqual(main(cmd), 0, "Error terminated for hotpot optimize with `--scatter-map`")

        cmd = [
            'optimize',
            osp.join(_parent_dir, 'inputs', 'inputs251206.xlsx'),
            osp.join(_parent_dir, 'output', 'optimize'),
            '--mesh', '20',
            '-s', 'Conc.:0.1:1.25,Current:5:20,FlowRate:5:30'
            # '--examples', 'COF',
            # '--scatter-map',
            # '--cmap', 'BluesSat'
        ]
        self.assertEqual(main(cmd), 0, "Error terminated for hotpot optimize with `--scatter-map`, `--cmap BluesSat`")


    def test_make_cosmic(self):
        cmd = [
            'optimize',
            osp.join(_parent_dir, 'inputs', 'inputs251206.xlsx'),
            osp.join(_parent_dir, 'output', 'cosmic'),
            '--mesh', '20',
            '-s', 'Conc.:0.1:1.25,Current:5:20,FlowRate:5:30',
            '--plot',
            '--init-index', '5'
            # '--examples', 'COF',
            # '--scatter-map',
            # '--cmap', 'BluesSat'
        ]
        self.assertEqual(main(cmd), 0, "Error terminated for hotpot optimize with `--scatter-map`, `--cmap BluesSat`")