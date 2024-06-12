/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    env: {
        NEXT_PUBLIC_API_HOST: process.env.NEXT_PUBLIC_API_HOST,
        NEXT_PUBLIC_API_PORT: process.env.NEXT_PUBLIC_API_PORT,
        NEXT_PUBLIC_AUTH_PASS: process.env.NEXT_PUBLIC_AUTH_PASS,
    }
};

export default nextConfig;