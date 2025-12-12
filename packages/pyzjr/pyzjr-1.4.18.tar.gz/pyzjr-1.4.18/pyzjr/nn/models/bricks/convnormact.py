import torch.nn as nn
from itertools import repeat
from collections import Iterable
from typing import Sequence

class ConvNormActivation(nn.Sequential):
    def __init__(
            self,
            in_channels: int,
            out_channels: int,
            kernel_size: int,
            stride=1,
            padding=None,
            groups: int=1,
            norm_layer=nn.BatchNorm2d,
            activation_layer=nn.ReLU,
            dilation=1,
            inplace=True,
            bias=None,
            apply_act=True,
            conv_layer=nn.Conv2d,
    ):
        if padding is None:
            if isinstance(kernel_size, int) and isinstance(dilation, int):
                padding = (kernel_size - 1) // 2 * dilation
            else:
                _conv_dim = len(kernel_size) if isinstance(kernel_size, Sequence) else len(dilation)
                kernel_size = self._make_ntuple(kernel_size, _conv_dim)
                dilation = self._make_ntuple(dilation, _conv_dim)
                padding = tuple((kernel_size[i] - 1) // 2 * dilation[i] for i in range(_conv_dim))
        if bias is None:
            bias = norm_layer is None
        self.conv = conv_layer(
            in_channels,
            out_channels,
            kernel_size,
            stride,
            padding,
            dilation=dilation,
            groups=groups,
            bias=bias,
        )
        layers = [self.conv]

        if norm_layer is not None:
            layers.append(norm_layer(out_channels))

        if activation_layer is not None and apply_act:
            params = {} if inplace is None else {"inplace": inplace}
            layers.append(activation_layer(**params))
        super().__init__(*layers)

    def _make_ntuple(x, n: int):
        """
        Make n-tuple from input x. If x is an iterable, then we just convert it to tuple.
        Otherwise, we will make a tuple of length n, all with value of x.
        reference: https://github.com/pytorch/pytorch/blob/master/torch/nn/modules/utils.py#L8

        Args:
            x (Any): input value
            n (int): length of the resulting tuple
        """
        if isinstance(x, Iterable):
            return tuple(x)
        return tuple(repeat(x, n))

    @property
    def in_channels(self):
        return self.conv.in_channels

    @property
    def out_channels(self):
        return self.conv.out_channels

class Conv2dNormActivation(ConvNormActivation):
    """
    Configurable block used for Convolution2d-Normalization-Activation blocks.

    Args:
        in_channels (int): Number of channels in the input image
        out_channels (int): Number of channels produced by the Convolution-Normalization-Activation block
        kernel_size: (int, optional): Size of the convolving kernel. Default: 3
        stride (int, optional): Stride of the convolution. Default: 1
        padding (int, tuple or str, optional): Padding added to all four sides of the input. Default: None, in which case it will be calculated as ``padding = (kernel_size - 1) // 2 * dilation``
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1
        norm_layer (Callable[..., torch.nn.Module], optional): Norm layer that will be stacked on top of the convolution layer. If ``None`` this layer won't be used. Default: ``torch.nn.BatchNorm2d``
        activation_layer (Callable[..., torch.nn.Module], optional): Activation function which will be stacked on top of the normalization layer (if not None), otherwise on top of the conv layer. If ``None`` this layer won't be used. Default: ``torch.nn.ReLU``
        dilation (int): Spacing between kernel elements. Default: 1
        inplace (bool): Parameter for the activation layer, which can optionally do the operation in-place. Default ``True``
        bias (bool, optional): Whether to use bias in the convolution layer. By default, biases are included if ``norm_layer is None``.
    """
    def __init__(
            self,
            in_channels: int,
            out_channels: int,
            kernel_size: int,
            stride = 1,
            padding = None,
            groups: int = 1,
            norm_layer=nn.BatchNorm2d,
            activation_layer=nn.ReLU,
            dilation=1,
            inplace=True,
            bias=None,
            apply_act=True
    ):
        super().__init__(
            in_channels,
            out_channels,
            kernel_size,
            stride,
            padding,
            groups,
            norm_layer,
            activation_layer,
            dilation,
            inplace,
            bias,
            apply_act,
            conv_layer=nn.Conv2d,
        )



class Conv2dNorm(Conv2dNormActivation):
    def __init__(self,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: int,
                 stride=1,
                 padding=None,
                 dilation=1,
                 groups=1,
                 bias=False,
                 norm_layer=nn.BatchNorm2d,
                 **kwargs,):
        super().__init__(in_channels=in_channels,
                         out_channels=out_channels,
                         kernel_size=kernel_size,
                         stride=stride,
                         padding=padding,
                         dilation=dilation,
                         groups=groups,
                         bias=bias,
                         apply_act=False,
                         norm_layer=norm_layer,
                         activation_layer=nn.ReLU(inplace=True),  # ignore, actually not working
                         **kwargs,)

class NormAct(nn.Module):
    def __init__(self,
                 in_channels,
                 norm_layer=nn.BatchNorm2d,
                 activation_layer=nn.ReLU(inplace=True),
                 ):
        super(NormAct, self).__init__()
        self.norm_layer = norm_layer(in_channels)
        self.activation_layer = activation_layer

    def forward(self, x):
        x = self.norm_layer(x)
        x = self.activation_layer(x)
        return x


ConvBNReLU = Conv2dNormActivation
ConvBN = Conv2dNorm
BNReLU = NormAct