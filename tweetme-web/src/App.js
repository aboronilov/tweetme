import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';

function loadTweets(callback) {
   const xhr = new XMLHttpRequest()
   const method = 'GET' // "POST"
   const url = "http://127.0.0.1:8000/api/tweets/"
   const responseType = "json"
   xhr.responseType = responseType
   xhr.open(method, url)
   xhr.onload = function () {
      callback(xhr.response, xhr.status)
   }
   xhr.onerror = function (err) {
      console.log(err)
      callback({"message": "The request has an error"}, 400)
   }
   xhr.send()
}

const Tweet = ({tweet}) => {
   // const tweetClassName = {className} ? {className} : "my-5 py-5 border bg-white"
   // "col-10 mx-auto col-md-6"
   return (
   <div className="my-5 py-5 border bg-white text-dark">
      <p>{ tweet.id } - { tweet.content }</p>
   </div>)
}

function App() {
   const [tweets, setTweets] = useState([])
   useEffect(() => {
      const myCallback = (response, status) => {
         console.log(response, status)
         if (status === 200) {
            setTweets(response)
         }
      }
      loadTweets(myCallback)
   }, [])
   return (
      <div className="App">
         <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p>
               Edit <code>src/App.js</code> and save to reload.
            </p>
            <div>
               {tweets.map((tweet, index) => {
                  return <Tweet tweet={tweet} key={tweet.id}/>
               })}
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
