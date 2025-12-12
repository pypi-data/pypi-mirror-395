# coding: utf-8

import os
import tempfile
import unittest

from nxtomo.application.nxtomo import NXtomo
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import MockNXtomo


class TestMockNXtomo(unittest.TestCase):
    """Test the MockNXtomo file"""

    def test_creation(self):
        folder = tempfile.mkdtemp()
        mock = MockNXtomo(scan_path=folder, n_proj=10, n_ini_proj=10)
        self.assertEqual(
            mock.scan_master_file,
            os.path.join(folder, os.path.basename(folder) + ".h5"),
        )
        tomoScan = NXtomoScan(mock.scan_path, entry=mock.scan_entry)
        self.assertEqual(len(NXtomo.get_valid_entries(mock.scan_master_file)), 1)
        tomoScan.update()
        self.assertEqual(tomoScan.scan_range, 360)
        self.assertEqual(len(tomoScan.projections), 10)
