import 'bootstrap/dist/css/bootstrap.min.css'
import $ from 'jquery'
import Popper from 'popper.js'
import 'bootstrap/dist/js/bootstrap.bundle.min'
import hero from './Assets/hero.svg'
import axios from 'axios'
import {useFetch} from './useFetch'
import NewsStory from './newsStory'
import {useState} from 'react'
import {Link} from 'react-router-dom'
function Home() {
    var {loading, data} = useFetch('https://ryanmccullough-assistantcoach.herokuapp.com/articles/')
    var firstArticles = data.slice(0, 5)
    var secondArticles = data.slice(5, 10)
    var [newsStories, setNewsStories] = useState([...firstArticles])
    const [index, setIndex] = useState({'first':0, 'second':1, 'third':2, 'fourth':3, 'fifth':4})

    return (
        <>
            <div className="home-card">
                <div className="home-card-content">
                    <div className="hero-items">
                        <h1 className="hero-title">Betting in the modern world</h1>
                        <p className="hero-paragraph">Improve your odds for success in fantasy football this week, and beyond, with predictions from our artificial intelligence. We use the power of Machine Learning to help you succeed.</p>
                        <Link to="/predictions"><button className="hero-btn">Start Here</button></Link>
                    </div>
                    <img src={hero} alt="hero section" className="hero-img"/>
                </div>
            </div>
            <div className="news-card">
                <div style={{'display':'flex', 'width':'100%', 'height':'100%', 'alignItems':'center', 'justifyContent':'center'}}>
                    {!loading ? <NewsStory {...data[index.first]} /> : <NewsStory {...newsStories[0]} /> }
                    {!loading ? <NewsStory {...data[index.second]} /> : 'Loading...'}
                    {!loading ? <NewsStory {...data[index.third]} /> : 'Loading...'}
                    {!loading ? <NewsStory {...data[index.fourth]} /> : 'Loading...'}
                </div>
            </div>
            <div className="circle-container">
                <div onClick={()=>{setIndex({'first':0, 'second':1, 'third':2, 'fourth':3, 'fifth':4})}}className="circle"></div>
                <div onClick={()=>{setIndex({'first':5, 'second':6, 'third':7, 'fourth':8, 'fifth':9})}} className="circle"></div>
            </div>
        </>
    );
}

export default Home;