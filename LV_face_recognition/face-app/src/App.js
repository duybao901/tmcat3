import React, { useState } from 'react'
import './App.css';
import Modal from './components/FaceModel/Modal';
import Register from './components/Register/Register';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Login from './components/Login/Login';

function App() {

  const [showRegister, setShowRegister] = useState(false)
  const [showLogin, setShowLogin] = useState(false)

  const notify = () => toast("Wow so easy!");
  return (
    <div className="App">
      <div style={{ padding: "50px" }}>
        <div>
          <h1 style={{ marginBottom: "40px" }}>
            Xác thực khuôn mặt bằng ReactJS
          </h1>
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <button className='btn' style={{ marginRight: '10px' }} onClick={() => setShowRegister(true)}>Đăng kí bằng khuôn mặt</button>
          <button className='btn' onClick={() => setShowLogin(true)}>Đăng nhập bằng khuôn mặt</button>
        </div>
      </div>
      <Modal show={showRegister} setShow={setShowRegister}>
        <Register setShow={setShowRegister}></Register>
      </Modal>

      <Modal show={showLogin} setShow={setShowLogin}>
        <Login setShow={setShowLogin}></Login>
      </Modal>

      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
      />
      <button onClick={notify}>Notify!</button>
    </div>
  );
}

export default App;
