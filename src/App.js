import './App.css';
import Navbar from './navbar'
import Home from './home'
import Predictions from './predictions'
import Rankings from './rankings'
import News from './news'
import {useFetch} from './useFetch'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {

  return (
    <div className="App">
      <Router>
        <Navbar />
        <Switch>
          <Route path="/predictions">
            <Predictions />
          </Route>
          <Route path="/rankings">
            <Rankings />
          </Route>
          <Route path="/news">
            <News />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
