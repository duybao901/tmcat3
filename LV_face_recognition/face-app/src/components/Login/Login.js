import React, { useRef, useEffect, useState } from 'react'
import FaceIcon from '../../images/face-icon.png'
import "./Login.css"
import * as faceapi from 'face-api.js'
import Webcam from 'react-webcam'

const Login = ({ setShow }) => {

    const refWebcam = useRef()
    const refCanvas = useRef()

    const [loadingmodel, setLoadingModel] = useState(false);
    const [refVideo, setRefVideo] = useState()
    const [timer, setTimer] = useState()
    const [totalScore, setTotalScore] = useState()

    const videoConstraints = {
        facingMode: "user",
        aspectRatio: 1.2
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
            const timerPlay = setInterval(async () => {
                if (refVideo) {
                    refCanvas.current.interHTML = faceapi.createCanvasFromMedia(refVideo)
                }

                const displaySize = {
                    width: 640, height: 480
                }
                faceapi.matchDimensions(refCanvas.current, displaySize)

                const detection = await faceapi.detectSingleFace(refVideo, new faceapi.SsdMobilenetv1Options)
                const resizeDetections = faceapi.resizeResults(detection, displaySize)

                // Xoa cac canvas truoc
                if (refCanvas.current) {
                    refCanvas.current.getContext('2d').clearRect(0, 0, 640, 480)
                }

                const score = resizeDetections._score

                if (score > 0.5) {

                }

                // Ve
                faceapi.draw.drawDetections(refCanvas.current, resizeDetections) // Ve o vuong phat hien


            }, 500)

            setTimer(timerPlay)
        }
    }


    useEffect(() => {
        return () => {
            clearInterval(timer)
        }
    }, [timer])



    return (
        <div>
            <div className="modal__header">
                <div className="login__title">
                    <img src={FaceIcon} alt='face-icon'></img>
                    <h2 className='modal__title'><span>Face</span>Login</h2>
                </div>
                <div className='modal__close' onClick={() => setShow(false)}>
                    <i className='bx bx-x'></i>
                </div>
            </div>
            <div className="modal__body">
                <div className="login__webcam">
                    {
                        <Webcam
                            audio={false}
                            screenshotFormat="image/jpeg"
                            width={"100%"}
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