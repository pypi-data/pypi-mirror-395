#!/usr/bin/env python3
"""
Test 16-bit compression with all codecs
"""

import numpy as np
from neuroglyph_16bit import create_16bit_codec, Bit16Adapter
from PIL import Image

def create_test_images():
    """Create various 16-bit test images"""
    tests = []
    
    # 1. Linear gradient (simple pattern)
    gradient = np.linspace(0, 65535, 512*512, dtype=np.uint16).reshape(512, 512)
    tests.append(("Gradient 512x512", gradient))
    
    # 2. Constant image (trivial)
    constant = np.full((256, 256), 32768, dtype=np.uint16)
    tests.append(("Constant 256x256", constant))
    
    # 3. Checkerboard (high frequency)
    checker = np.zeros((256, 256), dtype=np.uint16)
    checker[::2, ::2] = 65535
    checker[1::2, 1::2] = 65535
    tests.append(("Checkerboard 256x256", checker))
    
    # 4. Medical image simulation (smooth with noise)
    np.random.seed(42)
    base = np.linspace(0, 65535, 512*512).reshape(512, 512)
    noise = np.random.randint(-1000, 1000, (512, 512), dtype=np.int32)
    medical = np.clip(base + noise, 0, 65535).astype(np.uint16)
    tests.append(("Medical-like 512x512", medical))
    
    # 5. Astronomical image (sparse bright spots)
    astro = np.random.randint(0, 100, (512, 512), dtype=np.uint16)
    # Add some "stars"
    for _ in range(50):
        x, y = np.random.randint(0, 512, 2)
        astro[x:x+5, y:y+5] = 65535
    tests.append(("Astronomical 512x512", astro))
    
    return tests


def test_codec(codec_name: str, test_images):
    """Test a specific codec on all images"""
    print(f"\n{'='*70}")
    print(f"Testing: {codec_name.upper()} Codec")
    print(f"{'='*70}")
    
    try:
        codec = create_16bit_codec(codec_name)
        
        for name, image in test_images:
            print(f"\n{name}:")
            print("-" * 50)
            
            original_size = image.nbytes
            
            # Compress
            if codec_name == 'eco':
                compressed, stats = codec.compress_eco(image, use_differential=True)
            elif codec_name == 'hyper':
                compressed, stats = codec.compress_hyper(image, use_differential=True)
            elif codec_name == 'neural':
                compressed, stats = codec.compress(image, use_differential=True)
            
            # Display results
            print(f"  Original:      {stats.original_size:,} bytes")
            print(f"  Compressed:    {stats.compressed_size:,} bytes")
            print(f"  Ratio:         {stats.compression_ratio:.2f}x")
            print(f"  High byte:     {stats.high_byte_size:,} bytes")
            print(f"  Low byte:      {stats.low_byte_size:,} bytes")
            if stats.correlation_gain > 0:
                print(f"  Correlation:   +{stats.correlation_gain*100:.1f}%")
            print(f"  Energy:        {stats.energy_mj:.3f} mJ")
            
            # Verify lossless
            if codec_name == 'neural':
                decompressed = codec.decompress(compressed)
                if np.array_equal(image, decompressed):
                    print(f"  ✅ Lossless: VERIFIED")
                else:
                    print(f"  ❌ Lossless: FAILED")
                    diff = np.sum(image != decompressed)
                    print(f"     Different pixels: {diff}")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")


def test_bit_splitting():
    """Test the basic 16-bit splitting and merging"""
    print("\n" + "="*70)
    print("Testing 16-bit Split/Merge Operations")
    print("="*70)
    
    adapter = Bit16Adapter()
    
    # Test case 1: Full range
    test = np.array([[0, 255, 256, 65535]], dtype=np.uint16)
    high, low = adapter.split_16bit(test)
    reconstructed = adapter.merge_16bit(high, low)
    
    print(f"\nTest values: {test[0]}")
    print(f"High bytes:  {high[0]}")
    print(f"Low bytes:   {low[0]}")
    print(f"Reconstructed: {reconstructed[0]}")
    
    if np.array_equal(test, reconstructed):
        print("✅ Split/Merge: PASSED")
    else:
        print("❌ Split/Merge: FAILED")
    
    # Test case 2: Random data
    np.random.seed(42)
    random_16bit = np.random.randint(0, 65536, (100, 100), dtype=np.uint16)
    high, low = adapter.split_16bit(random_16bit)
    reconstructed = adapter.merge_16bit(high, low)
    
    if np.array_equal(random_16bit, reconstructed):
        print("✅ Random data: PASSED")
    else:
        print("❌ Random data: FAILED")


if __name__ == "__main__":
    print("="*70)
    print(" 16-BIT IMAGE COMPRESSION BENCHMARK")
    print("="*70)
    
    # Test basic operations
    test_bit_splitting()
    
    # Create test images
    print("\nCreating test images...")
    test_images = create_test_images()
    print(f"✅ Created {len(test_images)} test images")
    
    # Test each codec
    for codec_name in ['neural', 'eco', 'hyper']:
        test_codec(codec_name, test_images)
    
    print("\n" + "="*70)
    print("✨ 16-bit compression testing complete!")
    print("="*70)
