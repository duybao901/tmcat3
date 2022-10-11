import React, { useState } from 'react'
import './App.css';
import Modal from './components/FaceModel/Modal';
import Register from './components/Register/Register';
import { ToastContainer , toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {

  const [show, setShow] = useState(false)

  const onHandleShowModel = () => {
    setShow(true)
  }
  
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
          <button className='btn' style={{ marginRight: '10px' }} onClick={onHandleShowModel}>Đăng kí bằng khuôn mặt</button>
          <button className='btn'>Đăng nhập bằng khuôn mặt</button>
        </div>
      </div>
      <Modal show={show} setShow={setShow}>
        <Register setShow={setShow}></Register>
      </Modal>
      <ToastContainer
        position="top-right"
        autoClose={5000}
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
