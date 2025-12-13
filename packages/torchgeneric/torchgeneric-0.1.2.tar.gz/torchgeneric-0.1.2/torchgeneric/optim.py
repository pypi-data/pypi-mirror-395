import torch
from typing import Dict, Any, Iterable, Union  
from torch.optim.optimizer import Optimizer

Params = Union[Iterable[torch.Tensor], Iterable[Dict[str, Any]]]

class CHGD(Optimizer):
    """
    Classical Hamiltonian Gradient Descent
    """
    def __init__(
        self, 
        params: Params, 
        lr: float, 
        beta: float = 0.9, 
        gamma=0.1
    ):
        defaults = dict(lr=lr, beta=beta, gamma=gamma)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            lr = group['lr']
            beta = group['beta'] 
            gamma = group['gamma']

            for param in group['params']:
                if param.grad is None:
                    continue

                grad = param.grad
 
                state = self.state[param]
                if len(state) == 0:
                    state['step'] = 0
                    state['X'] = torch.zeros_like(param)
                    state['Y'] = torch.zeros_like(param)

                state['step'] += 1
                t = state['step']

                X = state['X'] 
                X.mul_(beta).add_(grad, alpha=(1 - beta) / gamma) 
                X_hat = X / (1 - beta**t) 
 
                param.add_(X_hat, value=-lr)
        return loss


class RHGD(Optimizer):
    """
    Relativistic Hamiltonian Gradient Descent
    """
    def __init__(
        self, 
        params: Params, 
        lr: float, 
        betas=(0.9, 0.999), 
        gamma=0.1,
        k=1e-8
    ):
        defaults = dict(lr=lr, betas=betas, k=k, gamma=gamma)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            lr = group['lr']
            beta1, beta2 = group['betas']
            k = group['k'] 
            gamma = group['gamma']

            for param in group['params']:
                if param.grad is None:
                    continue

                grad = param.grad
 
                state = self.state[param]
                if len(state) == 0:
                    state['step'] = 0
                    state['X'] = torch.zeros_like(param)
                    state['Y'] = torch.zeros_like(param)

                state['step'] += 1
                t = state['step']

                X = state['X']
                Y = state['Y']

                eta = (1 - beta2)**2 / gamma**2
                X.mul_(beta1).add_(grad, alpha=(1 - beta1) / gamma)
                Y.addcmul_(grad, grad, value=eta/(beta2**(2*t)))
 
                X_hat = X / (1 - beta1**t)
                Y_hat = Y / (eta * t)
 
                param.addcdiv_(X_hat, (Y_hat + k**2).sqrt(), value=-lr)
        return loss