import io

import h5py
import numpy as np

from scidatacontainer import AbstractFile, register


class Hdf5File(AbstractFile):
    def encode(self):
        with io.BytesIO() as fp:
            with h5py.File(fp, "w") as array:
                array.create_dataset(
                    "dataset", data=self.data, compression="gzip", compression_opts=9
                )
            fp.seek(0)
            data = fp.read()
        return data

    def decode(self, data):
        with io.BytesIO(data) as fp:
            with h5py.File(fp, "r") as array:
                self.data = array["dataset"][()]


register = [("hdf5", Hdf5File, np.ndarray)]
