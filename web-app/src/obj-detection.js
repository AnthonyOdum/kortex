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
                </div>

                <div class="drop-row row">
                    <h1 id="drop-off-header">Drop Off</h1>
                    <h1 id="drop-off-header">Location</h1>
                    <form action="http://localhost:5000/panning                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       " method="POST">
                    <div class="c-row row">
                        <div class="coord-col col-sm-4">
                            <label for="x">X:</label>
                            <input type="text" id="x" name="x" placeholder="0" required></input>
                        </div>
                        <div class="coord-col col-sm-4">
                            <label for="y">Y:</label>
                            <input type="text" id="y" name="y" placeholder="0" required></input>
                        </div>
                    </div>
                    <div class="col-md-5" id="z-coord-area">
                        <label for="z">Z:</label>
                        <input type="text" id="z" name="z" placeholder="0" required></input>
                        <input type="submit" value="Submit"></input>
                    </div>
                    </form>
                </div>
            </div>
        );
    }
}

export default ObjDetection;