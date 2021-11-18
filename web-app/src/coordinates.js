import React from 'react';

/*change action*/
function callBackend() {
    let xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'http://localhost:5000/start')
    xhttp.send()
}

class Coordinates extends React.Component {
    render() {
        return(
            <div class="row">
                <div class="item-col col-8">
                    <h1 class="input-header">Choose Item:</h1>
                    <h3>Item 1: Bear</h3>
                    <h3>Item 2: Bottle</h3>
                    <h3>Item 3: Soda Can</h3>
                </div>
                <div class="input-coord-row row">
                    <h1 class="input-header">Input<br></br> Coordinates:</h1>
                    <div class="coord-row row" id="coord-row1">
                        <h2>X:</h2>
                        <input class="coord-input" type="text" name="name" />
                    </div>
                    <div class="coord-row row">
                        <h2>Y:</h2>
                        <input class="coord-input" type="text" name="name" />
                    </div>
                    <div class="coord-row row">
                        <h2>Z:</h2>
                        <input class="coord-input" type="text" name="name" />
                    </div>
                </div>
            </div>
        );
    }
}

export default Coordinates;