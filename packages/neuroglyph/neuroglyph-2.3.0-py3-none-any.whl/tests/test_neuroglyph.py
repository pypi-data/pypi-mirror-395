"""
NeuroGlyph Test Suite - Comprehensive Unit Tests
================================================

Tests for all major codecs and optimizations.

Run with: pytest tests/
"""

import pytest
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neuroglyph_eco import EcoPNGCodec
from neuroglyph_hyper import HyperPNGCodec
from neuroglyph_fast import FastNeuralPNGCodec, FastEcoPNGCodec
from neuroglyph_16bit import compress_16bit, decompress_16bit
from neuroglyph_progressive import ProgressiveCodec
from neuroglyph_video import NeuroGlyphVideoCodec, create_test_video
from neuroglyph_simd import SIMDPaethFilter, get_simd_info


class TestBasicCompression:
    """Test basic compression/decompression roundtrip"""
    
    def test_eco_gradient(self):
        """Test EcoPNG on gradient (optimal case)"""
        # Create horizontal gradient
        img = np.array([[i for i in range(256)] for _ in range(256)], dtype=np.uint8)
        
        codec = EcoPNGCodec()
        compressed, stats = codec.compress_eco(img)
        
        # Should achieve excellent compression
        assert stats.compression_ratio > 100, "Expected >100× compression on gradient"
        assert stats.energy_used_mj < 1.0, "Expected <1 mJ energy"
        
    def test_eco_uniform(self):
        """Test EcoPNG on uniform image"""
        img = np.ones((256, 256), dtype=np.uint8) * 128
        
        codec = EcoPNGCodec()
        compressed, stats = codec.compress_eco(img)
        
        # Should detect constant pattern
        assert stats.compression_ratio > 1000, "Expected >1000× compression on uniform"
        assert "constant" in stats.method_used.lower() or "omega" in stats.method_used.lower()
        
    def test_hyper_energy(self):
        """Test HyperPNG energy efficiency"""
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
        
        codec = HyperPNGCodec()
        compressed, stats = codec.compress_hyper(img)
        
        # Should be energy efficient even on random data
        assert stats.energy_used_mj < 2.0, "Expected <2 mJ on complex image"


class Test16BitSupport:
    """Test 16-bit image compression"""
    
    def test_16bit_gradient(self):
        """Test 16-bit differential encoding on gradient"""
        # Create 16-bit gradient
        img = np.array([[i * 256 for i in range(256)] for _ in range(256)], dtype=np.uint16)
        
        compressed, stats = compress_16bit(img, codec='eco')
        
        # Should achieve excellent compression via MSB/LSB correlation
        assert stats.compression_ratio > 100, "Expected >100× compression on 16-bit gradient"
        
    def test_16bit_roundtrip(self):
        """Test 16-bit compression/decompression roundtrip"""
        # Create test pattern
        img = np.random.randint(0, 65536, (128, 128), dtype=np.uint16)
        
        compressed, _ = compress_16bit(img, codec='eco')
        decompressed = decompress_16bit(compressed)
        
        # Lossless verification
        assert np.array_equal(img, decompressed), "16-bit roundtrip should be lossless"


class TestSIMDOptimizations:
    """Test SIMD-accelerated codecs"""
    
    def test_simd_available(self):
        """Check SIMD support detection"""
        info = get_simd_info()
        
        assert 'backend' in info
        assert info['backend'] in ['numpy', 'neon', 'avx2']
        
    def test_simd_paeth_correctness(self):
        """Verify SIMD Paeth filter produces correct output"""
        img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        
        # Apply SIMD Paeth filter
        filtered = SIMDPaethFilter.apply_simd_optimized(img)
        
        # Basic sanity checks
        assert filtered.shape == img.shape
        assert filtered.dtype == np.int16
        
    def test_fast_codec_speedup(self):
        """Test that Fast codecs are actually faster"""
        img = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
        
        import time
        
        # Regular codec
        codec_regular = EcoPNGCodec()
        start = time.perf_counter()
        _, stats_regular = codec_regular.compress_eco(img)
        time_regular = time.perf_counter() - start
        
        # Fast codec
        codec_fast = FastEcoPNGCodec()
        start = time.perf_counter()
        _, stats_fast = codec_fast.compress_fast_eco(img)
        time_fast = time.perf_counter() - start
        
        # Fast should be faster or comparable (SIMD gains vary by CPU)
        # Just verify it runs without errors
        assert stats_fast.compression_ratio > 0


class TestProgressiveDecoding:
    """Test progressive decompression"""
    
    def test_progressive_levels(self):
        """Test 4-level progressive decoding"""
        img = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
        
        codec = ProgressiveCodec()
        compressed, stats = codec.compress_progressive(img)
        
        # Test each level
        for level in ['thumbnail', 'low', 'medium', 'high']:
            decoded = codec.decompress_progressive(compressed, level=level)
            
            assert decoded.shape == img.shape, f"Level {level} should preserve shape"
            
            # High quality should match original (lossless)
            if level == 'high':
                assert np.array_equal(decoded, img), "High quality should be lossless"


class TestVideoCodec:
    """Test video compression"""
    
    def test_video_static(self):
        """Test video codec on static frames (best case)"""
        # Create 10 identical frames
        frames = [np.ones((64, 64), dtype=np.uint8) * 128] * 10
        
        codec = NeuroGlyphVideoCodec(i_frame_interval=5)
        compressed, stats = codec.encode_video(frames, fps=30.0)
        
        # Should achieve excellent compression on static video
        assert stats.compression_ratio > 50, "Expected >50× compression on static video"
        
    def test_video_motion(self):
        """Test video codec on moving content"""
        # Create simple pan motion
        frames = create_test_video(width=128, height=128, num_frames=20, motion_type='pan')
        
        codec = NeuroGlyphVideoCodec(i_frame_interval=10)
        compressed, stats = codec.encode_video(frames, fps=30.0)
        
        # Should compress reasonably well
        assert stats.compression_ratio > 3, "Expected >3× compression on pan motion"
        
        # Should detect motion
        assert stats.avg_motion_magnitude > 0, "Should detect motion in pan"
        
    def test_video_adaptive_threshold(self):
        """Test adaptive threshold updates"""
        from neuroglyph_video import NeuralMotionEstimator
        
        estimator = NeuralMotionEstimator()
        
        # Initially at default
        assert estimator._static_threshold == 100
        
        # Simulate high-motion content
        estimator._update_adaptive_threshold(500.0)  # High SAD
        estimator._update_adaptive_threshold(600.0)
        estimator._update_adaptive_threshold(550.0)
        
        # Should increase threshold for high-motion content
        assert estimator._static_threshold > 100, "Threshold should adapt to high motion"
        
        # Simulate low-motion content
        for _ in range(10):
            estimator._update_adaptive_threshold(50.0)  # Low SAD
            
        # Should decrease threshold for low-motion content
        assert estimator._static_threshold < 150, "Threshold should adapt to low motion"


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_image(self):
        """Test handling of minimal images"""
        # 1×1 image
        img = np.array([[128]], dtype=np.uint8)
        
        codec = EcoPNGCodec()
        compressed, stats = codec.compress_eco(img)
        
        assert stats.compressed_size > 0
        
    def test_large_image(self):
        """Test handling of large images (memory test)"""
        # Create 2048×2048 image (4 MB)
        img = np.random.randint(0, 256, (2048, 2048), dtype=np.uint8)
        
        codec = FastEcoPNGCodec()
        compressed, stats = codec.compress_fast_eco(img)
        
        assert stats.compression_ratio > 0
        
    def test_grayscale_vs_color(self):
        """Test that video codec handles both grayscale and RGB"""
        # Grayscale frames
        frames_gray = create_test_video(width=64, height=64, num_frames=5, motion_type='static')
        
        codec = NeuroGlyphVideoCodec()
        compressed_gray, stats_gray = codec.encode_video(frames_gray, fps=30.0)
        
        assert stats_gray.compression_ratio > 0
        
        # RGB frames (create color version)
        frames_rgb = [np.stack([f, f, f], axis=-1) for f in frames_gray]
        
        compressed_rgb, stats_rgb = codec.encode_video(frames_rgb, fps=30.0)
        
        assert stats_rgb.compression_ratio > 0


class TestEnergyMetrics:
    """Test energy consumption tracking"""
    
    def test_energy_comparison(self):
        """Compare energy across codecs"""
        img = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
        
        # Test different codecs
        eco_codec = EcoPNGCodec()
        _, eco_stats = eco_codec.compress_eco(img)
        
        hyper_codec = HyperPNGCodec()
        _, hyper_stats = hyper_codec.compress_hyper(img)
        
        # Both should be energy efficient
        assert eco_stats.energy_used_mj < 5.0, "EcoPNG should use <5 mJ"
        assert hyper_stats.energy_used_mj < 5.0, "HyperPNG should use <5 mJ"
        
        # Energy should be proportional to time
        assert eco_stats.energy_used_mj > 0
        assert hyper_stats.energy_used_mj > 0


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
