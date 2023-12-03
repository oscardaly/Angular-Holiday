/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', 'sans'],
      },
      backgroundImage: {
        'dashboard': "url('../src/assets/background.jpg')"
      }
    },
  },
  plugins: [require("daisyui")],
}

