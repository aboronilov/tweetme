import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import { Tweets } from './tweets';
import { loadTweets } from './lookup/components';
import { TweetsList } from './tweets/components';

function App() {

   return (
      <div className="App">
         <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p>
               Edit <code>src/App.js</code> and save to reload.
            </p>
            <div>
               <TweetsList />
            </div>
            <a
               className="App-link"
               href="https://reactjs.org"
               target="_blank"
               rel="noopener noreferrer"
            >
               Learn React
            </a>
         </header>
      </div>
   );
}

export default App;
