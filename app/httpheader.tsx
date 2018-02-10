import * as React from 'react';
import { Button } from 'react-bootstrap';
import { lifecycle, withState } from 'recompose';


const enhance = lifecycle({
  componentDidMount() {
    fetch('/api/httpheader')
      .then((response) => response.json())
      .then((responseJson) => {
        console.log(responseJson);
        this.setState({ data: responseJson });
      })
      .catch((error) => {
        console.error(error);
      });
  }
});

const HttpHeaderViewBase: React.StatelessComponent<{ data: any; }> = ({ data }) => {
  return (
    <div>
      <div>
        Address: {data.remote_addr}
      </div>
      <div>
        Host: {data.remote_host}
      </div>
      <div>
        Headers: {JSON.stringify(data.headers)}
      </div>
    </div>
  );
};

export const HttpHeaderView = enhance(HttpHeaderViewBase);
