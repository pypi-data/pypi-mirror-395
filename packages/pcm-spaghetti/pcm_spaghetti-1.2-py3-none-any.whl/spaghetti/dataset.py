"""
Prepare the datasets for training and inference
"""
import random
from PIL import Image
import os
from torch.utils.data import Dataset


class TrainingDataset(Dataset):
    """
    The dataset class for the SPAGHETTI model training
    args:
        path_1: list of strings, the paths to the images in domain 1
        path_2: list of strings, the paths to the images in domain 2
        transform_1: the transformation for domain 1 images
        transform_2: the transformation for domain 2 images
        num_sample: int, optional, the number of images to sample from each domain
    """
    def __init__(self, path_1: list[str], path_2: list[str],
                 transform_1, transform_2, num_sample=None):
        random.seed(42)
        # domain 1
        domain1_paths = []
        for each in path_1:
            domain1_paths.extend([os.path.join(each, x) for x in os.listdir(each)
                                  if x.endswith((".png", ".jpg", ".jpeg", ".tiff", ".tif"))])
        if num_sample:
            try:
                self.domain1_images = random.sample(domain1_paths, k=num_sample)
            except ValueError:
                self.domain1_images = random.choices(domain1_paths, k=num_sample)
        else:
            self.domain1_images = domain1_paths

        # domain 2
        domain2_paths = []
        for each in path_2:
            domain2_paths.extend([os.path.join(each, x) for x in os.listdir(each)
                                  if x.endswith((".png", ".jpg", ".jpeg", ".tiff", ".tif"))])
        if num_sample:
            try:
                self.domain2_images = random.sample(domain2_paths, k=num_sample)
            except ValueError:
                self.domain2_images = random.choices(domain2_paths, k=num_sample)
        else:
            self.domain2_images = domain2_paths

        # others
        self.length_dataset = max(len(self.domain1_images), len(self.domain2_images))
        self.domain1_len = len(self.domain1_images)
        self.domain2_len = len(self.domain2_images)
        self.transform_1 = transform_1
        self.transform_2 = transform_2
        print("Dataset created with: ", self.length_dataset, " samples")

    def __len__(self):
        return self.length_dataset

    def __getitem__(self, index):
        domain1_img_path = self.domain1_images[index % self.domain1_len]
        domain2_img_path = self.domain2_images[index % self.domain2_len]
        domain1_img = Image.open(domain1_img_path).convert("RGB")
        domain2_img = Image.open(domain2_img_path).convert("RGB")

        domain1_img = self.transform_1(domain1_img)
        domain2_img = self.transform_2(domain2_img)

        return domain1_img, domain2_img
