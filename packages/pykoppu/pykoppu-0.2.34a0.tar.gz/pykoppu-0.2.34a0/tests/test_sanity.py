"""
Sanity Test for KOPPU.

Tests the basic physics and compilation pipeline.
"""

import unittest
import numpy as np
import networkx as nx
from pykoppu.opu.device import OPU
from pykoppu.problems.graph.maxcut import MaxCut
from pykoppu.biocompiler.compiler import BioCompiler
from pykoppu.biocompiler.isa import OpCode

class TestKoppuSanity(unittest.TestCase):
    
    def test_opu_specs(self):
        """Test if OPU loads correct physical specifications."""
        opu = OPU(model="lif_critical")
        specs = opu.specs
        
        # Check critical regime parameters
        self.assertAlmostEqual(specs.R, 50e6)
        self.assertAlmostEqual(specs.tau, 20e-3)
        self.assertAlmostEqual(specs.I_offset, 0.36e-9)
        self.assertAlmostEqual(specs.sigma, 2.0e-3)
        
    def test_maxcut_hamiltonian(self):
        """Test MaxCut to Hamiltonian conversion."""
        # Simple triangle graph
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (2, 0)])
        
        problem = MaxCut(G)
        
        # J should be related to adjacency
        # J_ij = -w_ij * scale
        # w_ij = 1
        # J should be negative
        
        self.assertTrue(np.all(problem.J <= 0))
        self.assertEqual(problem.J.shape, (3, 3))
        
        # Check symmetry
        self.assertTrue(np.allclose(problem.J, problem.J.T))
        
    def test_compiler_annealing(self):
        """Test if compiler generates annealing schedule."""
        G = nx.Graph()
        G.add_node(0)
        problem = MaxCut(G)
        
        compiler = BioCompiler()
        instructions = compiler.compile(problem, strategy="annealing")
        
        # Check for SIG instructions
        sig_ops = [instr for instr in instructions if instr.opcode == OpCode.SIG]
        self.assertGreaterEqual(len(sig_ops), 3)
        
        # Check if noise decreases
        noises = [instr.operands[0] for instr in sig_ops]
        self.assertTrue(noises[0] > noises[-1])

if __name__ == '__main__':
    unittest.main()
