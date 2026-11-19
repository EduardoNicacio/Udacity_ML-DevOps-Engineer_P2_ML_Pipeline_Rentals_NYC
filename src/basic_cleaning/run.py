#!/usr/bin/env python
"""Download a W&B artifact, perform basic cleaning, and log the result."""

import argparse
import logging

import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact.
    logger.info(f"Downloading input artifact {args.input_artifact}")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)
    logger.info(f"Loaded input data: {df.shape[0]} rows, {df.shape[1]} columns")

    # Drop rows with a price outside of the accepted nightly price window
    rows_before = df.shape[0]
    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info(
        f"Price filter [{args.min_price}, {args.max_price}]: kept {df.shape[0]} of "
        f"{rows_before} rows ({rows_before - df.shape[0]} removed)"
    )

    # Convert last_review from text to datetime
    df["last_review"] = pd.to_datetime(df["last_review"])
    logger.info("Converted last_review to datetime")

    # NOTE: missing values are intentionally NOT imputed here. Imputation is
    # handled by the inference pipeline, so the deployed model can also process
    # incomplete records at prediction time.

    logger.info(f"Saving cleaned data to clean_sample.csv ({df.shape[0]} rows)")
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    logger.info(
        f"Uploaded {args.output_artifact} of type {args.output_type} to Weights & Biases"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully qualified name of the input W&B artifact (e.g. sample.csv:latest)",
        required=True,
    )
    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the cleaned output artifact (e.g. clean_sample.csv)",
        required=True,
    )
    parser.add_argument(
        "--output_type",
        type=str,
        help="W&B artifact type for the cleaned data (e.g. clean_sample)",
        required=True,
    )
    parser.add_argument(
        "--output_description",
        type=str,
        help="Human-readable description for the cleaned output artifact",
        required=True,
    )
    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum acceptable nightly price in dollars",
        required=True,
    )
    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum acceptable nightly price in dollars",
        required=True,
    )

    args = parser.parse_args()
    go(args)
