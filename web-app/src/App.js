import logo from './logo.svg';
import cpLogo from './Cyberpunk-logo.png';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import Button from './button.js';
import React from 'react';
import { ItemList, UserInput } from './user_panel'

class App extends React.Component {
  render() {
    return (
    <div class='App'>
      <div id='coordinates'>
        <ItemList />
        <UserInput />
      </div>
      <div id='gripper'>
        <ItemList />
        <UserInput/>
      </div>
      <div id='home'>
        <ItemList />
        <UserInput/>
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
