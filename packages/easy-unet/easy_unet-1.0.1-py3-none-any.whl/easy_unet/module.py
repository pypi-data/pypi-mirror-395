import torch
from typing import Optional
from torch import nn, einsum
from functools import partial
import torch.nn.functional as F
from collections import namedtuple
from einops import rearrange, repeat
from torch.nn import Module, ModuleList
from einops.layers.torch import Rearrange

def exists(val):
    return val is not None

def default(val, d):
    return val if exists(val) else d

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

AttentionConfig = namedtuple('AttentionConfig', ['enable_flash', 'enable_math', 'enable_mem_efficient'])
class Attend(nn.Module):
    def __init__(self, dropout=0., flash=False, scale: Optional[float] = None):
        super().__init__()
        self.dropout = dropout
        self.scale = scale
        self.attn_dropout = nn.Dropout(dropout)
        self.flash = flash

        # determine efficient attention configs for cpu and cuda
        self.cpu_config = AttentionConfig(True, True, True)
        self.cuda_config = AttentionConfig(True, True, True) if torch.cuda.is_available() and flash else None

    def flash_attn(self, q, k, v):
        _, heads, q_len, _, k_len, is_cuda, device = *q.shape, k.shape[-2], q.is_cuda, q.device

        # scaling
        if self.scale is not None:
            default_scale = q.shape[-1]
            q = q * (self.scale / default_scale)

        q, k, v = map(lambda t: t.contiguous(), (q, k, v))

        # select config
        config = self.cuda_config if is_cuda else self.cpu_config
        if config is None:
            raise RuntimeError("CUDA flash attention requested but cuda_config is None.")

        # new API for PyTorch 2.2+
        from torch.nn.attention import sdpa_kernel
        with sdpa_kernel(**config._asdict()):
            out = F.scaled_dot_product_attention(
                q, k, v,
                dropout_p=self.dropout if self.training else 0.
            )
        return out

    def forward(self, q, k, v):
        q_len, k_len, device = q.shape[-2], k.shape[-2], q.device

        if self.flash:
            return self.flash_attn(q, k, v)

        scale = self.scale if self.scale is not None else q.shape[-1] ** -0.5

        # similarity
        sim = einsum("b h i d, b h j d -> b h i j", q, k) * scale

        # attention
        attn = sim.softmax(dim=-1)
        attn = self.attn_dropout(attn)

        # aggregate values
        out = einsum("b h i j, b h j d -> b h i d", attn, v)
        return out

class LinearAttention(Module):
    def __init__(
        self,
        dim,
        heads = 4,
        dim_head = 32,
        num_mem_kv = 4
    ):
        super().__init__()
        self.scale = dim_head ** -0.5
        self.heads = heads
        hidden_dim = dim_head * heads

        self.norm = RMSNorm(dim)

        self.mem_kv = nn.Parameter(torch.randn(2, heads, dim_head, num_mem_kv))
        self.to_qkv = nn.Conv2d(dim, hidden_dim * 3, 1, bias = False)

        self.to_out = nn.Sequential(
            nn.Conv2d(hidden_dim, dim, 1),
            RMSNorm(dim)
        )

    def forward(self, x: torch.Tensor):
        b, c, h, w = x.shape

        x = self.norm(x)

        qkv: torch.Tensor = self.to_qkv(x)
        qkv_tuple = qkv.chunk(3, dim = 1)
        q, k, v = map(lambda t: rearrange(t, 'b (h c) x y -> b h c (x y)', h = self.heads), qkv_tuple)

        mk, mv = map(lambda t: repeat(t, 'h c n -> b h c n', b = b), self.mem_kv)
        k, v = map(partial(torch.cat, dim = -1), ((mk, k), (mv, v)))

        q = q.softmax(dim = -2)
        k = k.softmax(dim = -1)

        q = q * self.scale

        context = torch.einsum('b h d n, b h e n -> b h d e', k, v)

        out = torch.einsum('b h d e, b h d n -> b h e n', context, q)
        out = rearrange(out, 'b h c (x y) -> b (h c) x y', h = self.heads, x = h, y = w)
        return self.to_out(out)

class Attention(Module):
    def __init__(
        self,
        dim,
        heads = 4,
        dim_head = 32,
        num_mem_kv = 4,
        flash = False
    ):
        super().__init__()
        self.heads = heads
        hidden_dim = dim_head * heads

        self.norm = RMSNorm(dim)
        self.attend = Attend(flash = flash)

        self.mem_kv = nn.Parameter(torch.randn(2, heads, num_mem_kv, dim_head))
        self.to_qkv = nn.Conv2d(dim, hidden_dim * 3, 1, bias = False)
        self.to_out = nn.Conv2d(hidden_dim, dim, 1)

    def forward(self, x: torch.Tensor):
        b, c, h, w = x.shape

        x = self.norm(x)

        qkv: torch.Tensor = self.to_qkv(x)
        qkv_tuple = qkv.chunk(3, dim = 1)
        q, k, v = map(lambda t: rearrange(t, 'b (h c) x y -> b h (x y) c', h = self.heads), qkv_tuple)

        mk, mv = map(lambda t: repeat(t, 'h n d -> b h n d', b = b), self.mem_kv)
        k, v = map(partial(torch.cat, dim = -2), ((mk, k), (mv, v)))

        out = self.attend(q, k, v)

        out = rearrange(out, 'b h (x y) d -> b (h d) x y', x = h, y = w)
        return self.to_out(out)

class StageBlock(Module):
    def __init__(self, in_dim, dropout):
        super().__init__()
        self.res_block1 = ResnetBlock(in_dim, in_dim, dropout=dropout)
        self.res_block2 = ResnetBlock(in_dim, in_dim, dropout=dropout)
        self.attn = LinearAttention(in_dim)

    def forward(
            self, 
            x: torch.Tensor
        ) -> torch.Tensor:
        z = self.res_block1(x)

        z = self.res_block2(z)
        z = self.attn(z) + z
        
        return z

class EasyUNet(Module):
    def __init__(
            self,
            dim=64,
            dim_mults = (1, 2, 4, 8),
            channels = 4,
            out_channels = 1,
            dropout = 0.,
        ):
        super().__init__()
        self.dim = dim
        self.dim_mults = dim_mults
        self.channels = channels
        self.out_channels = out_channels
        self.dropout = dropout

        encoder_dims = [*map(lambda m: dim * m, dim_mults)]
        decoder_dims = list(reversed(encoder_dims))
        down_stages_in_out_dims = list(zip(encoder_dims[:-1], encoder_dims[1:]))
        up_stages_in_out_dims = [(decoder_dims[0], decoder_dims[1])] + [(decoder_dims[i] * 2, decoder_dims[i + 1]) for i in range(1, len(decoder_dims) - 1)]
        mid_dim = encoder_dims[-1]

        self.init_conv = nn.Conv2d(channels, dim, kernel_size=7, padding=3)
        self.init_res_block = ResnetBlock(dim, dim, dropout=dropout)

        # ----- Encoder ----- #
        self.down_stages = ModuleList([])
        for i, (stage_in_dim, stage_out_dim) in enumerate(down_stages_in_out_dims):
            blocks = ModuleList()
            blocks.append(StageBlock(stage_in_dim, dropout=dropout))
            
            if stage_in_dim != stage_out_dim:
                blocks.append(Downsample(stage_in_dim, stage_out_dim))
            
            self.down_stages.append(nn.Sequential(*blocks))
        # ----- Encoder ----- #

        self.mid_block1 = ResnetBlock(mid_dim, mid_dim)
        self.mid_attn = Attention(mid_dim)
        self.mid_block2 = ResnetBlock(mid_dim, mid_dim)

        # ----- Decoder ----- #
        self.up_stages = ModuleList([])
        for i, (stage_in_dim, stage_out_dim) in enumerate(up_stages_in_out_dims):
            blocks = ModuleList()
            blocks.append(StageBlock(stage_in_dim, dropout=dropout))
            
            if stage_in_dim != stage_out_dim:
                blocks.append(Upsample(stage_in_dim, stage_out_dim))
            
            self.down_stages.append(nn.Sequential(*blocks))
        # ----- Decoder ----- #

        self.final_res_block = ResnetBlock(dim * 2, dim, dropout=dropout)
        self.final_conv = nn.Conv2d(dim, out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Initial conv and first ResBlock
        z: torch.Tensor = self.init_conv(x)
        z = self.init_res_block(z)
        skip0: torch.Tensor = z.clone()

        # ----- Encoder ----- #
        skips = []
        for i, down_stage in enumerate(self.down_stages):
            z = down_stage(z)
            if i < len(self.dim_mults) - 2:
                skips.append(z)
        # ----- Encoder ----- #

        # ----- Middle ----- #
        z = self.mid_block1(z)
        z = self.mid_attn(z) + z
        z = self.mid_block2(z)
        # ----- Middle ----- #

        # ----- Decoder ----- #
        skips.reverse()
        for i, up_stage in enumerate(self.up_stages):
            z = up_stage(z)
            if i < len(self.dim_mults) - 2:
                skip = skips.pop(0)
                z = torch.cat((skip, z), dim=1)
        # ----- Decoder ----- #

        # Final
        z = torch.cat((skip0, z), dim=1)
        z = self.final_res_block(z)
        x_recon = self.final_conv(z)

        return x_recon