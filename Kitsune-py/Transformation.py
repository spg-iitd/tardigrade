"""
    This file contains the Transformation class, which is uses to perform transformation on the feature vector before it is passed to the autoencoder.
    Different types of transformations are supported:
        0. No Transformation
        1. Key based permuation
        2. Key based encryption
"""
import random
import string
import numpy as np

def generate_key(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits +  string.ascii_lowercase) for _ in range(size))

class Transformation:
    def __init__(self, tf_type, key):
        self.tf_type = tf_type
        self.key = key
    
    def transform(self, vector):
        if self.tf_type == "0":
            return vector
        elif self.tf_type == "1":
            return self.permute(vector)
        elif self.tf_type == "2":
            return self.encrypt(vector)

    def permute(self, vector):
        """
            Key Based Random Permutation (KBRP)
            Assumption - Length of Key < Length of Feature Vector
        """

        # 1. init
        n = len(vector)
        s = min(len(self.key), n)
        K = [ord(c) for c in self.key]
        P = [i for i in range(1, n+1)]
        A = [0 for i in range(n)]

        for i in range(s):
            A[i] = K[i]
        for i in range(0, s-1):
            P[i] = A[i] + A[i+1] # According to text not pseudocode
        P[s-1] = A[0]
        for i in range(s, n):
            j = s
            while (j>0):
                for k in range(i-s, i):
                    if (j>=n):
                        break
                    P[i] = P[i] + P[k]
                    j -= 1

    
        for i in range(n):
            P[i] = P[i] % n

        # 2. eliminate
        l = 0
        r = n-1
        while (l<r):
            for i in range(l+1, r+1):
                if (P[i] == P[l]):
                    P[i] = 0
            l += 1
            for i in range(r-1, l-1, -1):
                if (P[i] == P[r]):
                    P[i] = 0
            r -= 1


        # 3. fill
        missing = set([i+1 for i in range(len(P))]) - set(P)
        m = len(missing)
        
        l = 0
        r = n-1
        side = 1
        while (len(missing) != 0):
            if side:
                while (l < len(P) and P[l] != 0):
                    l += 1
                if (l == len(P)):
                    break
                P[l] = missing.pop()
                side = 0
            else:
                while (r > 0 and P[r] != 0):
                    r -= 1
                if (r == -1):
                    break
                P[r] = missing.pop()
                side = 1

        # 4. permute vector

        return np.array([vector[i-1] for i in P])

    def encrypt(self, vector):
        return vector


"""
    Test Code
"""


if __name__ == "__main__":
    t = Transformation("1", "hello")
    p = t.permute([i+1 for i in range(0, 30)])

    # check if permutation is valid
    assert len(p) == 30
    assert set(p) == set([i+1 for i in range(0, 30)])


