import React, { useEffect, useState } from 'react'
import './App.css';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';

function App() {

  useEffect(() => {
    const hello = async () => {
      try {
        const res = await axios.get("http://192.168.1.8:5000/api/face/hello", {
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            "Access-Control-Allow-Origin": "*"
          }
        });
        console.log("Hello reponse", res)
        toast.success(res.data.msg)
      } catch (error) {
        console.log("Hello error 1:::", error)
      }

    }
    hello()
  }, [])

  return (
    <div className="App">
      {/* <div style={{ marginBottom: "20px" }}>
        <Link to="/register" style={{ marginRight: "10px" }}>Register</Link>
        <Link to="/login">Login</Link>
      </div> */}

      <Routes>
        {/* Register Page */}
        <Route path="/register" element={<RegisterPage />}>
        </Route>

        {/* Login Page */}
        <Route path="/login" element={<LoginPage />}>
        </Route>

      </Routes>
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
    </div>
  );
}

export default App;
