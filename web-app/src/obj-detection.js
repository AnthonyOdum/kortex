import React from 'react';

/*change action*/
function callBackend() {
    let xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'http://localhost:5000/start')
    xhttp.send()
}

class ObjDetection extends React.Component {
    render() {
        return(
            <div class="row">
                <div class="obj-detect-col col">
                    <h1 id="obj-detect-header">Object Detection</h1>
                    <button type="button" class="start-btn btn btn-light" onClick={callBackend}>Start</button>
                </div>

                <div class="drop-row row">
                    <h1 id="drop-off-header">Drop Off</h1>
                    <h1 id="drop-off-header">Location</h1>
                    <div class="c-row row">
                        <div class="coord-col col-sm-4">
                            <h3>X:</h3>
                            <input class="coor-input" id="x-input" type="text" name="name" />
                            <button type="button" class="input-enter-btn btn btn-light" onClick={callBackend}>Enter</button>
                        </div>
                        <div class="coord-col col-sm-4">
                            <h3>Y:</h3>
                            <input class="coor-input" id="y-input" type="text" name="name" />
                            <button type="button" class="input-enter-btn btn btn-light" onClick={callBackend}>Enter</button>
                        </div>
                    </div>
                    <div class="col-md-5" id="z-coord-area">
                        <h3>Z:</h3>
                        <input class="coor-input" id="z-input" type="text" name="name" />
                        <button type="button" class="input-enter-btn btn btn-light" onClick={callBackend}>Enter</button>
                    </div>
                </div>
            </div>
        );
    }
}

export default ObjDetection;