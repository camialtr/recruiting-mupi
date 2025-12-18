tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        background: 'rgb(var(--color-background) / <alpha-value>)',
        surface: 'rgb(var(--color-surface) / <alpha-value>)',
        border: 'rgb(var(--color-border) / <alpha-value>)',
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
        accent: 'rgb(var(--color-accent) / <alpha-value>)',
        'accent-olive': 'rgb(var(--color-accent-olive) / <alpha-value>)',
        'accent-muted': 'rgb(var(--color-accent-muted) / <alpha-value>)',
        'accent-denied': 'rgb(var(--color-accent-denied) / <alpha-value>)',
        'accent-ice': 'rgb(var(--color-accent-ice) / <alpha-value>)',
        'accent-darker': 'rgb(var(--color-accent-darker) / <alpha-value>)',
        'accent-grayer': 'rgb(var(--color-accent-grayer) / <alpha-value>)',
      }
    }
  }
}
