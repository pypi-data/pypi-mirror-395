
import os
from pathlib import Path
from os.path import isfile

def check_server(url):
    """Return True if the given URL can be opened, False otherwise.

        This is a small helper used to test model download endpoints before
        actually attempting to retrieve files.
    """
    from urllib.request import urlopen
    try:
        u = urlopen(url)
        u.close()
        return True
    except:
        return False
def download_url_to_file(url, dst, progress=True):
    """Download the object at ``url`` to the local path ``dst``.

    Parameters
    ----------
    url : str
        Source URL.
    dst : str or path-like
        Destination file path on the local filesystem.
    progress : bool, optional
        If ``True``, a simple textual progress indicator may be printed.

    Notes
    -----
    This function streams the response to disk in chunks to avoid
    loading large files into memory.
    """
    #print(f"download {url}")
    if not check_server(url): return False
    from urllib.request import urlopen
    import tempfile,shutil,ssl
    from tqdm import tqdm
    file_size = None
    ssl._create_default_https_context = ssl._create_unverified_context
    u = urlopen(url)
    meta = u.info()
    if hasattr(meta, "getheaders"):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    # We deliberately save it in a temp file and move it after
    dst = os.path.expanduser(dst)
    dst_dir = os.path.dirname(dst)
    f = tempfile.NamedTemporaryFile(delete=False, dir=dst_dir)
    try:
        with tqdm(total=file_size, disable=not progress, unit="B", unit_scale=True,  unit_divisor=1024) as pbar:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                pbar.update(len(buffer))
        f.close()
        shutil.move(f.name, dst)
    finally:
        f.close()
        if os.path.exists(f.name):
            os.remove(f.name)

def read_epochs(filename):
    """Read an integer "epoch" value from a small text file.

        The epochs file is used to detect whether a new version of the model
        is available on the server.
    """
    if not isfile(filename): return None
    try:
        with open(filename, "r") as f:
            for line in f:
                return  int(line.strip())
    except :
        print(f"Error reading {filename}")
    return None
def cache_model_path(model_type,net_size,mode):
    """Return the local path to the cached model file, downloading if needed.

        This function builds a cache directory under the user home, checks
        for the presence of the requested model, and if necessary:

        - downloads the latest ``.epochs`` file,
        - compares local and remote epochs,
        - downloads the corresponding ``.h5`` model file.

        Parameters
        ----------
        model_name : str
            Identifier for the family of models (e.g. "ALL-all").
        net_size : int
            Network patch size (e.g. 128 or 256).
        mode : {"2D", "3D"}
            Dimensionality of the model.

        Returns
        -------
        str
            Path to the local ``.h5`` model file.
    """
    ...
    import os
    from appdirs import user_data_dir
    MODEL_DIR = Path(user_data_dir("MorphoDeep"))
    os.makedirs(MODEL_DIR, exist_ok=True)
    if mode=="2D" and net_size==128:net_size=256 #No train model in 128
    filename=model_type+f"_FusedToSemantic_JUNNET_{mode}_{net_size}"
    MODEL_URL="https://morphonet.org/MODELS/"+filename
    model_file = os.fspath(MODEL_DIR / str(filename+".h5"))
    epochs_file = os.fspath(MODEL_DIR / str(filename+".epochs"))
    retrieve=True
    #Local Epochs
    current_epochs = read_epochs(epochs_file)

    #Distante Epochs
    download_url_to_file(MODEL_URL+".epochs", epochs_file, progress=False)
    distant_epochs=read_epochs(epochs_file)
    if current_epochs is not None:
        if distant_epochs==current_epochs:
            retrieve=False
        else:
            print(f" --> a new version is available at epochs {distant_epochs}")

    if retrieve or not isfile(model_file):
        print(f'Downloading:  {model_file}')
        download_url_to_file(MODEL_URL+".h5", model_file, progress=True)
    return model_file