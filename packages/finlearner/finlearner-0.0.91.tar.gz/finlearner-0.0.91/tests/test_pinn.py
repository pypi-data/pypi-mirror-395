import pytest
import tensorflow as tf
import numpy as np
from finlearner.pinn import BlackScholesPINN

def test_pinn_structure():
    model = BlackScholesPINN(r=0.05, sigma=0.2)
    
    # Create dummy input: batch of 5 points (t, S)
    t = np.random.rand(5)
    S = np.random.rand(5) * 100
    inputs = tf.stack([t, S], axis=1)
    
    # Run forward pass
    output = model(inputs)
    
    # Check shape (should be 5 outputs, 1 value each)
    assert output.shape == (5, 1)

def test_pinn_physics_loss():
    model = BlackScholesPINN()
    t = tf.constant([0.5], dtype=tf.float32)
    S = tf.constant([100.0], dtype=tf.float32)
    
    # Check if we can calculate the PDE residual
    residual = model.get_pde_residual(t, S)
    assert residual is not None