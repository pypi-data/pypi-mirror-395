import math
import torch
from tqdm import tqdm
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

    def forward(self, x, scale_shift=None):
        z = self.proj(x)
        z = self.norm(z)

        if scale_shift:
            scale, shift = scale_shift
            z = z * (scale + 1) + shift
        
        z = self.act(z)
        z = self.dropout(z)
        return z

class ResnetBlock(Module):
    def __init__(self, dim, dim_out, dropout = 0., time_emb_dim = None):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(time_emb_dim, dim_out * 2)
        ) if time_emb_dim is not None else None

        self.block1 = Block(dim, dim_out, dropout)
        self.block2 = Block(dim_out, dim_out)
        self.res_conv = nn.Conv2d(dim, dim_out, 1) if dim != dim_out else nn.Identity()

    def forward(self, x, time_emb: torch.Tensor):
        scale_shift = None
        if self.mlp is not None and time_emb is not None:
            time_emb = self.mlp(time_emb)
            time_emb = rearrange(time_emb, 'b c -> b c 1 1')
            scale_shift = time_emb.chunk(2, dim = 1)

        z = self.block1(x, scale_shift=scale_shift)
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

class SinusoidalPosEmb(Module):
    def __init__(self, dim, theta=10000):
        super().__init__()
        self.dim = dim
        self.theta = theta

    def forward(self, x: torch.Tensor):
        device = x.device
        half_dim = self.dim // 2
        emb = math.log(self.theta) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim).to(device) * -emb)
        emb = x[:, None] * emb[None, :]
        emb = torch.cat((emb.sin(), emb.cos()), dim=-1)
        return emb

class StageBlock(Module):
    def __init__(self, in_dim, dropout, time_emb_dim):
        super().__init__()
        self.res_block1 = ResnetBlock(in_dim, in_dim, dropout=dropout, time_emb_dim=time_emb_dim)
        self.res_block2 = ResnetBlock(in_dim, in_dim, dropout=dropout, time_emb_dim=time_emb_dim)
        self.attn = LinearAttention(in_dim)

    def forward(
            self, 
            x: torch.Tensor, 
            t: torch.Tensor
        ) -> torch.Tensor:
        z = self.res_block1(x, t)

        z = self.res_block2(z, t)
        z = self.attn(z) + z
        
        return z

class UNet(Module):
    def __init__(
            self,
            dim=64,
            dim_mults = (1, 2, 4, 8),
            channels = 4,
            dropout = 0.,
        ):
        super().__init__()
        self.dim = dim
        self.dim_mults = dim_mults
        self.channels = channels
        self.dropout = dropout

        self.self_condition = False

        encoder_dims = [*map(lambda m: dim * m, dim_mults)]
        decoder_dims = list(reversed(encoder_dims))
        down_stages_in_out_dims = list(zip(encoder_dims[:-1], encoder_dims[1:]))
        up_stages_in_out_dims = [(decoder_dims[0], decoder_dims[1])] + [(decoder_dims[i] * 2, decoder_dims[i + 1]) for i in range(1, len(decoder_dims) - 1)]
        mid_dim = encoder_dims[-1]

        # time embeddings
        time_dim = dim * 4
        sinu_pos_emb = SinusoidalPosEmb(dim, theta=10000)
        fourier_dim = dim
        self.time_mlp = nn.Sequential(
            sinu_pos_emb,
            nn.Linear(fourier_dim, time_dim),
            nn.GELU(),
            nn.Linear(time_dim, time_dim)
        )

        self.init_conv = nn.Conv2d(channels, dim, kernel_size=7, padding=3)
        self.init_res_block = ResnetBlock(dim, dim, dropout=dropout, time_emb_dim=time_dim)

        # ----- Encoder ----- #
        self.down_stages = ModuleList([])
        for i, (stage_in_dim, stage_out_dim) in enumerate(down_stages_in_out_dims):
            blocks = ModuleList()
            blocks.append(StageBlock(stage_in_dim, dropout=dropout, time_emb_dim=time_dim))
            
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
            blocks.append(StageBlock(stage_in_dim, dropout=dropout, time_emb_dim=time_dim))
            
            if stage_in_dim != stage_out_dim:
                blocks.append(Upsample(stage_in_dim, stage_out_dim))
            
            self.down_stages.append(nn.Sequential(*blocks))
        # ----- Decoder ----- #

        self.final_res_block = ResnetBlock(dim * 2, dim, dropout=dropout, time_emb_dim=time_dim)
        self.final_conv = nn.Conv2d(dim, channels, kernel_size=1)

    def forward(self, x: torch.Tensor, time: torch.Tensor, x_self_cond=None) -> torch.Tensor:
        # Time embedding
        t = self.time_mlp(time)

        # Initial conv and first ResBlock
        z: torch.Tensor = self.init_conv(x)
        z = self.init_res_block(z, t)
        skip0: torch.Tensor = z.clone()

        # ----- Encoder ----- #
        skips = []
        for i, down_stage in enumerate(self.down_stages):
            z = down_stage(z, t)
            if i < len(self.dim_mults) - 2:
                skips.append(z)
        # ----- Encoder ----- #

        # ----- Middle ----- #
        z = self.mid_block1(z, t)
        z = self.mid_attn(z) + z
        z = self.mid_block2(z, t)
        # ----- Middle ----- #

        # ----- Decoder ----- #
        skips.reverse()
        for i, up_stage in enumerate(self.up_stages):
            z = up_stage(z, t)
            if i < len(self.dim_mults) - 2:
                skip = skips.pop(0)
                z = torch.cat((skip, z), dim=1)
        # ----- Decoder ----- #

        # Final
        z = torch.cat((skip0, z), dim=1)
        z = self.final_res_block(z, t)
        x_recon = self.final_conv(z)

        return x_recon

ModelPrediction =  namedtuple('ModelPrediction', ['pred_noise', 'pred_x_start'])

def extract(a, t, x_shape):
    b, *_ = t.shape
    out = a.gather(-1, t)
    return out.reshape(b, *((1,) * (len(x_shape) - 1)))

def normalize_to_neg_one_to_one(img):
    return img * 2 - 1

def unnormalize_to_zero_to_one(t):
    return (t + 1) * 0.5

class Diffusion(Module):
    def __init__(
            self, 
            model: UNet, 
            image_size: int, 
            timesteps: int = 1000,
            beta_schedule: str = "linear",   # "linear", "cosine", "quadratic", "sigmoid"
            loss_type: str = "mse"           # "mse" or "l1"
        ):
        super().__init__()
        self.model = model
        self.image_size = image_size
        self.num_timesteps = timesteps
        self.device = next(self.parameters()).device
        self.beta_schedule = beta_schedule
        self.loss_type = loss_type

        # --- Beta schedule ---
        self.betas = self.make_beta_schedule(self.beta_schedule, timesteps).to(self.device)
        self.alphas = 1. - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1 - self.alphas_cumprod)
        self.alphas_cumprod_prev = F.pad(self.alphas_cumprod[:-1], (1, 0), value = 1.)

        self.sqrt_recip_alphas_cumprod = torch.sqrt(1. / self.alphas_cumprod)
        self.sqrt_recipm1_alphas_cumprod = torch.sqrt(1. / self.alphas_cumprod - 1)

        self.posterior_variance = self.betas * (1. - self.alphas_cumprod_prev) / (1. - self.alphas_cumprod)

        self.posterior_log_variance_clipped = torch.log(self.posterior_variance.clamp(min =1e-20))
        self.posterior_mean_coef1 = self.betas * torch.sqrt(self.alphas_cumprod_prev) / (1. - self.alphas_cumprod)
        self.posterior_mean_coef2 = (1. - self.alphas_cumprod_prev) * torch.sqrt(self.alphas) / (1. - self.alphas_cumprod)

        snr = self.alphas_cumprod / (1 - self.alphas_cumprod)
        maybe_clipped_snr = snr.clone()
        self.loss_weight = maybe_clipped_snr / snr

    # Beta Schedules
    def make_beta_schedule(self, schedule, timesteps):
        if schedule == "linear":
            return torch.linspace(1e-4, 0.02, timesteps)
        elif schedule == "quadratic":
            return torch.linspace(1e-4**0.5, 0.02**0.5, timesteps) ** 2
        elif schedule == "cosine":
            steps = timesteps + 1
            x = torch.linspace(0, timesteps, steps)
            alphas_cumprod = torch.cos(((x / timesteps) + 0.008) / 1.008 * math.pi / 2) ** 2
            alphas_cumprod = alphas_cumprod / alphas_cumprod[0]
            betas = 1 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
            return betas.clamp(0, 0.999)
        elif schedule == "sigmoid":
            betas = torch.linspace(-6, 6, timesteps)
            betas = torch.sigmoid(betas) * (0.02 - 1e-4) + 1e-4
            return betas
        else:
            raise NotImplementedError(f"Schedule {schedule} not implemented.")
    
    # Core helpers
    def predict_start_from_noise(self, x_t: torch.Tensor, t: torch.Tensor, noise: torch.Tensor):
        return (
            extract(self.sqrt_recip_alphas_cumprod, t, x_t.shape) * x_t -
            extract(self.sqrt_recipm1_alphas_cumprod, t, x_t.shape) * noise
        )
    
    def predict_noise_from_start(self, x_t: torch.Tensor, t: torch.Tensor, x0: torch.Tensor):
        return (
            (extract(self.sqrt_recip_alphas_cumprod, t, x_t.shape) * x_t - x0) / \
            extract(self.sqrt_recipm1_alphas_cumprod, t, x_t.shape)
        )
    
    def q_posterior(self, x_start: torch.Tensor, x_t: torch.Tensor, t: torch.Tensor):
        posterior_mean = (
            extract(self.posterior_mean_coef1, t, x_t.shape) * x_start +
            extract(self.posterior_mean_coef2, t, x_t.shape) * x_t
        )
        posterior_variance = extract(self.posterior_variance, t, x_t.shape)
        posterior_log_variance_clipped = extract(self.posterior_log_variance_clipped, t, x_t.shape)
        return posterior_mean, posterior_variance, posterior_log_variance_clipped

    def model_predictions(
            self, 
            x: torch.Tensor, 
            t: torch.Tensor, 
            clip_x_start=False, 
            rederive_pred_noise=False):
        model_output = self.model(x, t)
        maybe_clip = partial(torch.clamp, min = -1., max = 1.)

        pred_noise = model_output
        x_start = self.predict_start_from_noise(x, t, pred_noise)
        x_start = maybe_clip(x_start)

        if clip_x_start and rederive_pred_noise:
            pred_noise = self.predict_noise_from_start(x, t, x_start)

        return ModelPrediction(pred_noise, x_start)
    
    def p_mean_variance(self, x: torch.Tensor, t: torch.Tensor):
        preds = self.model_predictions(x, t)
        x_start: torch.Tensor = preds.pred_x_start
        x_start.clamp_(-1., 1.)

        model_mean, posterior_variance, posterior_log_variance = self.q_posterior(x_start = x_start, x_t = x, t = t)
        return model_mean, posterior_variance, posterior_log_variance, x_start
    
    def q_sample(self, x_start:torch.Tensor, t: torch.Tensor, noise: torch.Tensor):
        return (
            extract(self.sqrt_alphas_cumprod, t, x_start.shape) * x_start +
            extract(self.sqrt_one_minus_alphas_cumprod, t, x_start.shape) * noise
        )
    
    # Loss
    def p_losses(self, x_start: torch.Tensor, t: torch.Tensor):
        noise = torch.randn_like(x_start)

        x: torch.Tensor = self.q_sample(x_start, t, noise)

        predictions = self.model(x, t)

        # Calculate loss
        if self.loss_type == "mse":
            loss = F.mse_loss(predictions, noise, reduction='none')
        elif self.loss_type == "l1":
            loss = F.l1_loss(predictions, noise, reduction='none')
        else:
            raise ValueError(f"Unknown loss type: {self.loss_type}")
        # loss = F.mse_loss(predictions, noise, reduction='none')
        # loss = reduce(loss, 'b ... -> b', 'mean')
        loss = loss.mean(dim=[1, 2, 3])
        loss = loss * extract(self.loss_weight, t, loss.shape)
        loss = loss.mean()
        
        return loss

    def forward(self, x: torch.Tensor):
        t = torch.randint(0, self.num_timesteps, (x.shape[0], ), device=x.device)
        x = normalize_to_neg_one_to_one(x)
        return self.p_losses(x, t)
    
    @torch.inference_mode()
    def p_sample(self, x: torch.Tensor, t: int):
        batch_size = x.shape[0]

        t_batch = torch.full((batch_size,), t, device=self.device, dtype=torch.long)
        model_mean, _, model_log_variance, x_start = self.p_mean_variance(x = x, t = t_batch)
        noise = torch.randn_like(x) if t > 0 else 0. # no noise if t == 0
        pred_img = model_mean + (0.5 * model_log_variance).exp() * noise
        return pred_img, x_start
    
    @torch.inference_mode()
    def sample(self, batch_size: int, return_all_timesteps=False):
        target_image_shape = (batch_size, self.model.channels, self.image_size, self.image_size)

        image = torch.randn(target_image_shape).to(self.device)
        images = [image]

        for t in tqdm(reversed(range(0, self.num_timesteps)), desc="Sampling loop time step", total=self.num_timesteps):
            image, x_start = self.p_sample(image, t)
            images.append(image)
        
        # ret = torch.stack(images, dim = 1)
        ret = image if not return_all_timesteps else torch.stack(images, dim = 1)
        ret = unnormalize_to_zero_to_one(ret)
        return ret
    
    @torch.inference_mode()
    def ddim_sample(self, shape=[1, 3, 64, 64], sampling_timesteps=10, eta=0.0, return_all_timesteps = False):
        batch, device, total_timesteps, sampling_timesteps, eta = shape[0], self.device, self.num_timesteps, sampling_timesteps, eta

        times = torch.linspace(-1, total_timesteps - 1, steps = sampling_timesteps + 1)   # [-1, 0, 1, 2, ..., T-1] when sampling_timesteps == total_timesteps
        times = list(reversed(times.int().tolist()))
        time_pairs = list(zip(times[:-1], times[1:])) # [(T-1, T-2), (T-2, T-3), ..., (1, 0), (0, -1)]

        img = torch.randn(shape, device = device)
        imgs = [img]

        x_start = None

        for time, time_next in tqdm(time_pairs, desc = 'Sampling loop time step'):
            time_cond = torch.full((batch,), time, device = device, dtype = torch.long)
            pred_noise, x_start = self.model_predictions(img, time_cond, clip_x_start = True, rederive_pred_noise = True)

            if time_next < 0:
                img = x_start
                imgs.append(img)
                continue

            alpha = self.alphas_cumprod[time]
            alpha_next = self.alphas_cumprod[time_next]

            sigma = eta * ((1 - alpha / alpha_next) * (1 - alpha_next) / (1 - alpha)).sqrt()
            c = (1 - alpha_next - sigma ** 2).sqrt()

            noise = torch.randn_like(img)

            img = x_start * alpha_next.sqrt() + \
                  c * pred_noise + \
                  sigma * noise

            imgs.append(img)

        ret = img if not return_all_timesteps else torch.stack(imgs, dim = 1)

        ret = unnormalize_to_zero_to_one(ret)
        return ret