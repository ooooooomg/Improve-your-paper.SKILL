#!/usr/bin/env python3
"""Print PyTorch/CUDA/cv2 environment info for debugging setup issues."""
import sys

def check(name, import_str):
    try:
        mod = __import__(import_str)
        return mod
    except ImportError:
        return None

def main():
    print("=== Python ===")
    print(sys.version)

    print("\n=== PyTorch ===")
    torch = check('torch', 'torch')
    if torch:
        print(f"  version: {torch.__version__}")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  CUDA version: {torch.version.cuda}")
            print(f"  GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                vram_gb = props.total_mem / (1024**3)
                print(f"  GPU {i}: {props.name} ({vram_gb:.1f} GB)")
        print(f"  MPS available: {torch.backends.mps.is_available()}")
    else:
        print("  NOT INSTALLED")

    print("\n=== OpenCV ===")
    cv2 = check('cv2', 'cv2')
    print(f"  version: {cv2.__version__}" if cv2 else "  NOT INSTALLED")

    print("\n=== NumPy ===")
    np = check('numpy', 'numpy')
    print(f"  version: {np.__version__}" if np else "  NOT INSTALLED")

    print("\n=== CUDA Toolkit ===")
    import subprocess
    for cmd in ['nvcc --version', 'nvidia-smi --query-gpu=name,memory.total --format=csv']:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            print(f"  {cmd}:")
            for line in result.stdout.strip().split('\n')[:5]:
                print(f"    {line}")
        except Exception:
            print(f"  {cmd}: NOT FOUND")

    print("\n=== Environment Variables ===")
    import os
    for var in ['CUDA_VISIBLE_DEVICES', 'PYTHONHASHSEED', 'OMP_NUM_THREADS']:
        val = os.environ.get(var)
        print(f"  {var}={val}" if val else f"  {var}=(unset)")

if __name__ == '__main__':
    main()
