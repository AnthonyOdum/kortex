import logo from './logo.svg';
import cpLogo from './Cyberpunk-logo.png';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import { Button } from 'react-bootstrap';
import React from 'react';
import { render } from 'react-dom';

class App extends React.Component {
  callBackend() {
    let xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'http://localhost:5000/start')
    xhttp.send()
  }

  sendLocation(x, y, z) {
    let xhttp = new XMLHttpRequest()
    xhttp.open('POST', 'http://localhost:5000/move')
    let data = {
      "x": x,
      "y": y,
      "z": z
    }
    xhttp.send(data)

  }

  render() {
    return (
      <div className="App" id="main-bg">
        <form action="http://localhost:5000/moveRobot" method="POST">
          <label for="x">X:</label>
          <input type="text" id="x" name="x" placeholder="0" required></input>
          <label for="y">Y:</label>
          <input type="text" id="y" name="y" placeholder="0" required></input>
          <label for="z">Z:</label>
          <input type="text" id="z" name="z" placeholder="0" required></input>
          <input type="submit" value="Submit"></input>
        </form>
      </div>
    );
  }
}

export default App;
