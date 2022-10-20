import React from "react";

export function Alert({type, message}) {
    return (
    <div>
            { 
                type !== 'alert-success' ?
                    (
                        <div className="alert alert-danger" role="alert">
                            {message}
                        </div>
                    ) : 
                    (
                        <div className="alert alert-success" role="alert">
                            {message}
                        </div>
                    ) 
        }
    </div>
  );
};
