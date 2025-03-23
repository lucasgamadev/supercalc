import htmlPlugin from 'eslint-plugin-html';

export default [
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      indent: ['error', 2],
      'linebreak-style': ['error', 'windows'],
      quotes: ['error', 'single'],
      semi: ['error', 'always']
    }
  },
  {
    files: ['**/*.html'],
    plugins: {
      html: htmlPlugin
    }
  }
];