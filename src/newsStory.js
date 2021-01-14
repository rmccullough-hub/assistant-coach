function NewsStory(article) {
    var title = article.title
    return (
        <div className="home-news-story">
            <a href={article.url}><img class="home-images" src={article.image_path} alt="Story"/></a>
            <a href={article.url}><p style={{'fontSize':'12px', 'maxWidth':'175px', 'color':'white'}}>{article.title}</p></a>
        </div>
    );
}

export default NewsStory;