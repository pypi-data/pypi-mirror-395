#########################################
# Basic usufull functions for the API. ##
#########################################

import torch
from .deep_AE import AE_cls
from pathlib import Path


# Error map using mean
def emap_mean(x, y):
    return torch.mean(torch.square(x - y), (0)).detach().to("cpu").numpy()


# Error map using sum
def emap_sum(x, y):
    return torch.sum(torch.square(x - y), (0)).detach().to("cpu").numpy()


# Load a trained model
def deepAE_load(path, use_only=True, loss_fn=None, opt=None, opt_param=None):
    """
    Function to load a trained deepAE model.

    Arguments :
        path : (Path or str)
            The path to the directory where the model is stored.
            The folder must contain the hyperparameter file and the trained parameters.

        use_only : (bool)
            Specify if the model is intended for application only.
            If true, the training method cannot be called.
            Default to True.

        loss_fn : (function)
            The loss function used to train the model.
            Ignored if use_only is set to True.

        opt : (torch.optim object)
            The optimizer used to trained the model.
            Ignored if use_only is set to True.

        opt_param : (None or dict)
            The parameters to be passed to the optimizer.
            If None, a empty dict is assumed.
    """
    # Load the model hyperparameter
    with Path.open(Path(path + "AE_config.txt")) as f:
        param = eval(f.read())

    # Initilize the model
    ae = AE_cls(param, use_only, loss_fn, opt, opt_param)

    # Load trained parameters
    if torch.cuda.is_available():
        ae.load_state_dict(torch.load(path + "AE_state.save"))
    else:
        ae.load_state_dict(torch.load(path + "AE_state.save", map_location='cpu'))

    return ae
