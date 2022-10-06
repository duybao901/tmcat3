import React, { useState, useRef, useEffect } from 'react'
import "./Register.css"

const Register = ({ setShow }) => {

    const inputRef = useRef();

    const [userName, setUserName] = useState("username")
    const [imageList, setImageList] = useState([])
    const [typeAdd, setTypeAdd] = useState("")

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
            <div className='modal__content'>
                <div className="modal__header">
                    <div className="register__user-name">
                        <input id='username' ref={inputRef} className="modal__username" type="text" onChange={onHandleChange} value={userName} />
                        <label htmlFor='username'><i className='bx bx-pencil'></i></label>
                    </div>
                    <div className='modal__close' onClick={() => setShow(false)}>
                        <i className='bx bx-x'></i>
                    </div>
                </div>
                <div className="modal__body">
                    {
                        typeAdd === "" ? <div className="register__add-image">
                            <span>Thêm ảnh: </span>
                            <div style={{ display: "flex", margin: "20px 0px" }}>
                                <button style={{ marginRight: "10px" }} className='btn add-image__btn' onClick={() => setTypeAdd("webcam")}>
                                    <div>
                                        <i className='bx bx-camera'></i>
                                        <span>
                                            Webcam
                                        </span>
                                    </div>
                                </button>
                                <button className='btn add-image__btn' onClick={() => setTypeAdd("upload")}>
                                    <div>
                                        <i className='bx bx-upload'></i>
                                        <span>
                                            Upload
                                        </span>
                                    </div>
                                </button>
                            </div>
                        </div> : <div className="register__add-zone">
                            <div className="add-zone__webcam">
                                <div>
                                    <div>
                                        <span>
                                            Webcam
                                        </span>
                                        <i className='bx bx-x' onClick={() => setTypeAdd("")}></i>
                                    </div>
                                    {/* Camera */}
                                    <div className="add-zone__camera">

                                    </div>
                                    
                                </div>
                            </div>
                            <div>
                                <span>
                                    Ảnh:
                                </span>
                                <div>

                                </div>
                            </div>
                        </div>
                    }

                </div>
                <div className="modal__bottom" style={{ display: "flex", justifyContent: "flex-end" }}>
                    <button style={{ marginRight: "10px" }} className="btn btn--danger" onClick={() => setShow(false)}>Huỷ</button>
                    <button className="btn btn--success" onClick={() => setShow(false)}>Đăng kí</button>
                </div>
            </div>
        </div>
    )
}

export default Register