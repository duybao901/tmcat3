import React from 'react'
import "./FaceDetail.css"
import ReactDOM from 'react-dom'
import { CSSTransition } from 'react-transition-group'
const FaceDetail = ({ username, image, index, setShow, show, deleteSampleFile, deleteSample, isFileSample }) => {

    const handleDeleteSample = (index) => {
            setShow(false)

        if (isFileSample) {
            deleteSampleFile(index)
        } else {
            deleteSample(index)
        }

    }

    return ReactDOM.createPortal(
        <CSSTransition
            in={show}
            unmountOnExit
            timeout={{ enter: 0, exit: 0 }}
        >
            <div className="face-detail" onClick={() => setShow(false)}>
                <div className="face-detail__body" onClick={(e) => e.stopPropagation()}>
                    <div className="face-detail__head">
                        <h4>{username}</h4>
                        <div className='modal__close' onClick={() => setShow(false)}>
                            <i className='bx bx-x'></i>
                        </div>
                    </div>
                    <div className="face-detail__content">
                        <img src={image} alt='face'></img>
                        <i onClick={() => handleDeleteSample(index)} className='bx bx-trash'></i>
                    </div>
                </div>
            </div>

        </CSSTransition>,
        document.getElementById('root')
    )
}

export default FaceDetail