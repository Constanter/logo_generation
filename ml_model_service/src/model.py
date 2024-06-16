import torch
from diffusers import AutoPipelineForText2Image,DPMSolverMultistepScheduler


def get_model() -> AutoPipelineForText2Image:
    """
    Get the ML model.

    Returns
    -------
    AutoPipelineForText2Image
        The ML model.
    """
    pipe = AutoPipelineForText2Image.from_pretrained(
        'lykon/dreamshaper-xl-v2-turbo',
        torch_dtype=torch.float16,
        variant="fp16"
    )

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    pipe.enable_sequential_cpu_offload()

    txt2img = AutoPipelineForText2Image.from_pipe(pipe)
    
    return txt2img


txt2img_model = get_model()
