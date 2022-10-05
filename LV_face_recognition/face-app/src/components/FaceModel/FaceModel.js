import React from 'react'
import "./FaceModel.css"

const FaceModel = () => {
    return (
        <div className="face-model">
            <div className="face-model__content">
                <div className="face-model__header">
                    <div>
                        <input className="face-model__username" type="text" placeholder="UserName" />
                        <i className='bx bx-pencil'></i>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default FaceModel