import React from 'react';

class Message extends React.Component{

    render(){
        if(this.props.userMessage !== undefined && this.props.userMessage !== "" && this.props.userStatus !== "" && this.props.userStatus !== undefined){
            return (
                <div className={"ui message " + this.props.userStatus}>{this.props.userMessage}</div>
            )
        }
        return(true);
    }
}


export default Message;