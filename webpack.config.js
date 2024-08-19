const path = require('path');

module.exports = {
    entry: './static/js/index.js',
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: 'bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: { presets: ['@babel/env','@babel/preset-react'] }
                },
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    mode: 'development',
};
