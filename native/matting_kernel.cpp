// matting_kernel.cpp — CUDA bilateral-guided matting for ai-headshot-studio.
// Build: cmake -B build -DAHS_CUDA=ON && cmake --build build --config Release
#include <cuda_runtime.h>
#include <cstdint>

__global__ void bilateral_guided_kernel(
    const float* __restrict__ guide,
    const float* __restrict__ src,
    float* __restrict__ dst,
    int width, int height, int radius, float sigma_s, float sigma_r) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x >= width || y >= height) return;

    float wsum = 0.f, acc = 0.f;
    float g0 = guide[y * width + x];
    for (int dy = -radius; dy <= radius; ++dy) {
        for (int dx = -radius; dx <= radius; ++dx) {
            int nx = min(max(x + dx, 0), width - 1);
            int ny = min(max(y + dy, 0), height - 1);
            float g = guide[ny * width + nx];
            float ws = expf(-(dx * dx + dy * dy) / (2.f * sigma_s * sigma_s));
            float wr = expf(-((g - g0) * (g - g0)) / (2.f * sigma_r * sigma_r));
            float w = ws * wr;
            acc += w * src[ny * width + nx];
            wsum += w;
        }
    }
    dst[y * width + x] = acc / fmaxf(wsum, 1e-6f);
}

extern "C" int ahs_matting_apply(
    const float* guide, const float* src, float* dst,
    int width, int height, int radius, float sigma_s, float sigma_r) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    bilateral_guided_kernel