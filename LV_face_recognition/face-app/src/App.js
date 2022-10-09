import React, { useState } from 'react'
import './App.css';
import FaceDetail from './components/FaceDetail/FaceDetail';
import Modal from './components/FaceModel/Modal';
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
            Xác thực khuôn mặt bằng ReactJS
          </h1>
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <button className='btn' style={{ marginRight: '10px' }} onClick={onHandleShowModel}>Đăng kí bằng khuôn mặt</button>
          <button className='btn'>Đăng nhập bằng khuôn mặt</button>
        </div>
      </div>
      <Modal show={show} setShow={setShow}>
        <Register setShow={setShow}></Register>
      </Modal>

    </div>
  );
}

export default App;
