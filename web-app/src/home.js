import React from 'react';
import homeLogo from '../src/home-icon.png';

/*change action*/
function callBackend() {
    let xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'http://localhost:5000/home')
    xhttp.send()
}

class Home extends React.Component {
    render() {
        return(
            <div class="row">
                <div class="home-col col">
                    <h1 class="home-header">Return</h1>
                    <h1 class="home-header">Home</h1>
                    <button type="button" class="btn" onClick={callBackend}><img src={homeLogo} alt="Home Button"/></button>
                </div>
            </div>
        );
    }
}

export default Home;