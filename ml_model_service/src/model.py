import torch
from diffusers import StableDiffusionXLPipeline, AutoPipelineForText2Image
from diffusers import DPMSolverMultistepScheduler


def get_model() -> AutoPipelineForText2Image:
    """
    Get the ML model.

    Returns
    -------
    AutoPipelineForText2Image
        The ML model.
    """
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "RunDiffusion/Juggernaut-X-Hyper",
        torch_dtype=torch.float16
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    pipe.enable_sequential_cpu_offload()

    txt2img = AutoPipelineForText2Image.from_pipe(pipe)
    
    return txt2img


txt2img_model = get_model()
