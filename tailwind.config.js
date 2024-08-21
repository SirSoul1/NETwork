module.exports = {
  content: [
    './templates/**/*.html',
    './blog/templates/**/*.html',
    './users/templates/**/*.html',
    './mysite/templates/**/*.html',
    // Add any other paths where you might use Tailwind classes
  ],
  theme: {
    extend: {
      keyframes: {
        'zoom-in': {
          '0%': {
            transform: 'scale(0)',
            opacity: '0',
          },
          '100%': {
            transform: 'scale(1)',
            opacity: '1',
          },
        },
      },
      animation: {
        'zoom-in': 'zoom-in 0.5s ease-out',
      },
    },
  },
  plugins: [],
}
