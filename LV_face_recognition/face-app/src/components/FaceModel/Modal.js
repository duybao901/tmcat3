import React from 'react'
import "./Modal.css"
import ReactDOM from 'react-dom'
import { CSSTransition } from "react-transition-group";

const Modal = ({ children, show, setShow }) => {

    const onClosemodal = () => {
        setShow(false)
    }

    return ReactDOM.createPortal(
        <CSSTransition
            in={show}
            unmountOnExit
            timeout={{ enter: 0, exit: 250 }}
        >
            <div className="modal" onClick={onClosemodal}>
                <div className="modal__content" onClick={(e) => e.stopPropagation()}>
                    {children}
                </div>
            </div>
        </CSSTransition>,
        document.getElementById('root')

    )
}

export default Modal