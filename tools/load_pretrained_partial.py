"""
Partial weight loading from SVTR pretrained model to SVTR-RDA model.

Matches:
  patch_embed, pos_embed, blocks1, blocks2, sub_sample1, sub_sample2 -> loaded as-is
  blocks3.N.mixer.*  -> rda_layers.N.attn.*  (attention weights reused, MLP dropped)
  blocks3.N.norm1.*  -> rda_layers.N.norm.*
  last_conv          -> loaded as-is

Usage:
  python tools/load_pretrained_partial.py \
      --src pretrained_models/rec_svtr_tiny_none_ctc_en_train/best_accuracy.pdparams \
      --dst output/rec/svtr_rda_init.pdparams
"""

import argparse
import paddle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Path to original SVTR pretrained .pdparams")
    parser.add_argument("--dst", required=True, help="Output path for mapped weights")
    args = parser.parse_args()

    src = paddle.load(args.src)
    # pdparams may be wrapped under a key
    if "state_dict" in src:
        src = src["state_dict"]

    dst = {}
    loaded = []
    skipped = []

    for key, val in src.items():
        # Strip common "Student." or "backbone." prefixes if present
        k = key
        for prefix in ["Student.", "backbone.", "Backbone."]:
            if k.startswith(prefix):
                k = k[len(prefix):]

        # --- Direct copy: patch_embed, pos_embed, pos_drop ---
        if any(k.startswith(p) for p in [
            "patch_embed", "pos_embed", "pos_drop",
            "blocks1", "blocks2",
            "sub_sample1", "sub_sample2",
            "last_conv", "norm",
        ]):
            dst[key] = val
            loaded.append(key)
            continue

        # --- Map blocks3.N.mixer.* -> rda_layers.N.attn.* ---
        if k.startswith("blocks3."):
            rest = k[len("blocks3."):]          # e.g. "0.mixer.qkv.weight"
            parts = rest.split(".", 2)           # ["0", "mixer", "qkv.weight"]
            if len(parts) < 2:
                skipped.append(key)
                continue
            n = parts[0]                         # block index "0","1","2"
            sub = parts[1]                       # "mixer", "norm1", "norm2", "mlp", "drop_path"

            if sub == "mixer":
                # blocks3.N.mixer.X -> rda_layers.N.attn.X
                remainder = parts[2] if len(parts) > 2 else ""
                new_key = f"rda_layers.{n}.attn.{remainder}"
                dst[new_key] = val
                loaded.append(f"{key} -> {new_key}")
            elif sub == "norm1":
                # blocks3.N.norm1.X -> rda_layers.N.norm.X
                remainder = parts[2] if len(parts) > 2 else ""
                new_key = f"rda_layers.{n}.norm.{remainder}"
                dst[new_key] = val
                loaded.append(f"{key} -> {new_key}")
            else:
                # norm2, mlp, drop_path -> skip (MLP removed)
                skipped.append(key)
            continue

        skipped.append(key)

    paddle.save(dst, args.dst)

    print(f"\n=== Loaded {len(loaded)} tensors ===")
    for x in loaded:
        print(f"  OK  {x}")
    print(f"\n=== Skipped {len(skipped)} tensors ===")
    for x in skipped[:20]:
        print(f"  --  {x}")
    if len(skipped) > 20:
        print(f"  ... and {len(skipped)-20} more")
    print(f"\nSaved mapped weights to: {args.dst}")

if __name__ == "__main__":
    main()
