import * as React from 'react';
import { Button } from 'react-bootstrap';
import { compose, withState, withHandlers } from 'recompose';


const enhance = compose(
  withState<any, any, any, any>('value', 'updateValue', ''),
  withHandlers<any, any>({
    doDownload: (props: any) => (event: any) => {

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

const IdGenViewBase: React.StatelessComponent<{ value: any, updateValue: any, doDownload: any }>
  = ({ value, updateValue, doDownload }) => {
    return (
      <div>
        <div>
          <legend>Format</legend> 
          <input type={'radio'} value={'Base36'}/>
          <input type={'radio'} value={'Base62'}/>
          <legend>Length</legend> 
          <select>
            <option>7</option>
          </select>
          <legend>Count</legend> 
          <input/>
          <legend>Preview</legend> 
          <textarea readOnly={true}/>
          <button onClick={doDownload}>Download</button>
        </div>
      </div>
    );
  };

export const IdGenView = enhance(IdGenViewBase);
