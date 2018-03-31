var path = require('path');

module.exports = {
  plugins: [
    // your custom plugins
  ],
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
    modules: [ path.resolve(__dirname, "app"), 'node_modules' ]
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loaders: ["ts-loader"],
      },
      {
        test: /\.scss$/,
        loaders: ["style-loader", "css-loader", "sass-loader"],
      }
    ],
  },
};
