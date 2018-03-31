import * as webpack from "webpack";
import * as path from "path";

const rules: webpack.NewUseRule[] = [
  {
    test: /\.tsx?$/,
    exclude: /node_modules/,
    use: { loader: 'ts-loader' },
  },
  {
    test: /\.css$/,
    use: [
      {
        loader: "css-loader"
      }
    ],
    include: /node_modules/
  }
]

const config: webpack.Configuration = {
  mode: 'development',
  entry: path.join(__dirname, './app/app.tsx'),
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, 'dist')
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js']
  },
  module: { rules }
};

export default config;