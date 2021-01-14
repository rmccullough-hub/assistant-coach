import Footer from './footer'
import { useFetch } from './useFetch';
import { useState } from 'react'
function News() {
    const {loading, data} = useFetch('https://ryanmccullough-assistantcoach.herokuapp.com/articles/')
    var articles = data //.splice(0, 9)
    const [search, setSearch] = useState('')
    const [returnVal, setReturnVal] = useState([])
    const espn = 'https://a1.espncdn.com/combiner/i?img=%2Fi%2Fespn%2Fespn_logos%2Fespn_red.png'
    const yahoo = 'https://s.yimg.com/cv/apiv2/social/images/yahoo_default_logo-1200x1200.png'
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
        if (search) {
          var p = {'query':search}
          var csrftoken = getCookie('csrftoken')
            
          fetch('https://ryanmccullough-assistantcoach.herokuapp.com/filter/', {
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
              console.log(returnVal)
            });
              setSearch('')
            } else {
              console.log('empty values');
            }
          };
    return (
    <>
        <div className="position-stories"></div>
        <form className="news-search" onSubmit={handleSubmit}>
            {/* <h3>Stories for {!loading ? articles[0].date.substring(0, 7): 'Loading'}</h3> */}
            <button type="submit" className="news-search-btn">Search</button>
            <input 
            className="news-input" 
            placeholder="Search" 
            type="text" 
            value={search} 
            id='search'
            name='search'
            onChange={(e) => setSearch(e.target.value)} 
            />
        </form>
        <div className="row news-page-container">
            {returnVal.length === 0 ? articles.map((article)=>{
                return (
                <div className="article">
                    <a href={article.url} target="_blank">
                        <img style={{'maxWidth':'215px', 'maxHeight':'150px', 'marginTop':'10px', 'borderRadius':'1rem', 'marginLeft':'5px', 'marginRight':'5px'}} src={article.image_path} alt={article.title}/>
                    </a>
                    <a href={article.url} target="_blank">
                        <p style={{'fontSize':'12px', 'maxWidth':'225px', 'marginTop':'5px', 'color':'white'}}>{article.title}</p>
                    </a>
                </div>
                )
            }): returnVal.map((article)=> {
                if (article.source === 'espn') {
                    var image = espn
                } else if (article.source === 'yahoo') {
                    var image = yahoo
                } else {var image = article.image_path}
                return (
                    <div className="article">
                        <a href={article.url} target="_blank">
                            <img style={{'maxWidth':'215px', 'maxHeight':'150px', 'marginTop':'10px', 'borderRadius':'1rem', 'marginLeft':'5px', 'marginRight':'5px'}} src={image} alt={article.title}/>
                        </a>
                        <a href={article.url} target="_blank">
                            <p style={{'fontSize':'12px', 'maxWidth':'225px', 'marginTop':'5px'}}>{article.title}</p>
                        </a>
                    </div>
                    )
            })}
        </div>
        <Footer />
    </>
    );
}

export default News;