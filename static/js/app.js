import React, { Component } from 'react';
import { render } from 'react-dom';
import { Router, Switch, Route, browserHistory, Link } from 'react-router';
import { Button, Col } from 'react-bootstrap';
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

class Diff extends Component {
  constructor() {
    super()
    this.state = {
      files: [],
      left_content: null,
      right_content: null,
      left_filename: null,
      right_filename: null
    }
  }

  onDrop(files) {
    if (this.state.files) {
      files = Array.concat(this.state.files, files);
    }

    this.setState({
      files: files
    });
  }

  doCompare() {
    console.log('ho')
    console.log(this.state.files)
    //return;

    var formData = new FormData();
    formData.append('file[0]', this.state.files[0]);
    formData.append('file[1]', this.state.files[1]);

    fetch('/diff/compare', {
      method: 'POST',
      body: formData
    }).then(response => response.json())
    .then(data => {
      // aaa
      console.log(data);
      this.setState({
        left_content: data.left_result,
        right_content: data.right_result,
        left_filename: data.left_filename,
        right_filename: data.right_filename
      });
    });
  }

  render() {
    return (
      <div>
        <Col sm={12} md={6}>
          <Dropzone
              accept="text/*, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              onDrop={this.onDrop.bind(this)}
              multiple >
            {this.state.files.length > 0 ? <div>
              <div>Ready to upload {this.state.files.length} files...</div>
              <div>{this.state.files.map((file) => <div>{file.name}</div> )}</div>
            </div> : <p>Try dropping some files here, or click to select files to upload.</p>}
          </Dropzone>
          <Button onClick={this.doCompare.bind(this)}>
            Compare
          </Button>
        </Col>
        <Col sm={6} md={3}>
          <div>{this.state.left_filename}</div>
          <div dangerouslySetInnerHTML={{__html: this.state.left_content}}></div>
        </Col>
        <Col sm={6} md={3}>
          <div>{this.state.right_filename}</div>
          <div dangerouslySetInnerHTML={{__html: this.state.right_content}}></div>
        </Col>
      </div>
    );
  }
}

render((
  <Router history={createBrowserHistory()}>
    <Switch>
      <Route exact path="/" component={App} />
      <Route path="/pdfconv" component={PdfConv} />
      <Route path="/diff" component={Diff} />
    </Switch>
  </Router>
), document.querySelector('#root'));
