// jest.config.js
module.exports = {
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['<rootDir>/static/js/tests/setupTests.js'],
    moduleNameMapper: {
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
    },
    transform: {
      '^.+\\.(js|jsx)$': 'babel-jest'
    },
    testMatch: [
      '**/__tests__/**/*.js?(x)',
      '**/?(*.)+(spec|test).js?(x)'
    ],
    testPathIgnorePatterns: [
      '/node_modules/',
      '/staticfiles/'
    ],
    collectCoverageFrom: [
      'static/js/**/*.js',
      '!static/js/tests/**/*.js'
    ],
    coverageThreshold: {
      global: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80
      }
    },
    transformIgnorePatterns: [
      '/node_modules/(?!(jest-test|@testing-library)/)'
    ]
  };