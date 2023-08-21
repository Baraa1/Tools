/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/base.html",
            "../templates/**/*.html",
            "./js/*/.js",
            "./node_modules/flowbite/**/*.js",
],
  theme: {
    screens: {
      sm: "480px",
      md: "768px",
      lg: "976px",
      xl: "1440px",
    },
    extend: {
      colors: {
        ytText: "#000000",
        ytBackground: "#f7f7f7",
        ytPrimary: "#000000",
        ytSecondary: "#FFF0F0",
        ytAccent: "#ff0000",
      },
    },
    container: {
      center: true,
      margin:0,
      width:"100%",
    },
  },
  plugins: [
    'prettier-plugin-tailwindcss',
    require('flowbite/plugin'),
  ],

}

