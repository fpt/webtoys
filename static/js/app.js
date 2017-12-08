import React, { Component } from 'react';
import { render } from 'react-dom';
import { Router, Switch, Route, browserHistory, Link } from 'react-router';
import Dropzone from 'react-dropzone'

import createBrowserHistory from 'history/createBrowserHistory';

class App extends Component {
  render() {
    return (
      <h1>Hello, Worldo!</h1>
    );
  }
}

class PdfConv extends Component {
  constructor() {
    super()
    this.state = { files: [] }
  }

  onDrop(files) {
    this.setState({
      files
    });
  }

  render() {
    return (
      <div>
        <h1>Hello, Pdfconv!!</h1>
        <Dropzone onDrop={this.onDrop.bind(this)}>
          <p>Try dropping some files here, or click to select files to upload.</p>
        </Dropzone>
      </div>
    );
  }
}

render((
  <Router history={createBrowserHistory()}>
    <Switch>
      <Route exact path="/" component={App} />
      <Route path="/pdfconv" component={PdfConv} />
    </Switch>
  </Router>
), document.querySelector('#root'));
