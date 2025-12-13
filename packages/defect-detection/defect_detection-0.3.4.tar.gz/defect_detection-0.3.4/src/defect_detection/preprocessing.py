########################################################################################
## Define a generic preprocessing function for input images.                          ##
## Includes data augmentation and image spliting.                                     ##
## This function can be used to generate a training dataset for a new model.          ##
########################################################################################


import numpy as np
import cv2 as cv
import torch
import os
from pathlib import Path
import concurrent.futures as thd


def generate_dataset(
    spath="source",
    Flist="list.txt",
    fcrop=None,
    Naug=5,
    offset=25,
    da=0.20,
    db=0.20,
    dw=15,
    Nseg=8,
    size=512,
    opath="data/",
    name="data",
    opref="img",
    Ncore="10",
    seed=666,
):
    """
    Generates a dataset from a list of source images.
    The images ondergo data augmentation and spliting into square tiles.

    Arguments:
        spath : (Path or str)
            Path containing the source images.

        Flist : (Path or str)
            File containing the list of source image files to be processed.

        fcrop : (Path or str or None)
            File containing the initial croping information to be applied on source images.
            If not specifyied, no initial croping is applied.
            *Optional*

        Naug : (int)
            Number of source image duplicate generated during augmentation.

        offset : (int)
            Maximal random cropping offset applied durring augmentation (in pixel).

        da : (float)
            Maximal random luminosity variation applied durring augmentation.

        db : (float)
            Maximal random contrast variation applied durring augmentation.

        dw : (int)
            Random crop scale variation applied durring augmentation (in pixel).

        Nseg : (int)
            Number of vertical and horizontal split applied for image splitting.

        size : (int)
            Size in pixel of the generated image tiles.
            The source image is resized to fit the required size before splitting.

        opath : (Path or str)
            Path where the dataset is generated

        name : (str)
            Name of the dataset.
            Can be used ad ID when working with different dataset.

        opref : (str)
            Prefix used for naming the generated images.

        Ncore : (int)
            Number of CPU core to use for parallelizing the image generation.

        seed : (int)
            The seed to be used for numpy random generator (ensure reproducibility).
    """
    np.random.seed(seed)

    # Save preprocessing option in a file
    param = {
        "spath": spath,
        "Flist": Flist,
        "fcrop": fcrop,
        "Naug": Naug,
        "offset": offset,
        "da": da,
        "db": db,
        "dw": dw,
        "Nseg": Nseg,
        "size": size,
        "opath": opath,
        "name": name,
        "opref": opref,
        "Ncore": Ncore,
        "seed": seed,
    }
    with Path.open(Path(param["opath"] + param["name"] + ".txt"), "w") as f:
        print(param, file=f)

    print("Preprocessing parameters :")
    for k, i in param.items():
        print(f"\t{k} : {i}")

    # Load initial croping if needed
    if param["fcrop"] is not None:
        with Path.open(Path(param["fcrop"]), "r") as f:
            cr = eval(f.read())
    else:
        cr = None

    # Check if output path directory exists
    opath = param["opath"] + param["name"] + "/"
    if not os.path.exists(opath):
        os.mkdir(opath, 0o755)

    # Get the image list from file
    fl = []
    with Path.open(Path(param["Flist"])) as f:
        for li in f.readlines():
            if li[0] == "#":
                continue
            else:
                fl.append(li.strip())
    print(f"{len(fl)} images to process")

    # Load temporarly the first image to get shapes
    img = cv.imread(param["spath"] + fl[0])
    sxi, syi = img.shape[0], img.shape[1]
    del img

    # Initialize the augmented dataset container
    if cr:
        # Compute margin accounting for croping and offset
        xmin = max(cr[0], param["offset"] + param["dw"])
        xmax = min(sxi + cr[1], sxi - param["offset"] - param["dw"])
        ymin = max(cr[2], param["offset"] + param["dw"])
        ymax = min(syi + cr[3], syi - param["offset"] - param["dw"])
    else:
        # Compute margin accounting for offset only
        xmin = param["offset"] + param["dw"]
        xmax = sxi - param["offset"] - param["dw"]
        ymin = param["offset"] + param["dw"]
        ymax = syi - param["offset"] - param["dw"]

    print(
        f"Image shape before segmentation : ({xmax - xmin}, {ymax - ymin}) (+-{2*param['dw']})"
    )

    # Function to process one image (augmentation+segmentation)
    # To be parallelized.
    def process_img(i):
        np.random.seed(seed * i)

        # Compute segment edges
        sx = np.linspace(0, param["size"] * param["Nseg"], param["Nseg"] + 1, dtype=int)
        sy = np.linspace(0, param["size"] * param["Nseg"], param["Nseg"] + 1, dtype=int)

        # Augmentation loop
        for a in range(param["Naug"]):
            # Set random offset for position, brightness and contrast
            offset = np.random.randint(-param["offset"], param["offset"])
            da = np.random.uniform(1 - param["da"], 1 + param["da"])
            db = np.random.uniform(-param["db"], param["db"])
            dw = np.random.randint(0, param["dw"])

            # Read image in the croped/translated range
            img = cv.imread(param["spath"] + fl[i])[
                xmin + offset - dw : xmax + offset + dw,
                ymin + offset - dw : ymax + offset + dw,
            ]

            # Resize image so that it fits with segmentation
            img = cv.resize(
                img, (param["size"] * param["Nseg"], param["size"] * param["Nseg"])
            )

            # Apply brightness transformation
            img = da * img + db

            # Segmentation loop
            iid = param["Naug"] * i + a
            for si in range(sx.size - 1):
                for sj in range(sy.size - 1):
                    cv.imwrite(
                        opath + param["opref"] + f"_{iid}_x{si+1}y{sj+1}.jpg",
                        img[sx[si] : sx[si + 1], sy[sj] : sy[sj + 1]],
                    )

        # Free memmory
        del img
        del sx
        del sy

        return

    # Inintialize process pool for parallelization
    print("####PROCESSING IMAGES####")
    with thd.ProcessPoolExecutor(max_workers=param["Ncore"]) as exe:
        # Image loop
        for i in range(len(fl)):
            # Submit image process to the pool
            exe.submit(process_img, i)

    print("DONE")

    return


# Function to convert one numpy image torch tensor format
def get_tensor(im, dev="auto"):
    """
    Get a numpy image and convert it in torch tensor type.
    Also handles selection of device to be used by torch.

    Arguments :
        im : (numpy array)
            The image in numpy array format.
        dev : (str)
            Define the device that torch should use to handle the tensor.
            Support 'CPU', 'cuda' and 'auto'.
    """
    # Device automatic selection (if needed)
    if dev == "auto":
        # Check for CUDA availability
        if torch.cuda.is_available():
            dev = "cuda"
        else:
            dev = "cpu"

    # Type conversion (to float image)
    im = im.astype(np.float32)
    im = im / 255.0

    # Axis reordering (2->0)
    im = np.moveaxis(im, 2, 0)

    # Conversion to torch tensor and load in device
    im = torch.from_numpy(im).to(dev)

    return im
