import * as React from 'react';
import { Button } from 'react-bootstrap';
import { compose, withState, withHandlers } from 'recompose';


const enhance = compose(
  withState<any, any, any, any>('value', 'updateValue', ''),
  withHandlers<any, any>({
    doConvert: (props: any) => (event: any) => {

      const form = new FormData();
      form.append('original', props.value)

      const params = {
        headers: {
          'Accept': 'application/json, application/xml, text/plain, text/html, *.*',
        },
        method: 'POST',
        body: form
      };
      fetch('/xmlbeautify', params)
        .then((response) => response.text())
        .then((responseText) => {
          console.log(responseText)
          props.updateValue(responseText);
        })
        .catch((error) => {
          console.error(error);
        });
      },
  }),
);

const XmlBeautifyViewBase: React.StatelessComponent<{ value: any, updateValue: any, doConvert: any }>
  = ({ value, updateValue, doConvert }) => {
    return (
      <div>
        <div>
          <textarea onChange={(e) => {updateValue(e.target.value)}} value={value}/>
          <button onClick={doConvert}>Convert</button>
        </div>
      </div>
    );
  };

export const XmlBeautifyView = enhance(XmlBeautifyViewBase);
