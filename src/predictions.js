import playerOutline from './Assets/player.svg'
import Footer from './footer'
import axios from 'axios'
import {useState} from 'react'
import PlayerPrediction from './playerPrediction'

function Predictions() {
    const [player, setPlayer] = useState('')
    const [returnVal, setReturnVal] = useState({})

    const getCookie = (name) => {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
    
      const handleSubmit = (e) => {
        e.preventDefault();
        if (player) {
          var p = {'playerName':player}
          var csrftoken = getCookie('csrftoken')
          axios.defaults.headers.post['Content-type'] = 'application/json'
          axios.defaults.headers.post['X-CSRFToken'] = csrftoken
            
          fetch('https://ryanmccullough-assistantcoach.herokuapp.com/predictions/', {
              method:'POST',
              headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken,
              },
              body:JSON.stringify(p)
            }).then(function(response) {
              return response.json();
            }).then(function(response) {
              setReturnVal(response);
              console.log(returnVal.image_path)
            });
              setPlayer('')
            } else {
              console.log('empty values');
            }
          };
    const objCheck = (obj) =>{
      return Object.keys(obj).length === 0  && obj.constructor === Object;
    }

    // <h2 className="search-title">{returnVal.name} ({returnVal.position})</h2>
    return (
        <>
            <div className="predictions-card">
                <div style={{'height':'100%', 'width':'100%', 'position':'relative'}}>
                    { objCheck(returnVal) ? <img className="player-img" src={playerOutline} alt="Player"/> : <img className="player-img" src={returnVal.image_path} alt={returnVal.name}/>}
                    <form onSubmit={handleSubmit}>
                        <button type="submit" className="search-btn">Search</button>
                        <input 
                        type="text" 
                        value={player} 
                        id='player'
                        name='player'
                        onChange={(e) => setPlayer(e.target.value)} 
                        placeholder="player"
                        />
                    </form>
                    <div className="player-stats">
                        {objCheck(returnVal) ? <h2 className="search-title">Search a player</h2>: <PlayerPrediction {...returnVal}/>}                        
                    </div>
                </div>
            </div>
            <Footer />
        </>
    );
}

export default Predictions;