/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        stengazeta: ["Stengazeta", "sans-serif"],
        roboto: ["Roboto", "sans-serif"],
        bartina: ["Bartina", "sans-serif"],
      },
    },
  },
  plugins: [],
};
