import * as React from 'react';
import { Button } from 'react-bootstrap';
import { withStateHandlers } from 'recompose';


const enhance = withStateHandlers<{ data: string }, { onRawChange: any, onEncChange: any }>(
  () => ({
    data: '',
  }),
  {
    onRawChange: ({ data }: { data: any }) => (newvalue: string) => ({
      data: newvalue,
    }),
    onEncChange: ({ data }: { data: any }) => (newvalue: string) => ({
      data: decodeURI(newvalue),
    }),
  }
);

const UrlEncViewBase: React.StatelessComponent<{ data: any, onRawChange: any, onEncChange: any }>
  = ({ data, onRawChange, onEncChange }) => {
    return (
      <div>
        <div>
          <legend>Raw text</legend>
          <textarea onChange={(e) => { onRawChange(e.target.value); }} value={data}/>
        </div>
        <div>
          <legend>URL encoded text</legend>
          <textarea onChange={(e) => { onEncChange(e.target.value); }} value={encodeURI(data)}/>
        </div>
      </div>
    );
  };

export const UrlEncView = enhance(UrlEncViewBase);
