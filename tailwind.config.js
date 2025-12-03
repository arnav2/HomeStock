/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./electron/renderer/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#ebf5fb',
          100: '#d6eaf8',
          500: '#3498db',
          600: '#2980b9',
          700: '#21618c',
        },
        sidebar: {
          bg: '#2c3e50',
          hover: '#34495e',
          active: '#3498db',
        },
      },
    },
  },
  plugins: [],
}

