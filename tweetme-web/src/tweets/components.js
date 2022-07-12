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
   switch (action.type) {
      case "like":
         return <button className='btn btn-primary btn-sm'>{tweet.likes} likes</button>
      case "unlike":
         
   }
   return action.type === 'like' ? <button className='btn btn-primary btn-sm'>{tweet.likes} likes</button> : null
}

export const Tweet = ({ tweet }) => {
   // const tweetClassName = {className} ? {className} : "my-5 py-5 border bg-white"
   // "col-10 mx-auto col-md-6"
   return (
      <div className="my-5 py-5 border bg-white text-dark">
         <p>{tweet.id} - {tweet.content}</p>
         <div className='btn btn-group'>
            <ActionBtn tweet={tweet} action={{ type: "like" }} />
         </div>
      </div>)
}