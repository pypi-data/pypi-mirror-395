# import math, collections
# import numpy as np


# def sgd_update(param, grad, lr=0.01):
#     param = np.array(param, dtype=float)
#     grad = np.array(grad, dtype=float)
#     return param - lr * grad


# def momentum_update(param, grad, velocity, lr=0.01, momentum=0.9):
#     v_new = momentum * velocity + lr * grad
#     return param - v_new, v_new


# def adam_update(param, grad, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
#     # returns (param_new, m_new, v_new)
#     m_new = beta1 * m + (1 - beta1) * grad
#     v_new = beta2 * v + (1 - beta2) * (grad * grad)
#     m_hat = m_new / (1 - beta1**t)
#     v_hat = v_new / (1 - beta2**t)
#     param_new = param - lr * m_hat / (math.sqrt(v_hat) + eps)
#     return param_new, m_new, v_new


# def rmsprop_update(param, grad, s, lr=0.001, beta=0.9, eps=1e-8):
#     s_new = beta * s + (1 - beta) * (grad * grad)
#     param_new = param - lr * grad / (math.sqrt(s_new) + eps)
#     return param_new, s_new


# def lr_step_decay(base_lr, epoch, step_size=10, gamma=0.1):
#     return base_lr * (gamma ** (epoch // step_size))


# def lr_cosine_anneal(base_lr, epoch, max_epoch):
#     return base_lr * 0.5 * (1 + math.cos(math.pi * epoch / max_epoch))


import numpy as np
import math

def sgd_update(param, grad, lr=0.01):
    param = np.array(param, dtype=float)
    grad = np.array(grad, dtype=float)
    return param - lr * grad

def momentum_update(param, grad, velocity, lr=0.01, momentum=0.9):
    param = np.array(param, dtype=float)
    grad = np.array(grad, dtype=float)
    velocity = np.array(velocity, dtype=float)
    v_new = momentum * velocity + lr * grad
    return param - v_new, v_new

def adam_update(param, grad, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
    param = np.array(param, dtype=float)
    grad = np.array(grad, dtype=float)
    m = np.array(m, dtype=float)
    v = np.array(v, dtype=float)
    m_new = beta1 * m + (1 - beta1) * grad
    v_new = beta2 * v + (1 - beta2) * (grad * grad)
    m_hat = m_new / (1 - beta1**t)
    v_hat = v_new / (1 - beta2**t)
    param_new = param - lr * m_hat / (np.sqrt(v_hat) + eps)
    return param_new, m_new, v_new

def rmsprop_update(param, grad, s, lr=0.001, beta=0.9, eps=1e-8):
    # Convert to arrays
    param = np.array(param, dtype=float)
    grad  = np.array(grad,  dtype=float)
    s     = np.array(s,     dtype=float)

    # Update running average of squared gradients
    s_new = beta * s + (1 - beta) * (grad * grad)

    # Parameter update
    param_new = param - lr * grad / (np.sqrt(s_new) + eps)
    return param_new, s_new

def lr_step_decay(base_lr, epoch, step_size=10, gamma=0.1):
    """Step decay learning rate schedule."""
    return base_lr * (gamma ** (epoch // step_size))

def lr_cosine_anneal(base_lr, epoch, max_epoch):
    """Cosine annealing learning rate schedule."""
    return base_lr * 0.5 * (1 + math.cos(math.pi * epoch / max_epoch))