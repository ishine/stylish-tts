from config_loader import Config
from batch_manager import BatchManager
from typing import Callable, Optional, Any, List
from accelerate import Accelerator
import logging
from torch.utils.data import DataLoader
from losses import GeneratorLoss, DiscriminatorLoss, WavLMLoss, MultiResolutionSTFTLoss
from models.diffusion.sampler import DiffusionSampler
from models.slmadv import SLMAdversarialLoss
import json


class Manifest:
    def __init__(self) -> None:
        self.current_epoch: int = 0
        self.current_step: int = 0
        self.steps_per_epoch: int = 0
        self.current_total_step: int = 0
        self.total_trained_audio_seconds: float = 0.0
        self.stage: str = "first"
        self.best_loss: float = float("inf")
        self.max_epoch: int = 0
        self.training_log: list = []
        self.running_std: List[float] = []

    def load(self, path: str) -> None:
        with open(path, "r") as f:
            self.__dict__ = json.load(f)


class TrainContext:
    def __init__(self) -> None:
        self.config: Optional[Config] = None
        self.batch_manager: Optional[BatchManager] = None
        self.manifest: Manifest = Manifest()

        # Training functions
        self.train_batch: Optional[Callable] = None
        self.validate: Optional[Callable] = None

        self.accelerator: Optional[Accelerator] = None
        self.val_dataloader: Optional[DataLoader] = None

        self.model: Optional[Any] = None
        self.optimizer: Optional[Any] = None  # e.g., torch.optim.Optimizer

        self.logger: Optional[logging.Logger] = None

        self.diffusion_sampler: Optional[DiffusionSampler] = None  # Diffusion Sampler

        # Losses
        self.generator_loss: Optional[GeneratorLoss] = None  # Generator Loss
        self.discriminator_loss: Optional[DiscriminatorLoss] = (
            None  # Discriminator Loss
        )
        self.wavlm_loss: Optional[WavLMLoss] = None  # WavLM Loss
        self.stft_loss: Optional[MultiResolutionSTFTLoss] = None  # MultiRes STFT Loss
        self.slm_adversarial_loss: Optional[SLMAdversarialLoss] = None

        # Run parameters
        self.n_down: Optional[int] = None
        self.start_ds: Optional[int] = None
        self.early_joint: bool = False
