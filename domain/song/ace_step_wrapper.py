import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "ACE_Step" / "acestep"))

import os
import uuid
from domain.song.ACE_Step.acestep.pipeline_ace_step import ACEStepPipeline
from datetime import datetime


class ACEWrapper:
    def __init__(
        self,
        checkpoint_path: str = "checkpoints/ace_step",
        bf16: bool = True,
        torch_compile: bool = False,
        device_id: int = 0,
    ):
        os.environ["CUDA_VISIBLE_DEVICES"] = str(device_id)
        self.pipeline = ACEStepPipeline(
            checkpoint_dir=checkpoint_path,
            dtype="bfloat16" if bf16 else "float32",
            torch_compile=torch_compile
        )

    def generate(
        self,
        prompt: str,
        lyrics: str = "",
        duration: float = 45.0,
        save_path: str | None = None,
        infer_steps: int = 100
    ) -> dict:
        scheduler_type = "ddim"
        cfg_type = "cfg"
        omega_scale = 1.0
        manual_seeds = "1234"
        guidance_scale = 7.0
        guidance_interval = 1.0
        guidance_interval_decay = 1.0
        min_guidance_scale = 1.0
        use_erg_tag = True
        use_erg_lyric = True
        use_erg_diffusion = True
        oss_steps = "30,60"
        guidance_scale_text = 0.0
        guidance_scale_lyric = 0.0

        if not save_path:
            date_str = datetime.now().strftime("%y%m%d")
            filename = f"{date_str}_{uuid.uuid4().hex}.wav"
            save_path = os.path.join("uploads/song", filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

        self.pipeline(
            audio_duration=duration,
            prompt=prompt,
            lyrics=lyrics,
            infer_step=infer_steps,
            guidance_scale=guidance_scale,
            scheduler_type=scheduler_type,
            cfg_type=cfg_type,
            omega_scale=omega_scale,
            manual_seeds=manual_seeds,
            guidance_interval=guidance_interval,
            guidance_interval_decay=guidance_interval_decay,
            min_guidance_scale=min_guidance_scale,
            use_erg_tag=use_erg_tag,
            use_erg_lyric=use_erg_lyric,
            use_erg_diffusion=use_erg_diffusion,
            oss_steps=oss_steps,
            guidance_scale_text=guidance_scale_text,
            guidance_scale_lyric=guidance_scale_lyric,
            save_path=save_path
        )

        metadata_path = save_path.replace(".wav", ".json")

        return {
            "audio_path": save_path,
            "metadata_path": metadata_path
        }
