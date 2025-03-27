import numpy as np
from scipy.spatial.transform import Rotation as R

class Force:

    def __init__(self, F:tuple, r:tuple=None, T:tuple=None):
        # two three component vectors: 
        #   one for the #D position of the vector, 
        #   one for the magnitude and direction of the force
        self.F = np.array(F)

        if r is None:
            self.set_torque(T)
            self.r = np.zeros(3)
        else:
            self.get_torque(r)

    def convert_coords(self, S:dict):
        """
        Rotates a vector using the current quaternion.
        """
        q = S['q']

        self.r = R.from_quat(q).as_matrix() @ self.r
        self.F = R.from_quat(q).as_matrix() @ self.F
        self.T = R.from_quat(q).as_matrix() @ self.T

    def get_torque(self, r):

        if np.array_equal(self.F, np.zeros(3)):
            return np.zeros(3)

        d = self.r + ((np.dot(r, self.F) / np.dot(self.F, self.F)) * self.F)
            # finds the lever arm by which the force is applied to create the torque

        T = np.cross(d, self.F)
            # cross products the lever arm with the force

        self.T = T
    
    def set_torque(self, T):
        self.T = T