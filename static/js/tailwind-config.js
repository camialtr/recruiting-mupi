window.tailwind = window.tailwind || {};
window.tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                sans: ['Space Grotesk', 'sans-serif'],
                display: ['Monument Extended', 'sans-serif'],
            },
            colors: {
                background: 'rgb(var(--color-background) / <alpha-value>)',
                surface: 'rgb(var(--color-surface) / <alpha-value>)',
                'surface-contrast': 'rgb(var(--color-surface-contrast) / <alpha-value>)',
                border: 'rgb(var(--color-border) / <alpha-value>)',
                primary: 'rgb(var(--color-primary) / <alpha-value>)',
                secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
                accent: {
                    DEFAULT: 'rgb(var(--color-accent) / <alpha-value>)',
                    light: 'rgb(var(--color-accent-light) / <alpha-value>)',
                    dark: 'rgb(var(--color-accent-dark) / <alpha-value>)',
                },
                'accent-ice': {
                    DEFAULT: 'rgb(var(--color-accent-ice) / <alpha-value>)',
                    light: 'rgb(var(--color-accent-ice-light) / <alpha-value>)',
                    dark: 'rgb(var(--color-accent-ice-dark) / <alpha-value>)',
                },
            },
            borderRadius: {
                'xl': '1rem',
                '2xl': '1.5rem',
                '3xl': '2rem',
            }
        }
    }
}
