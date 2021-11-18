import React from 'react';

/*change action*/
function callBackend() {
    let xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'http://localhost:5000/start')
    xhttp.send()
}

class Gripper extends React.Component {
    render() {
        return(
            <div class="gp row">
                <div class="col-5">
                    <button type="button" class="grp btn btn-light" onClick={callBackend}>Open Gripper</button>
                    <button type="button" class="grp btn btn-light" onClick={callBackend}>Close Gripper</button>
                </div>

                <div class="input-width-row row">
                    <h1>Input Width</h1>
                    <div class="input-row row">
                        <input class="input-width" type="text" name="name" />
                        <button type="button" class="btn btn-light" onClick={callBackend}>Enter</button>
                    </div>
                </div>
            </div>
        );
    }
}

export default Gripper;