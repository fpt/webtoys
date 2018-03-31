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
      data: Buffer.from(newvalue, 'base64').toString('ascii'),
    }),
  }
);

const BaseConvViewBase: React.StatelessComponent<{ data: any, onRawChange: any, onEncChange: any }>
  = ({ data, onRawChange, onEncChange }) => {
    return (
      <div>
        <div>
          <legend>Raw text</legend>
          <textarea onChange={(e) => { onRawChange(e.target.value); }} value={data}/>
        </div>
        <div>
          <legend>Base64 encoded text</legend>
          <textarea onChange={(e) => { onEncChange(e.target.value); }} value={Buffer.from(data).toString('base64')}/>
        </div>
      </div>
    );
  };

export const BaseConvView = enhance(BaseConvViewBase);
