# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
import argparse
import os
from glob import glob

import torch
from safetensors import safe_open


def yield_keys_and_tensors(safetensors_file_names):
    for safetensors_file_name in safetensors_file_names:
        with safe_open(safetensors_file_name, framework='pt') as f:
            for k in f.keys():
                yield k, f.get_tensor(k)


def extract_layer_state_dict(safetensors_file_names, layer_name):
    layer_name_components = layer_name.split('.')
    layer_name_components_length = len(layer_name_components)
    state_dict = {}

    for key, tensor in yield_keys_and_tensors(safetensors_file_names):
        if key.startswith(layer_name):
            key_components = key.split('.')
            if key_components[:layer_name_components_length] == layer_name_components:
                key_components_without_layer_name_components = key_components[layer_name_components_length:]
                key_without_layer_name = '.'.join(key_components_without_layer_name_components)
                state_dict[key_without_layer_name] = tensor

    if not state_dict:
        raise Exception('No parameters found matching the exact layer name: %r' % (layer_name,))
    return state_dict


def main():
    parser = argparse.ArgumentParser(
        description="Extract a layer's state_dict from concatenated safetensors files (PyTorch format)."
    )
    parser.add_argument('--model-dir', required=True, help='Model directory containing *.safetensors files')
    parser.add_argument('--layer', required=True, help='Exact layer name (e.g., model.layers.8.self_attn)')
    parser.add_argument('--output', help='Output file (default: <layer>.pt)')
    args = parser.parse_args()

    safetensors_file_names = glob(os.path.join(os.path.expanduser(args.model_dir), '*.safetensors'))
    if not safetensors_file_names:
        raise Exception('No .safetensors files found in directory %r' % (args.model_dir,))

    state_dict = extract_layer_state_dict(safetensors_file_names, args.layer)

    output_file = args.output or (args.layer + '.ckpt')
    torch.save(state_dict, output_file)


if __name__ == '__main__':
    main()
