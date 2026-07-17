export default {
  extends: ['stylelint-config-standard'],
  ignoreFiles: ['src/static_dist/**'],
  rules: {
    'selector-class-pattern': '^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$',
  },
};
