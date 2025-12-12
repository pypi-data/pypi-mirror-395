"""
Perform pre-processing on the images using the pre-trained model
"""
import torch
from spaghetti import _spaghetti_modules as sp_modules
import os
from tqdm import tqdm
from torchvision.utils import save_image
import torchvision.transforms.v2 as v2


class Spaghetti():
    """
    The class to perform the inference using the SPAGHETTI model
    """
    def __init__(self, model_path: str):
        """
        Initialize the model
        args:
            model_path: str, the path to the model checkpoint
        """
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        generator = sp_modules.GeneratorResNet(3, 9)
        generator.to(device)
        ckpt = torch.load(model_path, map_location=device)["state_dict"]
        # get only G_AB weights
        ckpt = {k[5:]: v for k, v in ckpt.items() if ("G_AB" in k)}
        generator.load_state_dict(ckpt)
        generator.eval()
        # set attributes
        self.generator = generator
        self.device = device

    @staticmethod
    def _default_transform(img):
        """
        The default transformation to perform on the image
        args:
            img: np.ndarray or PIL.Image or torch.Tensor, the image to perform the transformation
        return:
            torch.Tensor, the transformed image
        """
        transform = [
            v2.ToImage(),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            v2.Resize((256, 256)),
        ]
        return v2.Compose(transform)(img)

    def pre_processing(self, imgs, transform=None):
        """
        Perform the pre-processing on the images
        args:
            imgs: list[PIL.Image or torch.Tensor or numpy.ndarray], the images to perform the pre-processing
            transform: None, "default", or callable, the transformation to perform on the images.
            If None, no transformation is performed. If "default", the default transformation is performed.
        return:
            list[torch.Tensor], the images after the pre-processing
        """
        processed_imgs = []
        for img in imgs:
            if transform == "default":
                transformed = self._default_transform(img)
            elif transform:
                transformed = transform(img)
            else:
                transformed = img
            processed_imgs.append(transformed)
        return processed_imgs

    def inference(self, imgs: list[torch.Tensor], names: list[str], save_path=None):
        """
        Perform the inference on the image
        args:
            img: list[torch.Tensor], the image(s) to perform the inference
            names: list[str], the names of the images
            save_path: str or None. If str, images will be saved to the path to after the transformation
        return:
            list[torch.Tensor], the images after the SPAGHETTI transformaton
        """
        print("Performing Inference...")
        transformed_imgs = []
        if save_path:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
        with torch.no_grad():
            for idx, img in enumerate(tqdm(imgs)):
                img = img.unsqueeze(0).to(self.device)
                transformed = self.generator(img).squeeze(0).cpu()
                # normalize to range [0,1]
                out = torch.clamp(transformed, min=-1, max=1)
                min_val = out.min()
                max_val = out.max()
                out = (out-min_val)/(max(max_val-min_val, 1e-5))
                out = torch.clamp(out, min=0, max=1)  # ensure no overflow
                if save_path:
                    name = os.path.join(save_path, f"transformed_{names[idx]}.png")
                    save_image(out, name, nrow=1, normalize=True, value_range=(-1, 1))
                transformed_imgs.append(out)
        return transformed_imgs
