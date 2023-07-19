react env = javascript transpiler and bundler
transpiler = convert javascript to older version of javascript
bundler = combine all javascript files into one file
babel is a transpiler
webpack = bundler

setup based on this video:
https://www.youtube.com/watch?v=h3LpsM42s5o&ab_channel=WittCode

setup:
npm init
npm install react
npm install react-dom
npm install webpack --save-dev
npm install webpack-cli --save-dev
npm install webpack-dev-server --save-dev # for live reload
npm install @babel/core --save-dev
npm install babel-loader --save-dev
npm install @babel/preset-react --save-dev
npm install @babel/preset-env --save-dev
npm install html-webpack-plugin --save-dev

commands:
npm run start
npm run build
