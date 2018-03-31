import * as React from 'react';
import { storiesOf } from '@storybook/react';
import { BaseConvView } from '../components/baseconv';
import { HttpHeaderView } from '../components/httpheader';
import { IdGenView } from '../components/idgen';
import { XmlBeautifyView } from '../components/xmlbeautify';
import { UrlEncView } from '../components/urlenc';
import { UniEscView } from '../components/uniesc';


storiesOf('BaseConv', module)
  .add('with text', () => (
    <BaseConvView />
  ));

storiesOf('HttpHeader', module)
  .add('with text', () => (
    <HttpHeaderView data={{}} />
  ));

storiesOf('UrlEnc', module)
  .add('with text', () => (
    <UrlEncView />
  ));

storiesOf('UniEsc', module)
  .add('with text', () => (
    <UniEscView />
  ));

storiesOf('IdGen', module)
  .add('with text', () => (
    <IdGenView />
  ));

storiesOf('XmlBeautify', module)
  .add('with text', () => (
    <XmlBeautifyView />
  ));
