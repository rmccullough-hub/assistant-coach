import logo from './Assets/logo.svg'
import {Link} from 'react-router-dom'
function Navbar() {
    return (
        <nav className="nav-container">
            <Link to="/"><h3 className="logo-text">AI-Coach</h3></Link>
            <Link to="/"><img src={logo} alt="Logo" className="logo"/></Link>
            <ul>
                <Link to="/"><li style={{'color':'#00D801'}}>Home</li></Link>
                <Link to="/predictions"><li>Predictions</li></Link>
                <Link to="/rankings"><li>Rankings</li></Link>
                <Link to="/news"><li>News</li></Link>
            </ul>
        </nav>
    );
}

export default Navbar;