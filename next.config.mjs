/** @type {import('next').NextConfig} */
const nextConfig = {
  // Image Optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Production Optimizations
  productionBrowserSourceMaps: false,

  experimental: {
    optimizePackageImports: ["@heroicons/react"],
  },

  // Turbopack configuration (Next.js 16+ default)
  turbopack: {
    resolveExtensions: ['.ts', '.tsx', '.js', '.jsx'],
  },

  // Performance
  poweredByHeader: false,

  // Security headers
  headers: async () => {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
        ],
      },
    ];
  },
};

export default nextConfig;
