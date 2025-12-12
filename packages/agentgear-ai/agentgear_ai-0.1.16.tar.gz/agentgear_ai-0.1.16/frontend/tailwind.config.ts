import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f7ff",
          100: "#dcecff",
          200: "#b6d7ff",
          300: "#89beff",
          400: "#5296f3",
          500: "#3174d9",
          600: "#245ab0",
          700: "#1f4a8d",
          800: "#1e3e73",
          900: "#1c345f"
        }
      }
    }
  },
  plugins: []
};

export default config;
