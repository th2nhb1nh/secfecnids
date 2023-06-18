from functools import partial
from collections import OrderedDict
import torch


class TorchHook:
    """
    Wraps a Pytorch model with methods to easily extract activations at specified layers

    Attributes
    ----------
    activation_dict : dict

    hooked_module_names : list
        Description
    model : TYPE
        Description
    module_dict : TYPE
        Description
    """

    def __init__(self, model, device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')):
        """
        Parameters
        ----------
        model: pytorch model
        """
        self.model = model.to(device).eval()
        self.module_dict = OrderedDict(
            [(name, module) for name, module in model.named_modules() if len(list(module.named_children())) == 0])
        self.activation_dict = {}
        self.hooked_module_names = []  # set()

    def available_modules(self):
        """
        Returns
        -------
        List of available module names and associated modules
        """
        return self.module_dict

    def hook_fn(self, name, module, input, output):
        self.activation_dict[name] = output

    def add_hooks(self, name_list):
        """
        Parameters
        ----------
        name_list : List of module names to hook

        """
        for name in name_list:
            # if name not in self.hooked_module_names:
            self.hooked_module_names.append(name)  ##
            # self.hooked_module_names.union(set(name_list))
            self.module_dict[name].register_forward_hook(partial(self.hook_fn, name))

    def forward(self, x):
        """
        Pass an input through the model

        Parameters
        ----------
        x : Input tensor to predict on

        Returns
        -------
        Model output and dictionary of activations

        Note
        ----
        If no hooks have been added to the model self.activation_dict will be empty
        """
        self.activation_dict = {}
        y = self.model(x)
        return y, self.activation_dict

