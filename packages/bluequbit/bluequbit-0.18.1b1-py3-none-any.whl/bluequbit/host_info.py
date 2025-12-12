import subprocess


def check_local_gpu_availability():
    try:
        subprocess.run(
            ["nvidia-smi"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
            timeout=0.5,
        )
    except (
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
        FileNotFoundError,
    ):
        return False
    return True
