/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/inference",
        destination: "http://backend_app:8000/inference",
      },
    ];
  },
};

export default nextConfig;
