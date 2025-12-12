import type { Config } from 'jest';

// https://jestjs.io/docs/configuration
const config: Config = {
    // bail: true, // bail after first failure
    globalSetup: "<rootDir>/lino_react/react/testSetup/setupJEST.js",
    globalTeardown: "<rootDir>/lino_react/react/testSetup/teardownJEST.js",
    testEnvironment: "<rootDir>/lino_react/react/testSetup/testEnvironment.js",
    moduleFileExtensions: ["js", "jsx", "ts", "tsx"],
    moduleNameMapper: {
        '^.+\\.(css|less)$': '<rootDir>/CSSStub.js'
    },
    preset: 'jest-puppeteer',
    // testRegex: "(/__tests__/.*|(\\.|/)(test|spec))\\.(jsx?|tsx?|js?|ts?)$",
    roots: ["<rootDir>/lino_react/react/components"],
    setupFilesAfterEnv: ["<rootDir>/lino_react/react/testSetup/setupTests.ts"],
    testMatch: [`<rootDir>/lino_react/react/components/__tests__/${process.env.BASE_SITE}/*.ts`],
    testTimeout: 300000,
    transform: {
        '^.+\\.(ts|tsx)?$': 'ts-jest',
        '^.+\\.(js|jsx)$': 'babel-jest',
    },
    transformIgnorePatterns: [
        "node_modules/(?!(query-string|decode-uri-component|split-on-first|filter-obj)/)"
    ],
    verbose: true,
}

export default config;
