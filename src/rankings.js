import Footer from './footer'
import {useFetch} from './useFetch'
function Rankings() {
    const {loading, data} = useFetch('https://ryanmccullough-assistantcoach.herokuapp.com/players/')

    const qbs = data.filter(player => player.position === "QB").slice(0, 5)
    const rbs = data.filter(player => player.position === "RB").slice(0, 5)
    const wrs = data.filter(player => player.position === "WR").slice(0, 5)
    const tes = data.filter(player => player.position === "TE").slice(0, 5)

    return (
        <>
        <div className="rankings-container">
            <div className="ranking">
                <span className="ranking-title">Top QBs</span>
                    {qbs.map((player)=>{
                        return (
                            <div className="player-container">
                                <div className="img-container">
                                    <img className="ranking-image" src={player.image_path} alt={player.name}/>
                                </div>
                                <span className="player-name">{player.name} ({player.team})</span>
                            </div>
                        );
                    })}
            </div>
            <div className="ranking">
                <span className="ranking-title">Top RBs</span>
                {rbs.map((player)=>{
                    return (
                        <div className="player-container">
                            <div className="img-container">
                                <img className="ranking-image" src={player.image_path} alt={player.name}/>
                            </div>
                            <span className="player-name">{player.name} ({player.team})</span>
                        </div>
                    );
                })}
            </div>
            <div className="ranking">
                <span className="ranking-title">Top WRs</span>
                {wrs.map((player)=>{
                    return (
                        <div className="player-container">
                            <div className="img-container">
                                <img className="ranking-image" src={player.image_path} alt={player.name}/>
                            </div>
                            <span className="player-name">{player.name} ({player.team})</span>
                        </div>
                    );
                })}
            </div>
        </div>
        <Footer />
        </>
    );
}

export default Rankings;