import React from 'react'
import "./Model.css"

const Model = ({children, show}) => {
    console.log(show)
    return (
        <div className="model">
            <div className="model__content">
                {children}
            </div>
        </div>
    )
}

export default Model