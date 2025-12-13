import WorkboxPlugin from 'workbox-webpack-plugin';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import TerserPlugin from 'terser-webpack-plugin';
import CssMinimizerPlugin from 'css-minimizer-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';
import webpack from 'webpack';
import path from 'path';
import { fileURLToPath } from 'url';
import process from 'process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// https://github.com/rschristian/babel-plugin-webpack-chain-name-comments/blob/master/index.js


export default (_env, argv) => {
    const isProduction = argv.mode === 'production';

    return {
        // devtool: "inline-source-map",
        devtool: "source-map",
        entry: ["./lino_react/react/index.js"],
        output: {
          filename: (pathData) => {
              return pathData.chunk.name === "main" ? "[name].[contenthash].js" : "main.[name].[contenthash].js"
          },
          chunkFilename: () => {
              return "main.[name].[chunkhash].js";
          },
          path: path.resolve(__dirname, './lino_react/react/static/react'),
          clean: isProduction,
        },
        optimization: {
            minimize: isProduction,
            minimizer: [
                new CssMinimizerPlugin(),
                new TerserPlugin({
                    parallel: true,
                    terserOptions: {
                        compress: {
                            ecma: 2015,
                        },
                    },
                }),
            ],
            runtimeChunk: 'single',
            splitChunks: {
                cacheGroups: {
                    utils: {
                        test: /[\\/]node_modules[\\/](weak-key|classnames|query-string|whatwg-fetch|reconnecting-websocket|abort-controller)[\\/]/,
                        name: "tpdep",
                        chunks: "all"
                    },
                    quill: {
                        test: /[\\/]node_modules[\\/]quill[\\/]/,
                        name: "quill",
                        chunks: "all"
                    },
                    // prStyles: {
                    //     test: /[\\/]node_modules[\\/]primereact.*\.css$/,
                    //     name: "prStyles",
                    //     chunks: "all"
                    // },
                    // styles: {
                    //     test: /\.css$/,
                    //     name: "styles",
                    //     chunks: "all"
                    // },
                    prLocale: {
                        test: /[\\/]node_modules[\\/]primelocale[\\/]/,
                        name: "prLocale",
                        chunks: "all"
                    },
                    prAppRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](toast|button)[\\/]/,
                        name: "prAppRequire",
                        chunks: "all"
                    },
                    prSiteContextRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](progressspinner|progressbar|scrollpanel|overlaypanel|card|dialog|splitbutton)[\\/]/,
                        name: "prSiteContextRequire",
                        chunks: "all"
                    },
                    prLinoBodyRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](selectbutton|dataview|galleria|dropdown|togglebutton)[\\/]/,
                        name: "prLinoBodyRequire",
                        chunks: "all"
                    },
                    prLinoBodyRequireChunk2: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](column|tristatecheckbox|datatable|inputnumber|inputtext|multiselect)[\\/]/,
                        name: "prLinoBodyRequireChunk2",
                        chunks: "all"
                    },
                    prLinoComponentsRequire: {
                        test: /[\\/]node_modules[\\/]primereact[\\/](fileupload|tabview|panel|checkbox|fieldset|password|autocomplete|calendar|contextmenu|utils|splitter|inputswitch|inputtextarea)[\\/]/,
                        name: "prLinoComponentsRequire",
                        chunks: "all"
                    },
                }
            }
        },
        module: {
            rules: [{oneOf: [
                {test: [/\.tsx?$/, /\.ts?$/],
                    use: 'ts-loader',
                    exclude: [/node_modules/, /electron/]},
                {test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
                    loader: 'url-loader',
                    exclude: /node_modules/,
                    options: {
                        limit: 10000,
                        name: '/static/media/[name].[hash:8].[ext]',
                        outputPath: '../../'}},
                {test: /\.(woff|woff2|eot|ttf|otf)/i,
                    type: "asset/resource"},
                {test: /\.(js|jsx|mjs)$/,
                    loader: 'babel-loader',
                    exclude: /node_modules/,
                    options: {
                        cacheDirectory: true,
                        presets: ['@babel/preset-env', '@babel/preset-react']}},
                {test: /\.css$/,
                    use: [
                        'style-loader',
                        {loader: 'css-loader',
                            options: {importLoaders: 1}}]},
                {exclude: [/\.(js|jsx|ts|tsx|mjs|cjs)$/, /\.html$/, /\.json$/],
                    loader: 'file-loader',
                    options: {
                        name: '/static/media/[name].[hash:8].[ext]',
                        outputPath: '../../'}},
            ]}]
        },
        plugins: [
            new webpack.DefinePlugin({
                'LINO_LOGLEVEL': isProduction ? 1 : 2,
            }),
            new WorkboxPlugin.InjectManifest({
                swDest: process.cwd() + '/lino_react/react/config/react/service-worker.js',
                swSrc: process.cwd() + '/lino_react/react/components/custom-service-worker.js',
                include: ['/static/react/main.js'],
                exclude: ['/main.js'],
                maximumFileSizeToCacheInBytes: 5000000
            }),
            new HtmlWebpackPlugin({
                filename: "./../../config/react/main.html",
                inject: false,
                minify: false,
                template: "./lino_react/react/components/index.html",
                templateParameters: (_htmlWebpackPlugin, assetInfo) => {
                    let injects = "";
                    assetInfo.js.forEach((script) => {
                        injects += `<script defer src="{{site.build_static_url('react/${script.split("/").slice(-1)[0]}')}}"></script>\n`
                    });
                    return {
                        webpack_comment: `<!--
        ATTENTION: This content is put here by webpack
        DO NOT MODIFY!
        Edit (lino_react/react/components/index.html) instead
        and run "npm run build".\n-->`,
                        webpack_injects: injects
                    }
                }
            }),
            new CopyWebpackPlugin({
                patterns: [
                    {
                        from: './node_modules/primereact/resources/themes/',
                        to: 'themes/',
                    },
                ],
            }),
        ],
        resolve: {
            alias: {
                'react-dom$': 'react-dom/profiling',
                'scheduler/tracing': 'scheduler/tracing-profiling',
            },
            extensions: [
                '.tsx', '.js', '.json', '.html', '.ts', '.jsx', '.css', '.mjs',
                '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.woff', '.woff2', '.eot',
                '.ttf', '.otf'
            ],
            extensionAlias: {
                '.js': ['.ts', '.tsx', '.js', '.jsx', '.mjs']
            },
            conditionNames: ['import', 'module', 'default']
        }
    };
}
