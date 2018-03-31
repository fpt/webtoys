import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';
import { PageHeader, Button, Col, Breadcrumb, ToggleButtonGroup, ToggleButton } from 'react-bootstrap';
import Dropzone from 'react-dropzone';
import { lifecycle, withState } from 'recompose';

import { HttpHeaderView } from './components/httpheader';
import { BaseConvView } from './components/baseconv';
import { XmlBeautifyView } from './components/xmlbeautify';
import { UrlEncView } from './components/urlenc';
import { IdGenView } from './components/idgen';


const Header = () => {
  return (
    <div>
      <PageHeader>WebToys</PageHeader>
      <Breadcrumb>
        <Breadcrumb.Item href="/">Home</Breadcrumb.Item>
        <Breadcrumb.Item active>HTTP Header</Breadcrumb.Item>
      </Breadcrumb>
    </div>
  ); 
};

const AppView = () => {
  return (
    <div>
      <Col md={4}>
        <h3>HTTP Request Header</h3>
        <p>Check HTTP Request your browser is sending.</p>
        <Link to="/httpheader">linklink</Link>
        <Button bsStyle="primary">Go</Button>
      </Col>
      <Col md={4}>
        <h3>Base64 encoder/decoder</h3>
        <p>Check HTTP Request your browser is sending.</p>
        <Link to="/baseconv">linklink</Link>
        <Button bsStyle="primary">Go</Button>
      </Col>
      <Col md={4}>
        <h3>XmlBeautify</h3>
        <p>Check HTTP Request your browser is sending.</p>
        <Link to="/xmlbeautify">linklink</Link>
        <Button bsStyle="primary">Go</Button>
      </Col>
      <Col md={4}>
        <h3>URL Encoder/Decoder</h3>
        <p>Check HTTP Request your browser is sending.</p>
        <Link to="/urlenc">linklink</Link>
        <Button bsStyle="primary">Go</Button>
      </Col>
      <Col md={4}>
        <h3>ID Generator</h3>
        <p>Check HTTP Request your browser is sending.</p>
        <Link to="/idgen">linklink</Link>
        <Button bsStyle="primary">Go</Button>
      </Col>
    </div>
  ); 
}

const App: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <Header/>
      <AppView/>
    </div>
  );
}

const HhdrAppView: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <h3>Hogehoge</h3>
      <HttpHeaderView data={{}}/>
    </div>
  ); 
}

const HhdrApp: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <Header/>
      <HhdrAppView/>
    </div>
  );
}


const BaseConvApp: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <Header/>
      <BaseConvView/>
    </div>
  );
}


const XmlBeautifyApp: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <Header/>
      <XmlBeautifyView/>
    </div>
  );
}

const UrlEncApp: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <Header/>
      <UrlEncView/>
    </div>
  );
}

const IdGenApp: React.StatelessComponent<React.Props<{}>> = () => {
  return (
    <div>
      <Header/>
      <IdGenView/>
    </div>
  );
}


ReactDOM.render((
  <BrowserRouter>
    <Switch>
      <Route exact path="/" component={App} />
      <Route exact path="/httpheader" component={HhdrApp} />
      <Route exact path="/baseconv" component={BaseConvApp} />
      <Route exact path="/xmlbeautify" component={XmlBeautifyApp} />
      <Route exact path="/urlenc" component={UrlEncApp} />
      <Route exact path="/idgen" component={IdGenApp} />
    </Switch>
  </BrowserRouter>
), document.querySelector('#app-root'));

