import React, { useState, useRef, useEffect } from 'react'
import "./Register.css"

const Register = ({ setShow }) => {

    const inputRef = useRef();

    const [userName, setUserName] = useState("username")

    const onHandleChange = (e) => {
        setUserName(e.target.value)
    }

    useEffect(() => {
        if (inputRef) {
            inputRef.current.style.width = ((inputRef.current.value.length + 1) * 10) + "px";
        }
    }, [userName])

    return (
        <div>
            <div className='face-modal__content'>
                <div className="modal__header">
                    <div className="register__user-name">
                        <input id='username' ref={inputRef} className="face-modal__username" type="text" onChange={onHandleChange} value={userName} />
                        <label htmlFor='username'><i className='bx bx-pencil'></i></label>
                    </div>
                    <div className='face-modal'>
                        <i className='bx bx-x' onClick={() => setShow(false)}></i>
                    </div>
                </div>
                <div className="modal__body">
                    <div className="register__add-image">
                        <span>Thêm ảnh khuôn mặt: </span>
                        <div style={{ display: "flex", margin: "20px 0px" }}>
                            <button style={{ marginRight: "10px" }} className='btn add-image__btn'>
                                <div>
                                    <i className='bx bx-camera'></i>
                                    <span>
                                        Webcam
                                    </span>
                                </div>
                            </button>
                            <button className='btn add-image__btn'><div>
                                <i className='bx bx-upload'></i>
                                <span>
                                    Upload
                                </span>
                            </div></button>
                        </div>
                    </div>
                </div>
                <div className="modal__bottom">
                    <button onClick={() => setShow(false)}>close</button>
                </div>
            </div>
        </div>
    )
}

export default Register