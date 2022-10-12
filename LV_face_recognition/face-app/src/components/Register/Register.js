import React, { useState, useRef, useEffect, useCallback } from 'react'
import "./Register.css"
import Webcam from 'react-webcam'
import FaceIcon from '../../images/face-icon.png'

import FaceDetail from '../FaceDetail/FaceDetail'
import axios from 'axios'
import { toast } from "react-toastify"

const Register = ({ setShow }) => {

    const videoConstraints = {
        height: 260,
        facingMode: "user",
        aspectRatio: 1
    };

    const inputRef = useRef();
    const webcamRef = useRef();

    const [userName, setUserName] = useState("username")
    const [imageList, setImageList] = useState([])
    const [imageListFile, setImageListFile] = useState([])
    const [recoding, setRecording] = useState(false)
    const [typeAdd, setTypeAdd] = useState("")
    const [autoCapture, setAutoCapture] = useState(null)
    const [second, setSecond] = useState(0)
    const [secondInterval, setSecondInterval] = useState(0)
    const [showFaceDetail, setShowFaceDetail] = useState({})
    const [loading, setLoading] = useState(false)

    const onHandleChange = (e) => {
        setUserName(e.target.value)
    }

    useEffect(() => {
        if (inputRef) {
            inputRef.current.style.width = ((inputRef.current.value.length + 1) * 10) + "px";
        }
    }, [userName])

    const capture = () => {

        const newListSample = imageList.concat(imageListFile)
        if (newListSample.length >= 15) {
            toast.warning("Số ảnh phải lớn hơn 10 và tối đa 15 ảnh")
            return;
        }

        setRecording(true)
        var i = 0;
        var interval = setInterval(() => {
            i += 100;
            if (i <= 1500) {
                const imageSrc = webcamRef.current.getScreenshot();
                setImageList(prevImageList => [...prevImageList, imageSrc])
            } else {
                setRecording(false)
                setSecond(0)
            }
        }, 100)

        setAutoCapture(interval)

        var intervalSecond = setInterval(() => {
            setSecond(s => s + 1)
        }, 1000)

        setAutoCapture(interval)
        setSecondInterval(intervalSecond)

    }

    useEffect(() => {
        if (second === 0 && recoding === false) {
            stopCapture()
        }
    }, [second])

    const stopCapture = () => {
        setRecording(false)
        clearInterval(autoCapture);
        clearInterval(secondInterval);
    }

    const onHandleChangeFile = (e) => {
        
        const target = e.target
        const files = target.files;

        const newListSample = imageList.concat(imageListFile)
        if (newListSample.length + files.length >= 15) {
            toast.warning("Số ảnh phải lớn hơn 10 và tối đa 15 ảnh")
            return;
        }

        if (files?.length !== 0 && files !== null) {
            setImageListFile(prevImageListFile => {
                return [...prevImageListFile, ...files]
            })
        }
    }

    const handleDragFile = (e) => {
        // const target = e.target
        // const files = target.files;
        // if (files?.length !== 0 && files !== null) {
        //     setImageListFile(prevImageListFile => {
        //         return [...prevImageListFile, ...files]
        //     })
        // }
    }

    function dataURLtoFile(dataurl, filename) {

        var arr = dataurl.split(','),
            mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]),
            n = bstr.length,
            u8arr = new Uint8Array(n);

        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }

        return new File([u8arr], filename, { type: mime });
    }

    const handleRegister = async (e) => {
        e.preventDefault();

        const isNullSample = imageList.every(element => element === null);

        if(isNullSample){
            toast.warning("Một số ảnh không hợp lệ")
            return;
        }

        const newImageListFile = imageList.map(item => {
            return dataURLtoFile(item, userName);
        })

        const newListSample = newImageListFile.concat(imageListFile)
        console.table(newListSample)

        const totalImage = newListSample.length;
        console.log(totalImage)

        if (totalImage < 10 || totalImage > 15) {
            toast.warning("Số ảnh phải lớn hơn 10 và tối đa 15 ảnh")
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < totalImage; i++) {
            formData.append("file", newListSample[i]);
        }

        // formData.files("files", newListSample)
        // formData.append("files", newListSample);
        formData.append("user_name", userName.trim().toLocaleLowerCase())

        // try {
        //     setLoading(true)
        //     const res = await axios.post("http://localhost:5000/api/face/train", formData, {
        //         headers: {
        //             'Content-Type': 'multipart/form-data'
        //         }
        //     })
        //     setLoading(false)
        //     toast.success(res.data.msg)
        // } catch (error) {
        //     setLoading(false)
        //     toast.warning(error.response.data.msg)
        // }

    }

    const deleteSample = (i) => {
        const newArray = imageList.filter((item) => {
            return item !== imageList[i]
        })

        setImageList(newArray)
    }

    const deleteAllSamples = () => {
        setImageList([])
        setImageListFile([])
    }

    const deleteSampleFile = (i) => {
        const newArray = imageListFile.filter((item) => {
            return item !== imageListFile[i]
        })

        setImageListFile(newArray)
    }

    const handleShowFaceDetail = (faceIndex, fileClick, cameraClick) => {
        setShowFaceDetail({
            [`showface-list-file${faceIndex}`]: fileClick,
            [`showface-list${faceIndex}`]: cameraClick,
        })
    }


    return (
        <div className="register__wrapper">
            {
                loading && <div className="register__fade"></div>
            }
            {
                loading && <div className="register__loading">
                    <div className="register__loading-circle">
                    </div>
                    <img src={FaceIcon} alt='face-icon-loading'></img>
                </div>
            }
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
                    </div> :
                        <div className="register__add-zone">
                            {
                                typeAdd === "webcam" ?
                                    <div className="add-zone__webcam">
                                        <div className="add-zone__head">
                                            <span>
                                                Webcam
                                            </span>
                                            <i className='bx bx-x' onClick={() => setTypeAdd("")}></i>
                                        </div>
                                        {/* Camera */}
                                        <div className="add-zone__camera">
                                            <Webcam
                                                audio={false}
                                                screenshotFormat="image/jpeg"
                                                width={"100%"}
                                                videoConstraints={videoConstraints}
                                                ref={webcamRef}
                                                screenshotQuality={1}
                                            >
                                            </Webcam>
                                        </div>
                                        <div className="add-zone__control">
                                            <button disabled={recoding ? true : false} className={`btn ${recoding && "btn--disable"}`} onClick={capture}>
                                                {
                                                    !recoding ? "Record 2 Second" : `Reconding in ${second}s...`
                                                }
                                            </button>
                                        </div>
                                    </div>
                                    :
                                    <div className="add-zone__upload-file">
                                        <div className="add-zone__head">
                                            <span>
                                                File
                                            </span>
                                            <i className='bx bx-x' onClick={() => setTypeAdd("")}></i>
                                        </div>
                                        <div style={{ padding: "10px" }}>
                                            <div className="add-zone__upload-from">
                                                <input onDragEnter={handleDragFile} multiple={true} onChange={onHandleChangeFile} type="file" id='file-upload' accept='image/*' name="file-upload"></input>
                                                <div className="add-zone__upload-from-text">
                                                    <i className='bx bx-image-add'></i>
                                                    <p>Chọn hình ảnh từ máy tính của bạn hoặc kéo và thả vào đây</p>
                                                </div>
                                            </div>
                                            <div className='add-zone__upload-from-text'>
                                                <img src={FaceIcon} alt="face-icon" style={{ width: "50px" }} />
                                                <p>
                                                    Hình ảnh sẽ được cắt thành hình vuông
                                                </p>
                                            </div>
                                        </div>

                                    </div>
                            }

                            <div className="add-zone__sample">
                                <div className="add-zone__sample-control">
                                    <span>
                                        {imageList.length + imageListFile.length} Ảnh:
                                    </span>
                                    <button className='btn' onClick={deleteAllSamples}>
                                        Xoá tất cả
                                    </button>
                                </div>
                                <div className="add-zone__captures">
                                    {
                                        imageList !== [] && imageList.map((image, index) => {
                                            return <div key={index} className="add-zone__captures-item">
                                                <img onClick={() => handleShowFaceDetail(index, false, true)} src={image} alt='sample-image'></img>
                                                <i className='bx bx-trash' onClick={() => deleteSample(index)}></i>
                                                <FaceDetail
                                                    isFileSample={false}
                                                    index={index}
                                                    username={userName}
                                                    deleteSample={deleteSample}
                                                    deleteSampleFile={deleteSampleFile}
                                                    show={showFaceDetail[`showface-list${index}`]}
                                                    setShow={() => handleShowFaceDetail()}
                                                    image={image}>
                                                </FaceDetail>
                                            </div>
                                        })
                                    }

                                    {
                                        imageListFile !== [] && imageListFile.map((image, index) => {
                                            return <div key={index} className="add-zone__captures-item">
                                                <img onClick={() => handleShowFaceDetail(index, true, false)} src={URL.createObjectURL(image)} alt='sample-image'></img>
                                                <i className='bx bx-trash' onClick={() => deleteSampleFile(index)}></i>
                                                <FaceDetail
                                                    isFileSample={true}
                                                    index={index}
                                                    username={userName}
                                                    deleteSample={deleteSample}
                                                    deleteSampleFile={deleteSampleFile}
                                                    show={showFaceDetail[`showface-list-file${index}`]}
                                                    setShow={() => handleShowFaceDetail()}
                                                    image={URL.createObjectURL(image)}>
                                                </FaceDetail>
                                            </div>
                                        })
                                    }
                                </div>
                            </div>
                        </div>

                }

            </div>
            <div className="modal__bottom" style={{ display: "flex", justifyContent: "flex-end" }}>
                <button style={{ marginRight: "10px" }} className="btn btn--danger" onClick={() => setShow(false)}>Huỷ</button>
                <form onSubmit={handleRegister} encType="multipart/form-data">
                    <button
                        disabled={imageList.length + imageListFile.length === 0 || recoding || loading ? true : false}
                        className={`btn btn--success ${imageList.length + imageListFile.length === 0 || recoding || loading ? "btn--disable" : ""}`}
                        type="submit">Đăng kí</button>
                </form>
            </div>
        </div>

    )
}

export default Register