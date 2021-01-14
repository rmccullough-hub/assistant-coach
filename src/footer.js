import linkedin from './Assets/linkedin.svg'
import github from './Assets/github.svg'
import gmail from './Assets/gmail.svg'
import React, { useRef, useState } from 'react';

function Footer() {

    const [copySuccess, setCopySuccess] = useState('');
    const [show, setShow] = useState(false)

    const textAreaRef = useRef(null);

    const sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
      }

    const copyToClipboard = async (e) => {
        textAreaRef.current.select();
        document.execCommand('copy');
        e.target.focus();
        setCopySuccess('Copied!');
        setShow(true)
        await sleep(3000)
        setShow(false)
    };

    return (
        <>
        {show && <div className="email-copy">
            <strong>Our email has been copied to your clipboard!</strong>
        </div>}
        <footer>
            <h4 className="footer-title">A quick note on this website and its creator</h4>
            <hr id="divider2"/>
            <div className="contact-container">
                <a href="https://www.linkedin.com/in/ryan-c-mccullough/" target="_blank" rel="noopener noreferrer"><img className="contact-logo" src={linkedin} alt="linkedin" /></a>
                <a href="https://github.com/rmccullough-hub" target="_blank" rel="noopener noreferrer"><img className="contact-logo" src={github} alt="github" /></a>
                <button style={{'borderStyle':'none','backgroundColor':'white'}} onClick={copyToClipboard}><img value="ryanmcculloughuc@gmail.com" className="contact-logo" src={gmail} alt="gmail" /></button>
            </div>
            <p className="footer-text">
                My name is Ryan McCullough, and I am an Economics major at San Diego State University. 
                I have used what Economics has taught me about math and statistics to create an accurate prediction algorithm for fantasy football. 
                I plan on expanding this website to include predictions on other sports and sport related bets. 
                If you would like to check out the code for this site and its predictions, you can click on the link to my GitHub to the left.  
            </p>
            <form >
                <textarea 
                style={{'width':'0px', 'height':'0px', 'position':'absolute','bottom':'-100%', 'opacity':'0'}}
                ref={textAreaRef}
                value='ryanmcculloughuc@gmail.com'
                />
            </form>
        </footer>
        </>
    );
}

export default Footer;