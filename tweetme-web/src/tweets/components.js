import { useEffect, useState } from 'react';
import { loadTweets } from '../lookup/components';

export const TweetsList = (props) => {
   const [tweets, setTweets] = useState([])
   useEffect(() => {
      const myCallback = (response, status) => {
         if (status === 200) {
            setTweets(response)
         }
      }
      loadTweets(myCallback)
   }, [])
   return tweets.map((tweet, index) => {
      return <Tweet tweet={tweet} key={tweet.id} />
   })
}

export const ActionBtn = ({ tweet, action }) => {
   const actionDisplay = action.display ? action.display : 'Action'
   const display = action.type === "like" ? `${tweet.likes} ${actionDisplay}` : actionDisplay
   const handleClick = (event) => {
      event.preventDefault()
      if (action.type === "like") {
         console.log(tweet.likes + 1)
      }
   }
   return <button className='btn btn-primary btn-sm' onClick={handleClick}>{display}</button>
}

export const Tweet = ({ tweet }) => {
   // const tweetClassName = {className} ? {className} : "my-5 py-5 border bg-white"
   // "col-10 mx-auto col-md-6"
   return (
      <div className="my-5 py-5 border bg-white text-dark">
         <p>{tweet.id} - {tweet.content}</p>
         <div className='btn btn-group'>
            <ActionBtn tweet={tweet} action={{ type: "like", display: "Likes" }} />
            <ActionBtn tweet={tweet} action={{ type: "unlike", display: "Unlike" }} />
            <ActionBtn tweet={tweet} action={{ type: "retweet"}} />
         </div>
      </div>)
}