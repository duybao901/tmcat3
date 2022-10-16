import React, { useRef, useEffect, useState } from 'react'
import FaceIcon from '../../images/face-icon.png'
import "./Login.css"
import * as faceapi from 'face-api.js'
import Webcam from 'react-webcam'
import axios from 'axios'
import { toast } from 'react-toastify'

const Login = () => {

    const refWebcam = useRef()
    const refCanvas = useRef()

    const [loadingmodel, setLoadingModel] = useState(false);
    const [refVideo, setRefVideo] = useState()
    const [timer, setTimer] = useState()
    const [captureList, setCaptureList] = useState([])
    const [firstDetection, setFirstDetection] = useState(false)
    const [loading, setLoading] = useState(false);
    const [isLogin, setIsLogin] = useState(false)

    const videoConstraints = {
        facingMode: "user",
        aspectRatio: 1
    };

    useEffect(() => {
        const loadModel = async () => {
            const MODEL_URI = process.env.PUBLIC_URL + '/models'

            Promise.all(
                [
                    faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URI), // Pre-trained model dùng để phát hiện gương mặt.
                    // faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URI),
                    faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URI), // FaceLandmark68Net Model: Pre-trained model dùng để xác định được các điểm xung quanh mặt.
                    //   faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URI) // Pre-trained model dùng để nhận dạng gương mặt.
                ]
            )
            console.log("Loading model success")
            setLoadingModel(true)
        }
        loadModel()
    }, [])

    useEffect(() => {
        if (refWebcam && loadingmodel) {
            setRefVideo(refWebcam.current.video)
        }
    }, [refWebcam, loadingmodel])


    const hanldeCameraPlay = async (e) => {
        if (loadingmodel) {
            // const timerPlay = setInterval(async () => {
            //     if (refVideo) {
            //         refCanvas.current.interHTML = faceapi.createCanvasFromMedia(refVideo)
            //     }

            //     const displaySize = {
            //         width: 640, height: 480
            //     }
            //     faceapi.matchDimensions(refCanvas.current, displaySize)

            //     const detection = await faceapi.detectSingleFace(refVideo, new faceapi.SsdMobilenetv1Options)

            //     if (detection) {
            //         setFirstDetection(true);
            //         const resizeDetections = faceapi.resizeResults(detection, displaySize)

            //         // Xoa cac canvas truoc
            //         if (refCanvas.current) {
            //             refCanvas.current.getContext('2d').clearRect(0, 0, 640, 480)
            //         }

            //         const score = resizeDetections._score
            //         if (score > 0.5) {
            //             if (captureList.length < 5) {
            //                 setCaptureList(prevCaptureList => [...prevCaptureList, { face: refWebcam.current.getScreenshot(), score: score }])
            //             }
            //         }

            //         // Ve
            //         faceapi.draw.drawDetections(refCanvas.current, resizeDetections) // Ve o vuong phat hien
            //     }

            // }, 700)
            // setTimer(timerPlay)
        }
    }

    useEffect(() => {
        return () => {
            clearInterval(timer)
        }
    }, [timer])

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

    function getBestCapture(captures) {
        var maxScoreTemp = 0;
        var bestCapture = {};

        captures.forEach((item) => {
            if (item.score > maxScoreTemp) {
                maxScoreTemp = item.score
                bestCapture = { ...item }
            }
        })

        return bestCapture
    }

    useEffect(() => {
        if (captureList.length >= 5) {
            setFirstDetection(false)
            setIsLogin(true)
            clearInterval(timer)

            const bestCapture = getBestCapture(captureList)
            const capture = dataURLtoFile(bestCapture.face, "user_capture_login")

            if (capture) {
                const login = async () => {
                    try {
                        const formData = new FormData();
                        formData.append("file", capture)

                        const res = await axios.post("http://localhost:5000/api/face/predict", formData)

                        setIsLogin(false)

                        console.log(res.data)

                        toast.success(res.data.username)

                    } catch (error) {
                        console.error(error.response.data.msg)
                    }
                }
                login()
            }
        }
    }, [captureList])

    return (
        <div className='login__wrapper'>

            <div className="modal__header">
                <div className="login__title">
                    <img src={FaceIcon} alt='face-icon'></img>
                    <h2 className='modal__title'><span>Face</span>Login</h2>
                </div>
            </div>
            <div className="modal__body">
                {
                    !firstDetection && <div className={`register__fade ${!isLogin && "register__fade-800"}`}></div>
                }
                {
                    !firstDetection && <>
                        <div className="register__loading">
                            <div className="register__loading-circle">
                                {
                                    isLogin && <p>
                                        Đang đăng nhập
                                    </p>
                                }
                            </div>
                            <img src={FaceIcon} alt='face-icon-loading'></img>

                        </div>
                    </>
                }
                <div className="login__webcam">
                    {
                        <Webcam
                            audio={false}
                            screenshotFormat="image/jpeg"
                            width={"100%"}
                            // height={"100%"}
                            videoConstraints={videoConstraints}
                            ref={refWebcam}
                            screenshotQuality={1}
                            onPlay={hanldeCameraPlay}
                        >
                        </Webcam>
                    }
                    <canvas ref={refCanvas}></canvas>
                </div>
            </div>
        </div>
    )
}

export default Login