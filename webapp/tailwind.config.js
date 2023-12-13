/** @type {import('tailwindcss').Config} */
import colors from "tailwindcss/colors";

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
      },
      screens: {
        smaller: "876px",
        normal: "1312px",
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1280px",
        "template-modal": "1395px",
        "template-modal-small": "1100px"
      },
      extend: {
        fontSize: {
          48: "48px"
        },
        spacing: {
          88: "88px"
        },
        maxWidth: {
          "normal-max-width": "1280px",
          "smaller-max-width": "844px"
        }
      },
      minWidth: {
        "dynamic-min-width": "calc(100vw - 32px)",
        "fixed-smaller-min-width": "844px",
        "fixed-normal-min-width": "1280px"
      },
      minHeight: {
        "screen-without-padding": "calc(100vh - 136px)"
      },
      colors: {
        white: colors.white,
        lightgrey: colors.gray,
        red: colors.red,
        black: colors.black,
        transparent: colors.transparent,
      }
    },
  },
  plugins: [require("daisyui")],
}

