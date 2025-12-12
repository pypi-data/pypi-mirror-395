module.exports = {
    presets: [
        ["@babel/preset-env", {targets: {node: "current"}}],
        ["@babel/preset-react", {runtime: "automatic"}],
        "@babel/preset-typescript",
    ],
    plugins: [
        "transform-class-properties",
        [
            "@babel/plugin-transform-runtime",
            {
                regenerator: true
            }
        ]
    ]
}
