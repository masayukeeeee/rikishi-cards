import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  images: {
    domains: ['www.sumo.or.jp'], // 外部画像ホストを追加
  },
};

export default nextConfig;
