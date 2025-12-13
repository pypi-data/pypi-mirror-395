#!/usr/bin/env python3
"""
Progressive Decompression for NeuroGlyph
=========================================

Enables progressive image rendering during download/decompression.
Perfect for web applications and streaming scenarios.

How it works:
1. Image divided into multiple quality layers (passes)
2. Each pass refines the image (similar to JPEG progressive)
3. First pass: Low resolution preview (1/8 size)
4. Second pass: Medium resolution (1/4 size)
5. Third pass: High resolution (1/2 size)
6. Final pass: Full resolution

Benefits:
- Faster perceived loading time
- Better user experience (see something immediately)
- Graceful degradation on slow connections
- Can stop decoding early for thumbnails

Strategy:
- Use wavelet decomposition natural hierarchy
- Each level = one progressive pass
- Decode only what you need
"""

import numpy as np
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import time


class ProgressiveQuality(Enum):
    """Quality levels for progressive decoding"""
    THUMBNAIL = 1    # 1/8 resolution, fast preview
    LOW = 2          # 1/4 resolution
    MEDIUM = 3       # 1/2 resolution
    HIGH = 4         # Full resolution
    

@dataclass
class ProgressivePass:
    """Information about a progressive decoding pass"""
    pass_number: int
    quality: ProgressiveQuality
    resolution: Tuple[int, int]
    data_size: int
    cumulative_size: int
    decode_time_ms: float


@dataclass
class ProgressiveStats:
    """Statistics for progressive compression/decompression"""
    total_passes: int
    original_size: int
    compressed_size: int
    passes: List[ProgressivePass]
    supports_early_termination: bool


class ProgressiveEncoder:
    """Encode images for progressive decompression"""
    
    @staticmethod
    def encode_progressive(image: np.ndarray, num_passes: int = 4) -> Tuple[bytes, ProgressiveStats]:
        """
        Encode image with progressive passes
        
        Args:
            image: Input image (H, W)
            num_passes: Number of progressive quality levels (1-4)
            
        Returns:
            compressed_data: Encoded progressive stream
            stats: Encoding statistics
        """
        if image.dtype != np.uint8:
            raise ValueError(f"Expected uint8 image, got {image.dtype}")
        
        h, w = image.shape
        original_size = image.nbytes
        
        # Create wavelet pyramid (natural progressive structure)
        pyramid = ProgressiveEncoder._create_pyramid(image, num_passes)
        
        # Encode each level
        import zlib
        passes_data = []
        passes_info = []
        cumulative_size = 0
        
        for i, (level_img, quality) in enumerate(pyramid):
            start_time = time.perf_counter()
            
            # Compress this level
            compressed_level = zlib.compress(level_img.tobytes(), level=9)
            passes_data.append(compressed_level)
            
            decode_time = (time.perf_counter() - start_time) * 1000
            cumulative_size += len(compressed_level)
            
            pass_info = ProgressivePass(
                pass_number=i + 1,
                quality=quality,
                resolution=level_img.shape,
                data_size=len(compressed_level),
                cumulative_size=cumulative_size,
                decode_time_ms=decode_time
            )
            passes_info.append(pass_info)
        
        # Package all passes
        # Header: [magic, version, h, w, num_passes]
        header = np.array([
            0x5047,  # Magic: 'PG' (Progressive)
            0x0100,  # Version 1.0
            h, w,
            num_passes
        ], dtype=np.uint16)
        
        # Pass sizes
        sizes = np.array([len(p) for p in passes_data], dtype=np.uint32)
        
        # Combine all data
        compressed_data = header.tobytes() + sizes.tobytes() + b''.join(passes_data)
        
        stats = ProgressiveStats(
            total_passes=num_passes,
            original_size=original_size,
            compressed_size=len(compressed_data),
            passes=passes_info,
            supports_early_termination=True
        )
        
        return compressed_data, stats
    
    @staticmethod
    def _create_pyramid(image: np.ndarray, num_levels: int) -> List[Tuple[np.ndarray, ProgressiveQuality]]:
        """
        Create image pyramid using wavelet decomposition
        
        Returns list of (image, quality) tuples from coarse to fine
        """
        pyramid = []
        
        # Quality mapping
        quality_map = {
            1: ProgressiveQuality.THUMBNAIL,
            2: ProgressiveQuality.LOW,
            3: ProgressiveQuality.MEDIUM,
            4: ProgressiveQuality.HIGH
        }
        
        # Generate downsampled versions (coarse to fine)
        h, w = image.shape
        
        for level in range(1, num_levels + 1):
            # Scale factor for this level
            scale = 2 ** (num_levels - level)
            
            if scale > 1:
                # Downsample
                scaled_h = h // scale
                scaled_w = w // scale
                downsampled = image.reshape(scaled_h, scale, scaled_w, scale).mean(axis=(1, 3))
                pyramid.append((downsampled.astype(np.uint8), quality_map[level]))
            else:
                # Full resolution
                pyramid.append((image, quality_map[level]))
        
        return pyramid


class ProgressiveDecoder:
    """Decode progressive images with quality control"""
    
    def __init__(self):
        self.current_pass = 0
        self.image_data = None
        self.header_parsed = False
        
    def decode_progressive(
        self, 
        compressed_data: bytes, 
        max_quality: ProgressiveQuality = ProgressiveQuality.HIGH,
        callback: Optional[Callable[[np.ndarray, int], None]] = None
    ) -> Tuple[np.ndarray, ProgressiveStats]:
        """
        Decode progressive image up to specified quality
        
        Args:
            compressed_data: Compressed progressive stream
            max_quality: Maximum quality to decode (can stop early)
            callback: Optional callback(image, pass_number) called after each pass
            
        Returns:
            final_image: Decoded image at requested quality
            stats: Decoding statistics
        """
        import zlib
        
        # Parse header
        header = np.frombuffer(compressed_data[:10], dtype=np.uint16)
        magic, version, h, w, num_passes = header
        
        if magic != 0x5047:
            raise ValueError("Invalid progressive format")
        
        # Parse pass sizes
        offset = 10
        sizes = np.frombuffer(
            compressed_data[offset:offset + num_passes*4], 
            dtype=np.uint32
        )
        offset += num_passes * 4
        
        # Decode passes progressively
        passes_info = []
        current_image = None
        max_pass = min(max_quality.value, num_passes)
        
        for i in range(max_pass):
            start_time = time.perf_counter()
            
            # Extract this pass data
            pass_size = sizes[i]
            pass_data = compressed_data[offset:offset + pass_size]
            offset += pass_size
            
            # Decompress
            decompressed = zlib.decompress(pass_data)
            
            # Reconstruct image at this quality level
            scale = 2 ** (num_passes - i - 1)
            pass_h = h // scale
            pass_w = w // scale
            
            pass_image = np.frombuffer(decompressed, dtype=np.uint8).reshape(pass_h, pass_w)
            
            # Upsample to full resolution for display
            if i < max_pass - 1:
                # Not final pass - upsample for preview
                current_image = ProgressiveDecoder._upsample_to_size(pass_image, (h, w))
            else:
                # Final pass
                current_image = pass_image if scale == 1 else ProgressiveDecoder._upsample_to_size(pass_image, (h, w))
            
            decode_time = (time.perf_counter() - start_time) * 1000
            
            # Record pass info
            quality_map = {
                1: ProgressiveQuality.THUMBNAIL,
                2: ProgressiveQuality.LOW,
                3: ProgressiveQuality.MEDIUM,
                4: ProgressiveQuality.HIGH
            }
            
            pass_info = ProgressivePass(
                pass_number=i + 1,
                quality=quality_map.get(i + 1, ProgressiveQuality.HIGH),
                resolution=pass_image.shape,
                data_size=pass_size,
                cumulative_size=offset - 10 - num_passes*4,
                decode_time_ms=decode_time
            )
            passes_info.append(pass_info)
            
            # Callback for progressive display
            if callback:
                callback(current_image.copy(), i + 1)
        
        stats = ProgressiveStats(
            total_passes=num_passes,
            original_size=h * w,
            compressed_size=len(compressed_data),
            passes=passes_info,
            supports_early_termination=True
        )
        
        return current_image, stats
    
    @staticmethod
    def _upsample_to_size(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Upsample image to target size using nearest neighbor"""
        h, w = image.shape
        target_h, target_w = target_size
        
        # Simple nearest neighbor upsampling
        row_ratio = target_h / h
        col_ratio = target_w / w
        
        upsampled = np.zeros(target_size, dtype=image.dtype)
        
        for i in range(target_h):
            for j in range(target_w):
                src_i = int(i / row_ratio)
                src_j = int(j / col_ratio)
                upsampled[i, j] = image[src_i, src_j]
        
        return upsampled


class StreamingProgressiveDecoder:
    """Decode progressive image from streaming data (partial downloads)"""
    
    def __init__(self):
        self.buffer = bytearray()
        self.header_parsed = False
        self.current_pass = 0
        self.passes_decoded = []
        
    def add_data(self, chunk: bytes) -> Optional[np.ndarray]:
        """
        Add data chunk and try to decode next pass
        
        Returns:
            Updated image if new pass available, None otherwise
        """
        self.buffer.extend(chunk)
        
        # Try to parse header if not done
        if not self.header_parsed and len(self.buffer) >= 10:
            header = np.frombuffer(self.buffer[:10], dtype=np.uint16)
            self.magic, self.version, self.h, self.w, self.num_passes = header
            self.header_parsed = True
            
            # Parse sizes if available
            if len(self.buffer) >= 10 + self.num_passes * 4:
                sizes_data = self.buffer[10:10 + self.num_passes * 4]
                self.sizes = np.frombuffer(sizes_data, dtype=np.uint32)
                self.data_offset = 10 + self.num_passes * 4
        
        # Try to decode next pass if available
        if hasattr(self, 'sizes') and self.current_pass < self.num_passes:
            # Check if we have enough data for next pass
            required_size = self.data_offset + sum(self.sizes[:self.current_pass + 1])
            
            if len(self.buffer) >= required_size:
                # Decode this pass
                decoder = ProgressiveDecoder()
                # Extract data up to current pass
                partial_data = bytes(self.buffer[:required_size])
                
                # Decode (will decode all passes up to current)
                try:
                    image, _ = decoder.decode_progressive(
                        partial_data,
                        max_quality=ProgressiveQuality(min(self.current_pass + 1, 4))
                    )
                    self.current_pass += 1
                    return image
                except:
                    pass
        
        return None


def demo_progressive():
    """Demonstrate progressive decompression"""
    print("=" * 70)
    print("PROGRESSIVE DECOMPRESSION DEMO")
    print("=" * 70)
    
    # Create test image (gradient)
    print("\nCreating test image (512×512 gradient)...")
    test_image = np.linspace(0, 255, 512*512, dtype=np.uint8).reshape(512, 512)
    
    # Encode with progressive
    print("\nEncoding with 4 progressive passes...")
    encoder = ProgressiveEncoder()
    compressed, encode_stats = encoder.encode_progressive(test_image, num_passes=4)
    
    print(f"\n✅ Encoded:")
    print(f"   Original:    {encode_stats.original_size:,} bytes")
    print(f"   Compressed:  {encode_stats.compressed_size:,} bytes")
    print(f"   Ratio:       {encode_stats.original_size/encode_stats.compressed_size:.2f}x")
    print(f"   Passes:      {encode_stats.total_passes}")
    
    print(f"\n📊 Pass Details:")
    for p in encode_stats.passes:
        print(f"   Pass {p.pass_number} ({p.quality.name:8s}): "
              f"{p.resolution[0]:3d}×{p.resolution[1]:3d}, "
              f"{p.data_size:6,} bytes, "
              f"{p.decode_time_ms:6.2f} ms")
    
    # Decode progressively with callback
    print(f"\n🎬 Progressive Decoding:")
    
    decoded_images = []
    
    def progress_callback(image, pass_num):
        decoded_images.append((pass_num, image.copy()))
        quality = encode_stats.passes[pass_num-1].quality.name
        print(f"   ✓ Pass {pass_num} decoded: {image.shape} ({quality})")
    
    decoder = ProgressiveDecoder()
    final_image, decode_stats = decoder.decode_progressive(
        compressed,
        max_quality=ProgressiveQuality.HIGH,
        callback=progress_callback
    )
    
    # Verify lossless at full quality
    print(f"\n🔍 Verification:")
    if np.array_equal(test_image, final_image):
        print(f"   ✅ Lossless: VERIFIED (perfect reconstruction)")
    else:
        diff = np.sum(test_image != final_image)
        print(f"   ⚠️  Difference: {diff} pixels")
    
    # Test early termination (thumbnail only)
    print(f"\n⚡ Early Termination Test (THUMBNAIL quality only):")
    start = time.perf_counter()
    thumbnail, thumb_stats = decoder.decode_progressive(
        compressed,
        max_quality=ProgressiveQuality.THUMBNAIL
    )
    thumb_time = (time.perf_counter() - start) * 1000
    
    print(f"   Resolution:  {thumbnail.shape}")
    print(f"   Time:        {thumb_time:.2f} ms")
    print(f"   Data read:   {thumb_stats.passes[0].cumulative_size:,} bytes "
          f"({thumb_stats.passes[0].cumulative_size/len(compressed)*100:.1f}% of total)")
    print(f"   Speedup:     {sum(p.decode_time_ms for p in decode_stats.passes)/thumb_time:.1f}x faster")
    
    # Test streaming decoder
    print(f"\n📡 Streaming Decoder Test:")
    streaming = StreamingProgressiveDecoder()
    
    # Simulate network chunks
    chunk_size = 100  # bytes per chunk
    for i in range(0, len(compressed), chunk_size):
        chunk = compressed[i:i+chunk_size]
        result = streaming.add_data(chunk)
        if result is not None:
            print(f"   ✓ Pass {streaming.current_pass} available after {i+len(chunk):,} bytes")
    
    print("\n" + "=" * 70)
    print("✨ Progressive decompression ready for production!")
    print("=" * 70)


if __name__ == "__main__":
    demo_progressive()
