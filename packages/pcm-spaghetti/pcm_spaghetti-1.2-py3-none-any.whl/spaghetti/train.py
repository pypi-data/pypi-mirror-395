"""
Implementation of the Spaghetti model training using PyTorch Lightning
"""
import os
import torch
import torch.nn as nn
import pytorch_lightning as pl
from pytorch_lightning.loggers import CSVLogger
from torchvision.utils import save_image
from torchvision.transforms.v2 import Grayscale
import itertools
from . import _spaghetti_modules as sp_modules
from . import utils


class _Spaghetti(pl.LightningModule):
    """
    Implement the training steps for the SPAGHETTI model
    args:
        save_dir: str, the directory to save the model checkpoints and logs
        batch_size: int, the batch size for the model, default 1
        weights: list of floats, the weights for the loss functions in the order of
        GAN loss, cycle loss, identity loss, and SSIM loss. Default [1.0, 10.0, 5.0, 10.0]
        lr: float, the learning rate for the model, default 0.0002
    """
    def __init__(self, save_dir, batch_size=1, weights=None,
                 lr=0.0005):
        super().__init__()
        self.save_dir = save_dir
        self.automatic_optimization = False
        # model
        self.G_AB = sp_modules.GeneratorResNet(3, 9)
        self.D_B = sp_modules.Discriminator(3)
        self.G_BA = sp_modules.GeneratorResNet(3, 9)
        self.D_A = sp_modules.Discriminator(3)
        # loss
        self.criterion_GAN = nn.MSELoss()
        self.criterion_cycle = nn.L1Loss()
        self.criterion_identity = nn.L1Loss()
        self.criterion_ssim = sp_modules.SSIMLoss()
        self.weights = weights if weights is not None else [1.0, 10.0, 5.0, 10.0]
        # others
        self.batch_size = batch_size
        self.lr = lr

    def calculate_loss_generator(self, res, x1, x2):
        # ground truth
        out_shape = [x1.size(0), 1, x1.size(2)//self.D_A.scale_factor,
                     x1.size(3)//self.D_A.scale_factor]
        valid = torch.ones(out_shape).to(self.device)
        fake_x1, fake_x2, recov_x1, recov_x2, new_x1, new_x2 = res
        # convert to gray scale for ssim calculation
        gray = Grayscale(num_output_channels=3)
        x1_gray = gray(x1)
        x2_gray = gray(x2)
        fake_x1_gray = gray(fake_x1)
        fake_x2_gray = gray(fake_x2)
        new_x1_gray = gray(new_x1)
        new_x2_gray = gray(new_x2)
        loss_GAN = (self.criterion_GAN(self.D_A(fake_x1), valid)
                    + self.criterion_GAN(self.D_B(fake_x2), valid))/2
        loss_cycle = (self.criterion_cycle(recov_x1, x1)
                      + self.criterion_cycle(recov_x2, x2))/2
        loss_identity = (self.criterion_identity(new_x1, x1)
                         + self.criterion_identity(new_x2, x2))/2
        loss_ssim_fake = (self.criterion_ssim(fake_x2_gray, x1_gray)
                          + self.criterion_ssim(fake_x1_gray, x2_gray)) / 2
        loss_ssim_real = (self.criterion_ssim(new_x1_gray, x1_gray)
                          + self.criterion_ssim(new_x2_gray, x2_gray)) / 2
        loss_ssim = (loss_ssim_fake + loss_ssim_real) / 2
        total_loss = (self.weights[0] * loss_GAN + self.weights[1] * loss_cycle
                      + self.weights[2] * loss_identity + self.weights[3] * loss_ssim)
        return total_loss

    def calculate_loss_discriminator(self, dis, x, x_fake):
        out_shape = [x.size(0), 1, x.size(2)//dis.scale_factor,
                     x.size(3)//dis.scale_factor]
        valid = torch.ones(out_shape).to(self.device)
        fake = torch.zeros(out_shape).to(self.device)
        loss_real = self.criterion_GAN(dis(x), valid)
        loss_fake = self.criterion_GAN(dis(x_fake.detach()), fake)
        total_loss = (loss_real + loss_fake) / 2
        return total_loss

    def training_step(self, batch, batch_idx):
        optimizer_G, optimizer_D_A, optimizer_D_B = self.optimizers()
        accumulated_grad_batches = (batch_idx+1) % self.batch_size == 0
        x1, x2 = batch
        # for discriminator
        fake_x1 = self.G_BA(x2)
        fake_x2 = self.G_AB(x1)

        # for identity
        new_x1 = self.G_BA(x1)
        new_x2 = self.G_AB(x2)

        # for reconstruction
        recov_x2 = self.G_AB(fake_x1)
        recov_x1 = self.G_BA(fake_x2)

        res = (fake_x1, fake_x2, recov_x1, recov_x2, new_x1, new_x2)

        # generator loss
        gen_loss = self.calculate_loss_generator(res, x1, x2)

        # discriminator A loss
        d_a_loss = self.calculate_loss_discriminator(self.D_A, x1, fake_x1)

        # discriminator B loss
        d_b_loss = self.calculate_loss_discriminator(self.D_B, x2, fake_x2)

        # optimize
        total_loss = gen_loss + d_a_loss + d_b_loss
        self.manual_backward(total_loss)

        if accumulated_grad_batches:
            optimizer_G.step()
            optimizer_G.zero_grad()
            optimizer_D_B.step()
            optimizer_D_B.zero_grad()
            optimizer_D_A.step()
            optimizer_D_A.zero_grad()

        metrics = {'train_gen_loss': gen_loss, 'train_D_A_loss': d_a_loss, 'train_D_B_loss': d_b_loss}
        self.log_dict(metrics, prog_bar=True)

    def validation_step(self, batch, batch_idx):
        x1, x2 = batch
        fake_x1 = self.G_BA(x2)
        fake_x2 = self.G_AB(x1)

        # for identity
        new_x1 = self.G_BA(x1)
        new_x2 = self.G_AB(x2)

        # for reconstruction
        recov_x2 = self.G_AB(fake_x1)
        recov_x1 = self.G_BA(fake_x2)

        res = (fake_x1, fake_x2, recov_x1, recov_x2, new_x1, new_x2)

        loss = self.calculate_loss_generator(res, x1, x2)
        self.log_dict({'val_gen_loss': loss}, sync_dist=True, prog_bar=True)
        # save image for visualization
        visual = torch.cat((x1, fake_x2, x2, fake_x1), 0)
        if batch_idx % 1000 == 0:
            try:
                save_image(
                    visual,
                    os.path.join(
                        self.save_dir, "visual",
                        f"visual_rank_{str(self.global_rank)}_batch_{batch_idx}_epoch_{self.current_epoch}.png"
                    ),
                    nrow=4, normalize=True, value_range=(-1, 1)
                )
            except FileExistsError:
                pass

    def configure_optimizers(self):
        optimizer_G = torch.optim.AdamW(
            itertools.chain(self.G_AB.parameters(), self.G_BA.parameters()),
            lr=self.lr, weight_decay=1e-2)
        optimizer_D_A = torch.optim.AdamW(
            self.D_A.parameters(),
            lr=self.lr, weight_decay=1e-2)
        optimizer_D_B = torch.optim.AdamW(
            self.D_B.parameters(),
            lr=self.lr, weight_decay=1e-2)
        return [optimizer_G, optimizer_D_A, optimizer_D_B], []


def train_spaghetti(train_loader, val_loader, batch_size=1, weights=None,
                    lr=0.0002, save_dir=None, epochs=100, name="my_spaghetti",
                    num_nodes=1, ngpus_per_node="auto"):
    """
    Train the SPAGHETTI model using PyTorch Lightning.
    args:
        train_loader: the PyTorch Dataloader for the training dataset
        val_loader: the PyTorch Dataloader for the validation dataset
        batch_size: int, the batch size for the model, default 1
        weights: list of floats, the weights for the loss functions in the order of
        GAN loss, cycle loss, identity loss, and SSIM loss. Default [1.0, 10.0, 5.0, 10.0]
        lr: float, the learning rate for the model, default 0.0002
        save_dir: str, the directory to save the model checkpoints and logs. Default current directory
        epochs: int, the number of epochs to train the model, default 100
        name: str, the name of the model for the logger, default "my_spaghetti"
        num_nodes: int, the number of nodes to train the model, default 1
        ngpus_per_node: int, the number of GPUs per node, default "auto" to use all the available GPUs
    """
    if weights is None:
        weights = [1.0, 10.0, 5.0, 10.0]
    if save_dir is None:
        final_save_dir = os.getcwd()
    else:
        final_save_dir = save_dir
    if not os.path.exists(os.path.join(final_save_dir, f"{name}_visualization")):
        os.makedirs(os.path.join(final_save_dir, f"{name}_visualization"))
    # create model
    lit_model = _Spaghetti(save_dir=final_save_dir, batch_size=batch_size, weights=weights, lr=lr)
    # train model
    logger = CSVLogger(final_save_dir, name=name)
    trainer = pl.Trainer(max_epochs=epochs, devices=ngpus_per_node, num_nodes=num_nodes,
                         use_distributed_sampler=True, enable_progress_bar=True,
                         strategy="ddp",
                         default_root_dir=final_save_dir, logger=logger)
    print("Trainer initialized with ", ngpus_per_node, "GPU(s) per node on ", num_nodes, "node(s)")
    print("Training Starting...")
    ckpt = utils.find_checkpoint(final_save_dir)
    if ckpt:
        print("Checkpoint found. Resuming from ", ckpt)
    else:
        print("Starting from epoch 0")
    trainer.fit(lit_model, train_loader, val_loader, None, ckpt)
    print("Training ended.")
