function PlayerPrediction(props) {
    console.log(props.current_projections)
    return (
        <>
            <h2 className="search-title">{props.name} ({props.position})</h2>
            <p>We predict that {props.position} {props.name} will score <b>{props.current_projection} points</b> this week.</p>
        </>
    );
}

export default PlayerPrediction;