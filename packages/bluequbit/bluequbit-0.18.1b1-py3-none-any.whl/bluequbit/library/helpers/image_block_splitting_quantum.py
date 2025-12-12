import logging
import math

import numpy as np

logger = logging.getLogger("bluequbit-python-sdk")


def find_largest_power_of_2(n):
    """
    Find the largest power of 2 that is less than or equal to n

    Parameters:
        n (int): Input number

    Returns:
        int: Largest power of 2 <= n
    """
    if n <= 0:
        return 1

    power = int(math.log2(n))
    return 2**power


def find_best_grid_arrangement(num_blocks, height, width):
    """
    Find the best grid arrangement (blocks_y, blocks_x) for a given number of blocks
    that maximizes the resulting block size (minimum of block height and block width)

    Parameters:
        num_blocks (int): Target number of blocks
        height (int): Image height
        width (int): Image width

    Returns:
        tuple: (blocks_y, blocks_x) that gives the largest possible blocks
    """
    best_arrangement = (1, num_blocks)
    best_block_size = 0

    for blocks_y in range(1, num_blocks + 1):
        if num_blocks % blocks_y != 0:
            continue
        blocks_x = num_blocks // blocks_y

        block_height = height // blocks_y
        block_width = width // blocks_x

        max_square_size = min(block_height, block_width)

        if max_square_size > best_block_size:
            best_block_size = max_square_size
            best_arrangement = (blocks_y, blocks_x)

    if height % best_arrangement[0] != 0 or width % best_arrangement[1] != 0:
        raise ValueError(
            f"Couldn't split image ({height}x{width}) into {num_blocks} blocks."
        )

    return best_arrangement


def apply_epsilon_clipping(block, epsilon=1e-12):
    """
    Apply epsilon clipping to a block to handle zero values

    Parameters:
        block (numpy.ndarray): Input block
        epsilon (float): Small value to replace zeros with

    Returns:
        tuple: (clipped_block, statistics)
    """
    zero_mask = block == 0
    zeros_count = np.sum(zero_mask)

    clipped_block = block.copy()
    clipped_block[zero_mask] = epsilon

    stats = {
        "zeros_clipped": int(zeros_count),
        "total_pixels": int(block.size),
        "zero_percentage": float(zeros_count / block.size * 100),
        "min_value_before": float(np.min(block)),
        "min_value_after": float(np.min(clipped_block)),
        "max_value": float(np.max(block)),
    }

    return clipped_block, stats


def split_image_for_quantum(image, num_blocks, *, normalize_blocks=True, epsilon=1e-12):
    """
    Split an image into square blocks with power-of-2 dimensions for quantum processing
    Each block is normalized to sum to 1 individually, with epsilon clipping for zero values

    Parameters:
        image (numpy.ndarray): Input image
        num_blocks (int): Number of blocks to create
        normalize_blocks (bool): Whether to normalize each block to sum to 1
        epsilon (float): Small value to clip zero pixels to avoid numerical issues

    Returns:
        dict: Dictionary containing:
            - 'blocks': List of square image blocks (each normalized to sum to 1)
            - 'normalization_factors': List of normalization factors for each block
            - 'epsilon_info': Information about epsilon clipping applied
            - 'block_size': Size of each square block (d)
            - 'qubits_needed': Number of qubits needed per block (2 * log2(d))
            - 'blocks_y': Number of blocks in y direction
            - 'blocks_x': Number of blocks in x direction
            - 'original_shape': Original image shape
            - 'cropped_shape': Shape after cropping to fit blocks
            - 'metadata': Additional info for reconstruction
    """
    # Get image dimensions
    if len(image.shape) == 3:
        height, width, channels = image.shape
    else:
        height, width = image.shape
        channels = 1

    # Find the best grid arrangement for the given number of blocks
    blocks_y, blocks_x = find_best_grid_arrangement(num_blocks, height, width)

    # Calculate the maximum possible block dimensions
    max_block_height = height // blocks_y
    max_block_width = width // blocks_x

    # Find the largest power of 2 that fits in both dimensions
    max_block_size = min(max_block_height, max_block_width)
    block_size = find_largest_power_of_2(max_block_size)

    # Calculate qubits needed
    qubits_needed = 2 * int(math.log2(block_size))

    # Crop the image to fit the blocks perfectly
    cropped_height = blocks_y * block_size
    cropped_width = blocks_x * block_size

    if len(image.shape) == 3:
        cropped_image = image[:cropped_height, :cropped_width, :]
    else:
        cropped_image = image[:cropped_height, :cropped_width]

    # Split the cropped image into blocks and normalize each one
    blocks = []
    normalization_factors = []
    epsilon_stats = {
        "total_zeros_clipped": 0,
        "blocks_with_zeros": 0,
        "epsilon_used": epsilon,
        "per_block_stats": [],
    }

    for y in range(blocks_y):
        for x in range(blocks_x):
            y_start = y * block_size
            y_end = (y + 1) * block_size
            x_start = x * block_size
            x_end = (x + 1) * block_size

            if len(cropped_image.shape) == 3:
                block = cropped_image[y_start:y_end, x_start:x_end, :].astype(
                    np.float32
                )
            else:
                block = cropped_image[y_start:y_end, x_start:x_end].astype(np.float32)

            # Apply epsilon clipping to handle zero values
            block_clipped, block_epsilon_stats = apply_epsilon_clipping(block, epsilon)

            # Track epsilon statistics
            epsilon_stats["total_zeros_clipped"] += block_epsilon_stats["zeros_clipped"]
            if block_epsilon_stats["zeros_clipped"] > 0:
                epsilon_stats["blocks_with_zeros"] += 1
            epsilon_stats["per_block_stats"].append(block_epsilon_stats)

            # Calculate normalization factor for this block (after epsilon clipping)
            block_sum = float(np.sum(block_clipped))

            if normalize_blocks and block_sum > 0.0:
                # Normalize block to sum to 1
                normalized_block = block_clipped / block_sum
                normalization_factors.append(block_sum)
            else:
                # Don't normalize, but still track the sum
                normalized_block = block_clipped
                normalization_factors.append(block_sum if block_sum > 0 else 1.0)

            blocks.append(normalized_block)

    return {
        "blocks": blocks,
        "normalization_factors": normalization_factors,
        "epsilon_info": epsilon_stats,
        "block_size": block_size,
        "qubits_needed": qubits_needed,
        "blocks_y": blocks_y,
        "blocks_x": blocks_x,
        "original_shape": image.shape,
        "cropped_shape": cropped_image.shape,
        "metadata": {
            "num_blocks_requested": num_blocks,
            "num_blocks_created": len(blocks),
            "channels": channels,
            "normalized": normalize_blocks,
            "epsilon_clipped": True,
            "epsilon_value": epsilon,
            "crop_info": {
                "original_height": height,
                "original_width": width,
                "cropped_height": cropped_height,
                "cropped_width": cropped_width,
            },
        },
    }


def reconstruct_from_blocks(
    processed_blocks, split_result, *, denormalize=True, remove_epsilon=False
):
    """
    Reconstruct an image from processed blocks using the original split result metadata

    Parameters:
        processed_blocks (list): List of processed blocks (same order as original split)
        split_result (dict): Result dictionary from split_image_for_quantum
        denormalize (bool): Whether to apply the original normalization factors to restore scale
        remove_epsilon (bool): Whether to attempt to remove epsilon padding (set small values back to 0)

    Returns:
        numpy.ndarray: Reconstructed image
    """
    blocks_y = split_result["blocks_y"]
    blocks_x = split_result["blocks_x"]
    block_size = split_result["block_size"]
    channels = split_result["metadata"]["channels"]
    normalization_factors = split_result["normalization_factors"]
    epsilon = split_result["metadata"]["epsilon_value"]

    # Calculate reconstructed image dimensions
    height = blocks_y * block_size
    width = blocks_x * block_size

    # Create empty image
    if channels == 1:
        reconstructed = np.zeros((height, width), dtype=np.float32)
    else:
        reconstructed = np.zeros((height, width, channels), dtype=np.float32)

    # Place each block back
    block_idx = 0
    for y in range(blocks_y):
        for x in range(blocks_x):
            y_start = y * block_size
            y_end = (y + 1) * block_size
            x_start = x * block_size
            x_end = (x + 1) * block_size

            # Get the processed block
            processed_block = processed_blocks[block_idx].copy()

            # Print diagnostic information
            logger.debug(f"Block {block_idx} before denormalization:")
            logger.debug(f"Sum: {np.sum(processed_block):.6f}")
            logger.debug(f"Min: {np.min(processed_block):.6f}")
            logger.debug(f"Max: {np.max(processed_block):.6f}")

            # Apply denormalization if requested
            if denormalize and split_result["metadata"]["normalized"]:
                processed_block *= normalization_factors[block_idx]
                logger.debug(
                    f"After denormalization (factor: {normalization_factors[block_idx]:.6f}):"
                )
                logger.debug(f"Sum: {np.sum(processed_block):.6f}")
                logger.debug(f"Min: {np.min(processed_block):.6f}")
                logger.debug(f"Max: {np.max(processed_block):.6f}")

            # Remove epsilon padding if requested
            if remove_epsilon:
                epsilon_threshold = epsilon * 2
                processed_block[processed_block <= epsilon_threshold] = 0

            # Place the block
            if channels == 1:
                reconstructed[y_start:y_end, x_start:x_end] = processed_block
            else:
                reconstructed[y_start:y_end, x_start:x_end, :] = processed_block

            block_idx += 1

    return reconstructed
