import React from 'react'
import "./Register.css"

const Register = () => {
    return (
        <div>
            <div className='face-model__content'>
                <div className="model__header">
                    <div>
                        <input className="face-model__username" type="text" placeholder="UserName" />
                        <i className='bx bx-pencil'></i>
                    </div>
                    <div className='face-model'>
                        <i className='bx bx-x'></i>
                    </div>
                </div>
                <div className="model__body">
                    This is model body
                </div>
                <div className="model__bottom">
                    <button>close</button>
                </div>
            </div>
        </div>
    )
}

export default Register