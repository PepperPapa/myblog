module.exports = {
  entry: "./css/sign.scss",
  output: {
    filename: "./css/sign.css"
  },
  module: {
    loaders: [
      {
        test: /\.scss$/,
        loader: 'style!css!sass'
      }
    ]
  }
}
