import torch
from torch import nn
from typing import Tuple
import torch.nn.functional as F
from torch.nn import Module, ModuleList
from einops.layers.torch import Rearrange

def Upsample(dim, dim_out):
    return nn.Sequential(
        nn.Upsample(scale_factor = 2, mode = 'nearest'),
        nn.Conv2d(dim, dim_out, 3, padding = 1)
    )

def Downsample(dim, dim_out):
    return nn.Sequential(
        Rearrange('b c (h p1) (w p2) -> b (c p1 p2) h w', p1 = 2, p2 = 2),
        nn.Conv2d(dim * 4, dim_out, 1)
    )

class RMSNorm(Module):
    def __init__(self, dim):
        super().__init__()
        self.scale = dim ** 0.5
        self.g = nn.Parameter(torch.ones(1, dim, 1, 1))

    def forward(self, x):
        return F.normalize(x, dim = 1) * self.g * self.scale

class Block(Module):
    def __init__(self, dim, dim_out, dropout = 0.):
        super().__init__()
        self.proj = nn.Conv2d(dim, dim_out, 3, padding = 1)
        self.norm = RMSNorm(dim_out)
        self.act = nn.SiLU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        z = self.proj(x)
        z = self.norm(z)
        z = self.act(z)
        z = self.dropout(z)
        return z

class ResnetBlock(Module):
    def __init__(self, dim, dim_out, dropout = 0.):
        super().__init__()
        self.block1 = Block(dim, dim_out, dropout)
        self.block2 = Block(dim_out, dim_out)
        self.res_conv = nn.Conv2d(dim, dim_out, 1) if dim != dim_out else nn.Identity()

    def forward(self, x):
        z = self.block1(x)
        z = self.block2(z)
        z = z + self.res_conv(x)
        return z

class Encoder(Module):
    def __init__(
            self,
            dim = 64,
            dim_mults = (1, 2, 4, 8),
            dim_latent = 64,
            image_size = 64,
            image_channels = 3,
            dropout = 0.,
        ):
        super().__init__()
        self.dim = dim
        self.dim_mults = dim_mults
        self.dim_latent = dim_latent
        self.image_channels = image_channels
        self.dropout = dropout
        self.image_size = image_size

        dims = [dim, *map(lambda m: dim * m, dim_mults)]
        stages_in_out_dims = list(zip(dims[:-1], dims[1:]))

        self.init_conv = nn.Conv2d(image_channels, dim, 7, padding = 3)

        self.down_stages = ModuleList([])
        for (stage_in_dim, stage_out_dim) in stages_in_out_dims:
            blocks = ModuleList()
            blocks.append(ResnetBlock(stage_in_dim, stage_in_dim, dropout=dropout))
            blocks.append(ResnetBlock(stage_in_dim, stage_in_dim, dropout=dropout))
            
            if stage_in_dim != stage_out_dim:
                blocks.append(Downsample(stage_in_dim, stage_out_dim))
            
            self.down_stages.append(nn.Sequential(*blocks))

        mid_dim = dims[-1]
        self.mid_block1 = ResnetBlock(mid_dim, dim_latent * 2, dropout=dropout)
        self.mu_logvar_out = ResnetBlock(dim_latent * 2, dim_latent * 2, dropout=dropout)
    
    def forward(self, x):
        z = self.init_conv(x)
        for down_stage in self.down_stages:
            z = down_stage(z)
        z = self.mid_block1(z)
        mu, logvar = torch.chunk(self.mu_logvar_out(z), chunks=2, dim=1)
        return mu, logvar

class Decoder(Module):
    def __init__(
            self,
            dim = 64,
            dim_mults = (1, 2, 4, 8),
            dim_latent = 64,
            image_size = 64,
            image_channels = 3,
            dropout = 0.,
        ):
        super().__init__()
        self.dim = dim
        self.dim_mults = dim_mults
        self.dim_latent = dim_latent
        self.image_channels = image_channels
        self.dropout = dropout
        self.image_size = image_size

        dims = [dim, *map(lambda m: dim * m, dim_mults)]
        stages_in_out_dims = list(zip(*map(reversed, (dims[1:], dims[:-1]))))

        self.z_in = ResnetBlock(dim_latent, dim_latent, dropout=dropout)
        
        mid_dim = dims[-1]
        self.mid_block1 = ResnetBlock(dim_latent, mid_dim)

        self.up_stages = ModuleList([])
        for (stage_in_dim, stage_out_dim) in stages_in_out_dims:
            blocks = ModuleList()
            blocks.append(ResnetBlock(stage_in_dim, stage_in_dim, dropout=dropout))
            blocks.append(ResnetBlock(stage_in_dim, stage_in_dim, dropout=dropout))
            
            if stage_in_dim != stage_out_dim:
                blocks.append(Upsample(stage_in_dim, stage_out_dim))
            
            self.up_stages.append(nn.Sequential(*blocks))
        
        self.out_dim = image_channels
        self.final_res_block = ResnetBlock(dim, dim)
        self.final_conv = nn.Conv2d(dim, self.out_dim, 1)
        self.final_activation = nn.Tanh()

    def forward(self, x):
        z = self.z_in(x)
        z = self.mid_block1(z)
        for up_stage in self.up_stages:
            z = up_stage(z)
        z = self.final_res_block(z)
        z = self.final_conv(z)
        z = self.final_activation(z)
        return z

class VariationalAutoEncoder(Module):
    def __init__(
            self,
            dim=64,
            dim_mults = (1, 2, 4, 8),
            dim_latent = 64,
            image_size = 64,
            image_channels = 3,
            dropout = 0.,
        ):
        super().__init__()
        self.encoder = Encoder(
            dim=dim,
            dim_mults=dim_mults,
            dim_latent=dim_latent,
            image_channels=image_channels,
            dropout=dropout,
            image_size=image_size,
        )

        self.decoder = Decoder(
            dim=dim,
            dim_mults=dim_mults,
            dim_latent=dim_latent,
            image_channels=image_channels,
            dropout=dropout,
            image_size=image_size,
        )
    
    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        z = mu + eps * std
        return z

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decoder(z)
        return x_recon, mu, logvar
    
    @torch.no_grad()
    def reconstruct(self, x: torch.Tensor) -> torch.Tensor:
        self.eval()
        x = x.to(next(self.parameters()).device)
        x_recon, _, _ = self.forward(x)
        return x_recon