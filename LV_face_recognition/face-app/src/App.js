import React, { useState } from 'react'
import './App.css';
import Model from './components/FaceModel/Model';
import Register from './components/Register/Register';

function App() {

  const [show, setShow] = useState(false)

  const onHandleShowModel = () => {
    setShow(true)
  }

  return (
    <div className="App">
      <div style={{ padding: "50px" }}>
        <div>
          <h1 style={{ marginBottom: "40px" }}>
            Face Authentication using ReactJS
          </h1>
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <button className='btn' style={{ marginRight: '10px' }} onClick={onHandleShowModel}>Face Register</button>
          <button className='btn'>Face Sign In</button>
        </div>
        <Model show={show}>
          <Register></Register>
        </Model>
      </div>
    </div>
  );
}

export default App;
