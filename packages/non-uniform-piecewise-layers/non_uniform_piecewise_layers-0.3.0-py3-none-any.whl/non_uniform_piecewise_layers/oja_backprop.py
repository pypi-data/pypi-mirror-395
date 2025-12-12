import torch
from torch import nn
from typing import Optional, Callable


def oja_update_linear(weight: torch.Tensor, pre: torch.Tensor, post: torch.Tensor, lr: float, reduce: str = "mean") -> None:
    with torch.no_grad():
        if pre.dim() == 1:
            pre_b = pre.unsqueeze(0)
        else:
            pre_b = pre
        if post.dim() == 1:
            post_b = post.unsqueeze(0)
        else:
            post_b = post
        if reduce == "sum":
            scale = 1.0
        else:
            scale = 1.0 / float(pre_b.shape[0])
        hebb = post_b.t() @ pre_b
        hebb = hebb * scale
        row_scales = (post_b.pow(2).sum(dim=0) * scale).unsqueeze(1)
        weight.add_(lr * (hebb - row_scales * weight))


class OjaLinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True, activation: Optional[Callable[[torch.Tensor], torch.Tensor]] = None):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features, bias=bias)
        self.activation = activation if activation is not None else nn.Identity()
        self._last_pre: Optional[torch.Tensor] = None
        self._last_post: Optional[torch.Tensor] = None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        self._last_pre = x.detach()
        z = self.linear(x)
        y = self.activation(z)
        self._last_post = y.detach()
        return y

    def oja_step(self, lr: float, reduce: str = "mean") -> None:
        if self._last_pre is None or self._last_post is None:
            return
        oja_update_linear(self.linear.weight, self._last_pre, self._last_post, lr, reduce=reduce)

    def zero_oja_buffers(self) -> None:
        self._last_pre = None
        self._last_post = None


def apply_oja(module: nn.Module, lr: float, reduce: str = "mean") -> None:
    for m in module.modules():
        oja_fn = getattr(m, "oja_step", None)
        if callable(oja_fn):
            oja_fn(lr, reduce=reduce)


def zero_oja_buffers(module: nn.Module) -> None:
    for m in module.modules():
        zero_fn = getattr(m, "zero_oja_buffers", None)
        if callable(zero_fn):
            zero_fn()


def oja_backprop_step(model: nn.Module, optimizer: torch.optim.Optimizer, oja_lr: float, reduce: str = "mean", zero_grad: bool = True) -> None:
    optimizer.step()
    apply_oja(model, oja_lr, reduce=reduce)
    zero_oja_buffers(model)
    if zero_grad:
        optimizer.zero_grad(set_to_none=True)
