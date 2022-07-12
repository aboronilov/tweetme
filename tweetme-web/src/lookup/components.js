export const loadTweets = (callback) => {
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
      callback({ "message": "The request has an error" }, 400)
   }
   xhr.send()
}