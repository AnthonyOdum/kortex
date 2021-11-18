import logo from './logo.svg';
import cpLogo from './Cyberpunk-logo.png';
import './App.css';
import './gripper-panel.css';
import './coordinates.css';
import './obj-detection.css';
import './home.css';
import 'bootstrap/dist/css/bootstrap.css';
import Button from './button.js';
import Gripper from './gripper-panel.js';
import Coordinates from './coordinates.js';
import Home from './home.js';
import ObjDetection from './obj-detection.js';
import React from 'react';
import { ItemList, UserInput } from './user_panel'

class App extends React.Component {
  render() {
    return (
    <div class='App'>
      <div id='objectDetection'>
        <ObjDetection />
      </div>
      {/*<div id='gripper'>
        <Gripper />
    </div>*/}
      <div id='home'>
        <Home />
      </div>
      {/*
      <div id='rightBackground'>
        <h1>Press me:</h1>
        <Button />
      </div>
      */}
    </div>
    );
  }
}

export default App;
