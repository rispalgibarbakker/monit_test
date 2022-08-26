import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ApolloClient, InMemoryCache, ApolloProvider, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:8200/graphql',
  
  cache: new InMemoryCache(),
});
const root = ReactDOM.createRoot(document.getElementById('root'));
client
  .query({
    query: gql`
    query GetTransactionSeries($presetRange: String= "LAST_7_DAYS") {
      transactionSeries(presetRange: $presetRange) {
        key
        amount
      }
    } 
    `,
  })
  .then((result) => console.log(result));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
