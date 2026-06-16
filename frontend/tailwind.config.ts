import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: { extend: { colors: { brand: { DEFAULT: "#635bff", dark: "#4438ca" } } } },
  plugins: [],
};
export default config;
