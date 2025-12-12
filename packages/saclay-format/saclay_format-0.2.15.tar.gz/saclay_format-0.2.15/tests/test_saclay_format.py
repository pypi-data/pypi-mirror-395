import unittest
import numpy as np
import os
import shutil
from saclay_format import saclay_parser as parser


class TestParser(unittest.TestCase):

    def setUp(self):
        """Create a temporary working directory."""
        self.tmpdir = "tmp_test_parser"
        os.makedirs(self.tmpdir, exist_ok=True)

    def tearDown(self):
        """Remove temporary directory after each test."""
        shutil.rmtree(self.tmpdir)

    # ----------------------------------------------------------
    def create_dummy_rho(self, shape):
        nx, ny, nz = shape
        x = np.arange(nx)
        y = np.arange(ny)
        z = np.arange(nz)
        z, y, x = np.meshgrid(z, y, x, indexing="ij")
        # actuellement field = (nz, ny, nx)
        field = (x + 2*y + 3*z).astype(np.float64)

        # convertir en (nx, ny, nz), ordre attendu par le parser
        return np.transpose(field, (2, 1, 0))

    # ----------------------------------------------------------
    def create_dummy_data(self):
        nx, ny, nz = 6, 7, 8
        nw_n, nw_p = 5, 4

        data = {
            "metadata": {
                "nx": nx, "ny": ny, "nz": nz,
                "dx": 0.9, "dy": 0.8, "dz": 0.7,
                "prefix": "dummy",
                "description": "dummy data",
                "Z": 10, "N": 12,
                "frame": 1,
                "t0": 0., "dt": 0.,
            }
        }

        # -------------------- fields --------------------
        rho_n = {
            "name": "rho_n",
            "n_components": 1,
            "type": "real",
            "unit": "fm^-3",
            "suffix": "_rho_n.bin"
        }
        j = {
            "name": "j",
            "n_components": 3,
            "type": "real",
            "unit": "arb",
            "suffix": "_j.bin"
        }

        data["metadata"]["field"] = [rho_n, j]
        data["rho_n"] = self.create_dummy_rho((nx, ny, nz))
        data["j"] = np.random.rand(nx, ny, nz, 3).astype(np.float64, order="F")

        # ---------------- wavefunctions ----------------
        wf = {
            "representation": "canonical",
            "n_neutron_states": nw_n,
            "n_proton_states": nw_p,
            "suffix": "_state"
        }
        data["metadata"]["wavefunction"] = wf

        data["statesn"] = np.random.rand(nx, ny, nz, 2, nw_n).astype(np.complex128, order="F")
        data["statesp"] = np.random.rand(nx, ny, nz, 2, nw_p).astype(np.complex128, order="F")
        data["un"] = np.random.rand(nw_n).astype(np.complex128)
        data["vn"] = np.random.rand(nw_n).astype(np.complex128)
        data["up"] = np.random.rand(nw_p).astype(np.complex128)
        data["vp"] = np.random.rand(nw_p).astype(np.complex128)

        return data

    # ----------------------------------------------------------
    def test_yaml_write_read(self):
        data = self.create_dummy_data()



        yamlfile = os.path.join(self.tmpdir, "dummy.yaml")
        parser.write(data, yamlfile)

        read_data = parser.read(yamlfile)

        # version
        self.assertEqual(read_data["metadata"]["version"], parser.PARSER_VERSION)

        # fields
        self.assertLess(np.linalg.norm(read_data["rho_n"] - data["rho_n"]), 1e-15)
        self.assertLess(np.linalg.norm(read_data["j"] - data["j"]), 1e-15)

        # wavefunctions
        for key in ["statesn", "statesp", "un", "vn", "up", "vp"]:
            self.assertLess(np.linalg.norm(read_data[key] - data[key]), 1e-15)

    # ----------------------------------------------------------
    def test_hdf5_write_read(self):
        data = self.create_dummy_data()

        h5file = os.path.join(self.tmpdir, "dummy.h5")
        parser.write(data, h5file)

        read_data = parser.read(h5file)

        # version
        self.assertEqual(read_data["metadata"]["version"], parser.PARSER_VERSION)

        # fields
        self.assertLess(np.linalg.norm(read_data["rho_n"] - data["rho_n"]), 1e-15)
        self.assertLess(np.linalg.norm(read_data["j"] - data["j"]), 1e-15)

        # wavefunctions
        for key in ["statesn", "statesp", "un", "vn", "up", "vp"]:
            self.assertLess(np.linalg.norm(read_data[key] - data[key]), 1e-15)


if __name__ == "__main__":
    unittest.main()
