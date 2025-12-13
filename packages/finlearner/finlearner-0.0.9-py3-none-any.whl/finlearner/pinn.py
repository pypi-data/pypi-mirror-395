import tensorflow as tf
import numpy as np

class BlackScholesPINN(tf.keras.Model):
    """
    Physics-Informed Neural Network (PINN) for solving the Black-Scholes Equation.
    
    PDE: dV/dt + 0.5*sigma^2*S^2*d2V/dS2 + r*S*dV/dS - r*V = 0
    """
    def __init__(self, r=0.05, sigma=0.2):
        super(BlackScholesPINN, self).__init__()
        self.r = r
        self.sigma = sigma
        
        # Simple Dense Network
        self.hidden1 = tf.keras.layers.Dense(50, activation='tanh', dtype='float32')
        self.hidden2 = tf.keras.layers.Dense(50, activation='tanh', dtype='float32')
        self.hidden3 = tf.keras.layers.Dense(50, activation='tanh', dtype='float32')
        self.out = tf.keras.layers.Dense(1, activation=None, dtype='float32')

    def call(self, inputs):
        # inputs: [t, S]
        x = self.hidden1(inputs)
        x = self.hidden2(x)
        x = self.hidden3(x)
        return self.out(x)

    def get_pde_residual(self, t, S):
        """Calculates the residual of the Black-Scholes PDE."""
        with tf.GradientTape(persistent=True) as tape2:
            tape2.watch(t)
            tape2.watch(S)
            with tf.GradientTape(persistent=True) as tape1:
                tape1.watch(t)
                tape1.watch(S)
                
                inputs = tf.stack([t, S], axis=1)
                V = self(inputs)
                
            dV_dt = tape1.gradient(V, t)
            dV_dS = tape1.gradient(V, S)
            
        d2V_dS2 = tape2.gradient(dV_dS, S)
        
        # Black-Scholes PDE Residual
        # Note: We usually solve for Time to Maturity (tau), so dt term might flip sign 
        # depending on formulation. Here we assume forward formulation.
        f = dV_dt + 0.5 * (self.sigma**2) * (S**2) * d2V_dS2 + self.r * S * dV_dS - self.r * V
        return f

    def train_step(self, t_batch, S_batch, V_boundary):
        """Custom training step combining Data Loss + Physics Loss."""
        with tf.GradientTape() as tape:
            # 1. Boundary Loss (Data)
            inputs = tf.stack([t_batch, S_batch], axis=1)
            V_pred = self(inputs)
            loss_data = tf.reduce_mean(tf.square(V_boundary - V_pred))
            
            # 2. Physics Loss (PDE Residual)
            # Sample random points in domain for physics constraint
            t_physics = tf.random.uniform(shape=(100,), minval=0, maxval=1)
            S_physics = tf.random.uniform(shape=(100,), minval=50, maxval=150)
            residual = self.get_pde_residual(t_physics, S_physics)
            loss_physics = tf.reduce_mean(tf.square(residual))
            
            total_loss = loss_data + loss_physics
            
        grads = tape.gradient(total_loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
        return total_loss