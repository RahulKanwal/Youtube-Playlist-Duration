import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
import ReactDOM from 'react-dom';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'

function App() {
  const [playlist, setPlaylist] = useState( "" );
  // const result = useState( '' );
  // const result = useRef(null);
  const handleSubmit = e => {
    e.preventDefault();
    axios.post('https://youtube-playlist-duration.onrender.com/api/duration', {"link": playlist})
    .then(response => {
      console.log(response)
      // alert(response.data)
      // result(response)
      ReactDOM.render(<h2>Playlist Duration: {response.data}</h2>,
      document.getElementById('duration'));
    })
    .catch(error => {
      console.log(error)
      ReactDOM.render(<p>Sorry. There is error. Please check the playlist link. If the link is correct then there must be an issue in the API and we are sorry about that.</p>,
      document.getElementById('duration'));
    })
    // fetch('https://yt-playlist-duration-flask.herokuapp.com/', {
    //   method: 'post',
    //   body: JSON.stringify({
    //     link: playlist,
    //   })
    // })
    // .then(response => ReactDOM.render(<h2>Playlist Duration: {response.data}</h2>,
    // document.getElementById('duration')),)
    // .catch(err => ReactDOM.render(<p>Sorry. There is error. Please check the playlist link. If the link is correct then there must be an issue in the API and we are sorry about that.</p>,
    // document.getElementById('duration')),)
    // setPlaylist("");
  }

  return (
    <div className="App">
      <h1>YouTube Playlist Duration</h1>
      <form onSubmit={handleSubmit}>
      <div class="form-group row">
        <div class="col-md-12">
        <label for="playlist link">Enter Playlist Link</label>
          <input type="text" class="form-control" value={playlist} onChange={e => setPlaylist(e.target.value)} placeholder="https://www.youtube.com/playlist?list=playlist_id" />
          <input type="submit" className="btn btn-primary" name="Calculate" />
        </div>
      </div>
      </form>
      <div id="duration">

      </div>
    </div>
  );
}

export default App;
