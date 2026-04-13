import argparse
import os
import paddle


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract Student weights from a DistillationModel checkpoint."
    )
    parser.add_argument(
        "--src",
        required=True,
        help="Path to distillation checkpoint .pdparams (contains Teacher.* and Student.*)",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output path for student-only .pdparams",
    )
    parser.add_argument(
        "--prefix",
        default="Student.",
        help="Prefix to extract (default: Student.)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.src):
        raise FileNotFoundError(f"Source checkpoint not found: {args.src}")

    state_dict = paddle.load(args.src)
    student_state = {
        k[len(args.prefix) :]: v
        for k, v in state_dict.items()
        if k.startswith(args.prefix)
    }

    if not student_state:
        raise ValueError(
            f"No keys found with prefix '{args.prefix}'. "
            "Please check checkpoint format and prefix."
        )

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    paddle.save(student_state, args.out)

    src_mb = os.path.getsize(args.src) / (1024 * 1024)
    out_mb = os.path.getsize(args.out) / (1024 * 1024)

    print(f"[OK] Extracted prefix: {args.prefix}")
    print(f"[OK] Source: {args.src} ({src_mb:.2f} MB)")
    print(f"[OK] Output: {args.out} ({out_mb:.2f} MB)")
    print(f"[OK] Saved tensors: {len(student_state)}")


if __name__ == "__main__":
    main()


# cd D:\IEEE\data\phD\PaddleOCR D:\IEEE\data\phD\env\Scripts\python.exe tools\extract_student_from_distill.py --src output\rec\svtr_student_tiny_distill\best_model\model.pdparams --out output\rec\svtr_student_tiny_distill\student_only\model.pdparams