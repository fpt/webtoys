import React, { Component } from 'react';
import ReactDOM, { render } from 'react-dom';
import { Router, Switch, Route, browserHistory, Link } from 'react-router';
import { Button, Col } from 'react-bootstrap';
import Dropzone from 'react-dropzone'
import ReactHtmlParser, { processNodes, convertNodeToElement, htmlparser2 } from 'react-html-parser';

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


const styles ={
  svg_outer: {
    width:'100%'
  }
};


class Diff extends Component {
  constructor() {
    super()
    this.state = {
      files: [],
      left_content: null,
      right_content: null,
      left_filename: null,
      right_filename: null,
      diff_pairs: null,
      diff_pair_polys: null,
      diff_height: null
    }
  }

  componentDidUpdate() {
    console.log('hogehoge');
    console.log(this.refs);

    // should monitor carefully...
    if (this.state.diff_pairs && !this.state.diff_pair_polys && this.refs) {
      let polys = [];
      let lr = ReactDOM.findDOMNode(this.refs['left-outer']).getBoundingClientRect();
      let rr = ReactDOM.findDOMNode(this.refs['right-outer']).getBoundingClientRect();
      let max_height = 0;
      for (let pair of this.state.diff_pairs) {
        let ra = ReactDOM.findDOMNode(this.refs[pair[0]]).getBoundingClientRect();
        let rb = ReactDOM.findDOMNode(this.refs[pair[1]]).getBoundingClientRect();
        ra.y = ra.y - lr.y;
        rb.y = rb.y - rr.y;
        polys.push({
          key: pair.join(),
          points: [
            0 + ',' + (ra.y),
            30 + ',' + rb.y,
            30 + ',' + (rb.y + rb.height),
            0 + ',' + (ra.y + ra.height)
          ]
        });
        max_height = Math.max(max_height, ra.y + ra.height, rb.y + rb.height)
      }

      this.setState({
        diff_pair_polys: polys,
        diff_height: max_height
      })
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

  _postCompare(formData) {
    return fetch('/diff/compare/test01');
    return fetch('/diff/compare', {
      method: 'POST',
      body: formData
    });
  }

  doCompare() {
    var formData = new FormData();
    formData.append('file[0]', this.state.files[0]);
    formData.append('file[1]', this.state.files[1]);

    this._postCompare(formData)
      .then(response => response.json())
      .then(data => {
        // aaa
        console.log(data);
        this.setState({
          left_content: data.left_result,
          right_content: data.right_result,
          left_filename: data.left_filename,
          right_filename: data.right_filename,
          diff_pairs: data.diff_lines
        });
      });
  }

  render() {
    const left_elts = ReactHtmlParser(this.state.left_content);
    const right_elts = ReactHtmlParser(this.state.right_content);

    var polys = null;
    if (this.state.diff_pair_polys) {
      polys = this.state.diff_pair_polys.map(function(poly){
        return <polygon key={poly.key} fill="red" stroke="blue" strokeWidth="1" 
                        points={poly.points.join(' ')} />
      });
    }
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
        <Col sm={5} md={3} ref="left-outer">
          <div>{this.state.left_filename}</div>
          <div>{ left_elts }</div>
        </Col>
        <Col sm={1}>
          <svg version="1.1" width="30" height={this.state.diff_height} xmlns="http://www.w3.org/2000/svg" style={styles.svg_outer}>
            {polys}
          </svg>
        </Col>
        <Col sm={5} md={3} ref="right-outer">
          <div>{this.state.right_filename}</div>
          <div>{ right_elts }</div>
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

