import React from 'react';

function callBackend() {
    let xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'http://localhost:5000/start')
    xhttp.send()
}

class Button extends React.Component {
    render() {
        return(
            <div class="row">
                <div class="col-5" id="start-button-col">
                    <button type="button" class="btn btn-light" onClick={callBackend}>Start</button>
                </div>
            </div>
        );
    }
}

export default Button;