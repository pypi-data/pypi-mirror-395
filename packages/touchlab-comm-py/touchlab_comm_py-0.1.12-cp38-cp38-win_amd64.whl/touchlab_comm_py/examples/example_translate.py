#!/usr/bin/env python3

# Copyright (c) 2025 Touchlab Limited. All Rights Reserved
# Unauthorized copying or modifications of this file, via any medium is strictly prohibited.

import touchlab_comm_py as tl
import time
import argparse
import numpy as np

def plot(raw, translated):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))

    x = np.arange(raw.shape[0])

    plt.subplot(2, 1, 1)
    plt.title("Raw Data")
    plt.plot(x, raw)
    plt.ylabel('Channels')
    plt.xlabel('Samples')

    plt.subplot(2, 1, 2)
    plt.title("Translated Data")
    plt.plot(x, translated)
    plt.ylabel('Channels')
    plt.xlabel('Samples')

    plt.tight_layout()
    plt.show()

def main():
      # Set up argument parser
      parser = argparse.ArgumentParser(description="Touchlab Sensor Example")
      parser.add_argument("parameter_file", type=str, help="Parameter file to load")
      args = parser.parse_args()

      # Load parameters from a file
      com=tl.TouchlabComms()
      com.init(args.parameter_file)

      # Create sample data for translation
      sample_data = np.tile(np.sin(np.linspace(0, np.pi, 100)) *  3000 + 3000, (18, 1)).transpose()
      sample_data += np.round(np.random.normal(0, 20.0, sample_data.shape))

      # Pick a bias from the sample data
      bias = sample_data[0:1, :].tolist()

      # Zero the translator and translate the sample data
      com.zero(bias, [])
      translated = np.zeros((sample_data.shape[0], len(com.translate(sample_data[0]))))
      for i, row in enumerate(sample_data):
          translated[i, :] = com.translate(row)

      plot(sample_data, translated)

if __name__ == "__main__":
    main()
